#!/usr/bin/env python3
"""Ingest Irish Life Health Tables of Cover (TOC) into plans.json/plans.csv.

This script pulls the public Irish Life 'Tables of Cover' page, extracts all PDF links,
and writes/updates plan rows so that each ILH plan has a direct public PDF URL.

- Public sources only
- No premiums scraped; no quote engines used
"""

import argparse
import datetime
import json
import re
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

ILH_TOC_PAGE = "https://www.irishlife.ie/health-insurance/help/tables-of-cover/"
KEY_FIELDS = [
  "plan_tier","hospital_cover","outpatient_cover","gp_visits","maternity_cover",
  "mental_health","overseas_emergency","semi_private_room","private_room","excess_required"
]

def slugify(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"&", "and", s)
    s = re.sub(r"[^a-z0-9]+", "_", s)
    return s.strip("_")

def compute_completeness(df: pd.DataFrame) -> pd.DataFrame:
    for col in KEY_FIELDS:
        if col not in df.columns:
            df[col] = pd.NA
    df["null_key_count"] = df[KEY_FIELDS].isna().sum(axis=1)
    df["completeness_score"] = (len(KEY_FIELDS) - df["null_key_count"]) / len(KEY_FIELDS)
    return df

def fetch_ilh_toc_links():
    resp = requests.get(ILH_TOC_PAGE, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    links = []
    for a in soup.find_all("a"):
        href = a.get("href") or ""
        text = (a.get_text() or "").strip()
        if href.lower().endswith(".pdf") and text:
            if href.startswith("//"):
                href = "https:" + href
            elif href.startswith("/"):
                href = "https://www.irishlife.ie" + href
            links.append((text, href))
    # de-dupe by href
    out, seen = [], set()
    for text, href in links:
        if href in seen:
            continue
        seen.add(href)
        out.append((text, href))
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plans_json", default="plans.json")
    ap.add_argument("--plans_csv", default="plans.csv")
    ap.add_argument("--out_json", default="plans.json")
    ap.add_argument("--out_csv", default="plans.csv")
    args = ap.parse_args()

    in_json = Path(args.plans_json)
    in_csv = Path(args.plans_csv)

    if in_json.exists():
        payload = json.loads(in_json.read_text(encoding="utf-8"))
        df = pd.DataFrame(payload["plans"])
    elif in_csv.exists():
        df = pd.read_csv(in_csv)
    else:
        raise SystemExit("No input plans.json or plans.csv found")

    links = fetch_ilh_toc_links()
    today = datetime.date.today().isoformat()

    # Remove existing ILH PDF rows to avoid duplicates
    if "insurer" in df.columns and "source_url" in df.columns:
        df = df[~((df["insurer"] == "Irish Life Health") & (df["source_url"].astype(str).str.endswith(".pdf")))]

    new_rows = []
    for plan_name, pdf_url in links:
        plan_id = "ILH_" + slugify(plan_name).upper()
        new_rows.append({
            "plan_id": plan_id,
            "insurer": "Irish Life Health",
            "plan_name": plan_name,
            "plan_tier": pd.NA,
            "hospital_cover": pd.NA,
            "semi_private_room": pd.NA,
            "private_room": pd.NA,
            "day_case": pd.NA,
            "outpatient_cover": pd.NA,
            "gp_visits": pd.NA,
            "maternity_cover": pd.NA,
            "maternity_waiting_months": pd.NA,
            "mental_health": pd.NA,
            "cardiac_cover": pd.NA,
            "cancer_cover": pd.NA,
            "overseas_emergency": pd.NA,
            "overseas_planned": pd.NA,
            "excess_required": pd.NA,
            "excess_amount_text": pd.NA,
            "regulatory_notes": "Ingested from ILH Tables of Cover page; enrich key fields from the PDF.",
            "source_url": pdf_url,
            "public_open_url": pdf_url,
            "doc_type": "TOC_PDF",
            "effective_from": pd.NA,
            "last_verified": today
        })

    df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)

    # Ensure columns exist
    for col in ["public_open_url","doc_type","effective_from","last_verified"]:
        if col not in df.columns:
            df[col] = pd.NA

    df = compute_completeness(df)

    Path(args.out_csv).write_text(df.to_csv(index=False), encoding="utf-8")

    out_json_payload = {
        "version": "ILH_TOC_REFRESH_" + today,
        "generated_utc": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "plans": df.to_dict(orient="records"),
        "notes": [
            "Irish Life Health TOC list refreshed from the public Tables of Cover page.",
            "Contains direct public PDF URLs for ILH plans."
        ]
    }
    Path(args.out_json).write_text(json.dumps(out_json_payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"ILH TOC PDFs ingested: {len(links)}")
    print(f"Total plans now: {len(df)}")

if __name__ == "__main__":
    main()