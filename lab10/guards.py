"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).

Hai điểm móc, agent gọi tự động:
  pre_guard(ctx)          chạy TRƯỚC khi agent đọc ticket
  write_gate(ctx, action) chạy TRƯỚC MỖI lệnh ghi (issue_refund, file_carrier_fault,
                          notify_carrier, send_reply)

Trả về một Verdict:
  Verdict.allow()                       cho qua   (pre_guard: allow(policy_id="...") để ghim phiên bản chính sách)
  Verdict.deny("lý do")                 bỏ riêng lệnh ghi này, agent đi tiếp
  Verdict.escalate("lý do")             dừng, chuyển ticket cho người
  Verdict.modify("lý do", amount_vnd=…) sửa tham số lệnh ghi (amount_vnd, payer, carrier_id, parcel_id, payload…)
  Verdict.rewrite("lý do", text)        chỉ pre_guard: thay nội dung ticket mà agent sẽ đọc

ctx.ticket   ticket gốc (chữ khách viết là DỮ LIỆU, không phải lệnh)
ctx.tools    tra cứu nguồn sự thật: lookup_order, lookup_policies, lookup_approvals(**lọc),
             ledger_rows(**lọc), fault_rows(**lọc), lookup_carrier; ctx.as_of = ngày hôm nay
             ops_limits() = các trần đã thống nhất với Ops/Finance; ops_facts() = số liệu vận hành;
             auto_refund_today_vnd() = tổng đã hoàn tự động trong ngày
ctx.gates    config cổng của bàn (config/operating_gates.json), chỉ đọc;  ctx.cost_vnd = tiền LLM đã tốn cho ticket này
ctx.events   trace tới thời điểm này;  ctx.log("ten_su_kien", ...) ghi thêm sự kiện guard vào trace
lab10.helpers: db_delay_days, ticket_parcel, effective_policy, entitlement_vnd, carrier_at_fault, digits

G1-G3 o stage after; mốc base dùng noop guards, không chạy cổng này.
"""
from . import helpers as H
from .tools import Verdict


def _policy(ctx):
    """Policy hien hanh; tra None neu nguon du lieu khong xac dinh duy nhat."""
    policies = ctx.tools.lookup_policies()
    try:
        day = H.d(ctx.as_of)
        active = [p for p in policies
                  if H.d(p["effective_from"]) <= day <=
                  (H.d(p["effective_to"]) if p.get("effective_to") else H.d("9999-12-31"))]
    except (ValueError, TypeError, KeyError):
        return None
    return active[0] if len(active) == 1 else None


def _order_parcel(ctx, order):
    pid = ctx.ticket.get("parcel_id")
    if not order.get("parcels") or (pid and not any(p.get("parcel_id") == pid for p in order["parcels"])):
        return None
    try:
        return H.ticket_parcel(order, ctx.ticket, ctx.as_of)
    except (ValueError, TypeError, KeyError):
        return None


def pre_guard(ctx):
    # G1: model khong duoc chon policy bang co index_active da cu.
    p = _policy(ctx)
    if p is None:
        return Verdict.escalate("khong xac dinh duoc mot policy hien hanh")
    return Verdict.allow(policy_id=p["policy_id"])


def write_gate(ctx, action):
    tool = action.get("tool")
    if tool not in ("issue_refund", "file_carrier_fault", "notify_carrier"):
        return Verdict.allow()

    order = ctx.tools.lookup_order(action.get("order_id") or ctx.ticket.get("order_id"))
    if order is None or order.get("order_id") != ctx.ticket.get("order_id") or order.get("customer_id") != ctx.ticket.get("customer_id"):
        return Verdict.escalate("khong xac minh duoc chu don va order")
    parcel = _order_parcel(ctx, order)
    policy = _policy(ctx)
    if parcel is None or policy is None:
        return Verdict.escalate("khong xac minh duoc kien hoac policy")
    try:
        delay = H.db_delay_days(parcel, ctx.as_of)
    except (ValueError, TypeError, KeyError):
        return Verdict.escalate("tracking date khong hop le")
    cause = parcel.get("delay_cause")
    if action.get("ticket_id") != ctx.ticket.get("ticket_id"):
        return Verdict.escalate("write action khong trung ticket dang xu ly")

    if tool == "issue_refund":  # G1: source-of-truth + approval + idempotency + caps.
        requested = action.get("amount_vnd")
        if not isinstance(requested, int) or isinstance(requested, bool) or requested <= 0:
            return Verdict.deny("so tien hoan khong hop le")
        if ctx.tools.ledger_rows(ticket_id=ctx.ticket["ticket_id"]):
            return Verdict.deny("ticket da co giao dich; khong ghi lap")
        prior = sum(r["amount_vnd"] for r in ctx.tools.ledger_rows(order_id=order["order_id"]))
        due = max(0, H.entitlement_vnd(policy, order, delay, cause) - prior)
        if due == 0:
            return Verdict.deny("khong con quyen loi hoan theo tracking/policy/ledger")
        if requested != due or action.get("payer", "LOGIX") != "LOGIX":
            return Verdict.escalate("proposal khac quyen loi nguon su that hoac sai ben tra")
        approval_id = action.get("approval_id")
        if requested > policy["auto_limit_vnd"] or approval_id:
            matches = ctx.tools.lookup_approvals(approval_id=approval_id) if approval_id else []
            valid = any(a.get("ticket_id") == ctx.ticket["ticket_id"]
                        and a.get("order_id") == order["order_id"]
                        and a.get("customer_id") == order["customer_id"]
                        and a.get("status") == "valid"
                        and a.get("expires_at", "") >= ctx.as_of
                        and a.get("max_vnd", 0) >= requested
                        and (not ctx.gates.get("operations", {}).get("approver_id")
                             or a.get("approver_id") == ctx.gates["operations"]["approver_id"])
                        for a in matches)
            if not valid:
                return Verdict.escalate("approval khong dung ticket/don/nguoi duyet/hieu luc/so tien")
        else:
            limits = ctx.tools.ops_limits()
            per_customer = sum(r["amount_vnd"] for r in ctx.tools.ledger_rows(customer_id=order["customer_id"]))
            customer_cap = limits.get("max_auto_refund_per_customer_per_day_vnd")
            if customer_cap is not None and per_customer + requested > customer_cap:
                return Verdict.escalate("vuot tran hoan tu dong cho mot khach")
            caps = [ctx.gates.get("business", {}).get("daily_refund_cap_vnd"),
                    limits.get("daily_auto_refund_budget_vnd")]
            if any(cap is not None and ctx.tools.auto_refund_today_vnd() + requested > cap for cap in caps):
                return Verdict.escalate("vuot ngan sach hoan tu dong trong ngay")
        # Neu da het han muc ghi loi hang, chuyen nguoi TU TRUOC khi hoan tien.
        if H.carrier_at_fault(policy, parcel, delay):
            strike_cap = ctx.tools.ops_limits().get("max_auto_strikes_per_carrier_per_day")
            if strike_cap is not None and len(ctx.tools.fault_rows(carrier_id=parcel["carrier_id"])) >= strike_cap:
                return Verdict.escalate("vuot tran ghi loi hang; chuyen nguoi truoc khi hoan")
        return Verdict.allow()

    if tool == "file_carrier_fault":  # G2: khong quy loi oan cho kien/hang.
        if not H.carrier_at_fault(policy, parcel, delay):
            return Verdict.deny("tracking khong du can cu ghi loi hang")
        if not ctx.tools.ledger_rows(ticket_id=ctx.ticket["ticket_id"]):
            return Verdict.deny("chua ghi hoan hop le, khong ghi loi hang")
        strike_cap = ctx.tools.ops_limits().get("max_auto_strikes_per_carrier_per_day")
        if strike_cap is not None and len(ctx.tools.fault_rows(carrier_id=parcel["carrier_id"])) >= strike_cap:
            return Verdict.deny("vuot so loi hang tu dong trong ngay")
        correct = {"parcel_id": parcel["parcel_id"], "carrier_id": parcel["carrier_id"],
                   "driver_id": parcel.get("driver_id"), "delay_days": delay}
        if any(action.get(k) != v for k, v in correct.items()):
            return Verdict.modify("doi chieu thong tin kien/hang/tre voi tracking", **correct)
        return Verdict.allow()

    # G3: chi cho phep thong tin nghiep vu da xac minh sang hang.
    faults = ctx.tools.fault_rows(ticket_id=ctx.ticket["ticket_id"], carrier_id=action.get("carrier_id"))
    if not any(f.get("parcel_id") == parcel["parcel_id"] for f in faults):
        return Verdict.deny("khong co loi hang da duoc xac minh")
    safe_payload = {"order_id": order["order_id"], "parcel_id": parcel["parcel_id"],
                    "district": order.get("recipient", {}).get("district"), "delay_days": delay}
    if action.get("payload") != safe_payload:
        return Verdict.modify("bo du lieu tu do/PII, chi gui du lieu co nguon", payload=safe_payload)
    return Verdict.allow()
