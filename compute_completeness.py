#!/usr/bin/env python3
"""Compute completeness_score for plans.csv.

Usage:
  python compute_completeness.py plans.csv plans_with_completeness.csv

Notes:
- Completeness is computed only across key decision fields (see KEY_FIELDS below).
- NULL/blank values count as missing.
- This script does NOT scrape the web; it only processes your local CSV.
"""

import sys
import pandas as pd

KEY_FIELDS = [
  "plan_tier","hospital_cover","outpatient_cover","gp_visits","maternity_cover",
  "mental_health","overseas_emergency","semi_private_room","private_room","excess_required"
]

def main():
    if len(sys.argv) != 3:
        print("Usage: python compute_completeness.py <input_plans.csv> <output_plans.csv>")
        sys.exit(2)

    in_path, out_path = sys.argv[1], sys.argv[2]
    df = pd.read_csv(in_path)

    for col in KEY_FIELDS:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    df["null_key_count"] = df[KEY_FIELDS].isna().sum(axis=1)
    df["completeness_score"] = (len(KEY_FIELDS) - df["null_key_count"]) / len(KEY_FIELDS)

    df.to_csv(out_path, index=False)

    # Summary
    print("Rows:", len(df))
    print("Avg completeness:", round(df["completeness_score"].mean(), 3))
    print("Lowest completeness rows:")
    print(df.sort_values("completeness_score").head(10)[["plan_id","insurer","plan_name","completeness_score","null_key_count"]])

if __name__ == "__main__":
    main()
