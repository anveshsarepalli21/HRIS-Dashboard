import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed"

def compute_ttf(jobs: pd.DataFrame) -> pd.DataFrame:
    closed = jobs.dropna(subset=["closed_date"]).copy()
    closed["opened_date"] = pd.to_datetime(closed["opened_date"])
    closed["closed_date"] = pd.to_datetime(closed["closed_date"])
    closed["time_to_fill_days"] = (closed["closed_date"] - closed["opened_date"]).dt.days
    return closed[["job_id","role","dept","time_to_fill_days"]].sort_values("time_to_fill_days")

def compute_funnel(apps: pd.DataFrame) -> pd.DataFrame:
    g = apps.groupby(["job_id","stage"]).size().reset_index(name="count")
    wide = g.pivot(index="job_id", columns="stage", values="count").fillna(0).reset_index()
    return wide

def compute_unpaid_active(emp: pd.DataFrame, pay: pd.DataFrame, month: str) -> pd.DataFrame:
    active = emp[emp["status"]=="Active"][["emp_id","first_name","last_name","dept","role"]]
    paid = pay[pay["month"]==month][["emp_id","paid"]]
    merged = active.merge(paid, on="emp_id", how="left")
    return merged[(merged["paid"].isna()) | (merged["paid"]==0)].fillna({"paid":0})

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    emp = pd.read_csv(RAW / "employees.csv")
    jobs = pd.read_csv(RAW / "job_postings.csv")
    apps = pd.read_csv(RAW / "applications.csv")
    pay  = pd.read_csv(RAW / "payroll.csv")

    jobs["opened_date"] = pd.to_datetime(jobs["opened_date"])
    jobs["closed_date"] = pd.to_datetime(jobs["closed_date"], errors="coerce")
    apps["stage"] = apps["stage"].str.title()

    ttf = compute_ttf(jobs)
    funnel = compute_funnel(apps)
    mismatches = compute_unpaid_active(emp, pay, month="2025-02")

    ttf.to_csv(OUT / "ttf.csv", index=False)
    funnel.to_csv(OUT / "funnel.csv", index=False)
    mismatches.to_csv(OUT / "payroll_mismatch.csv", index=False)

    print("Wrote:")
    for f in ["ttf.csv","funnel.csv","payroll_mismatch.csv"]:
        print(f" - data/processed/{f}")

if __name__ == "__main__":
    main()
