# HRIS Dashboard

This project turns raw HR data into:
- **Time-to-Fill** for closed jobs
- **Recruiting Funnel** (Applied → Screen → Interview → Offer → Hired)
- **Payroll mismatch** checks (Active but Unpaid)

## How to run
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/compute_metrics.py

