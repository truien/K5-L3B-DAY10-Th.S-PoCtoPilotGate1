"""★ FILE ĐỘI SỬA (2/3): chỉ số theo dõi (monitor). Thêm ÍT NHẤT MỘT chỉ số bắt được sự cố của bàn.

Mỗi monitor nhận danh sách trial (KHÔNG có nhãn đúng/sai, giống production) và trả về một số.
Một trial = {"ticket_id", "seed", "day", "status", "amount_vnd", "ticket", "events", "ledger", "faults", "outbound",
             "arrive_min", "warehouse", "cost_vnd", "review_kind", "queue_wait_min", "queue_stuck"}
  "day"            một ngày vận hành giả lập: các ticket cùng "day" và cùng "seed" chạy nối nhau trên cùng một sổ cái
  "arrive_min"     phút ticket tới trong ca (0..480)          "warehouse"   kho của đơn
  "cost_vnd"       tiền LLM + nền tảng đã tốn cho ticket      "review_kind" None / "escalated" (trợ lý chuyển người) /
  "queue_wait_min" số phút chờ người duyệt (None nếu không vào hàng chờ)     "recheck" (nhân viên tự kiểm lại)
Chỉ số có thể là kỹ thuật (tỉ lệ model đè số trong ticket lên DB), vận hành (số ca cần người trong giờ đông nhất),
hay kinh doanh (tỉ lệ ticket trợ lý đọc xong vẫn phải chuyển người).

lab10.grade kiểm: monitor chạy không lỗi, và giá trị trên gói sự cố khác giá trị trên bộ nền,
tức là monitor "sáng đèn" khi sự cố xảy ra.
"""


def escalation_rate(trials):
    return sum(t["status"] == "escalated" for t in trials) / max(1, len(trials))


def source_of_truth_conflict_rate(trials):
    """Share of trials where a guard detects incomplete tracking or a conflicting numeric delay claim.

    Uses runtime guard events only; it does not inspect labels or expected outcomes.
    """
    kinds = {"parcel_tracking_incomplete", "false_denial_conflict", "delay_claim_conflict_rewritten"}
    flagged = 0
    for trial in trials:
        events = trial.get("events") or []
        if any(e.get("type") == "guard" and e.get("kind") in kinds for e in events):
            flagged += 1
    return flagged / max(1, len(trials))


def max_carrier_faults_per_simulated_day(trials):
    """Peak unique carrier-fault rows for one simulated day/scenario, seed and carrier."""
    buckets = {}
    for trial in trials:
        base = (trial.get("day"), trial.get("seed"))
        for fault in trial.get("faults") or []:
            key = (*base, fault.get("carrier_id"))
            row = (fault.get("ticket_id"), fault.get("parcel_id"))
            buckets.setdefault(key, set()).add(row)
    return max((len(rows) for rows in buckets.values()), default=0)


MONITORS = {
    "escalation_rate": escalation_rate,     # có sẵn; KHÔNG tính là metric mới của đội
    "source_of_truth_conflict_rate": source_of_truth_conflict_rate,
    "max_carrier_faults_per_simulated_day": max_carrier_faults_per_simulated_day,
}
STARTER_MONITORS = ("escalation_rate",)
