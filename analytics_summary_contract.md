# Analytics Summary Output Contract (v1.4.1)

Generated: 2026-02-28T18:34:09Z

Returned by `GET /analytics_summary`.

```json
{
  "generated_utc": "2026-02-28T18:34:09Z",
  "window_days": 7,
  "plan_clicks": [{"plan_id":"ILH_OPTIMISE_GOLD_TOC","count":123}],
  "question_metrics": [
    {
      "question_id":"Q_HOSPITAL_LEVEL",
      "asked_count":540,
      "avg_info_gain":0.62,
      "dropoff_rate":0.05,
      "avg_time_to_answer_sec":12.4
    }
  ],
  "rank_changes": [
    {"question_id":"Q_MATERNITY","old_rank":5,"new_rank":3}
  ]
}
```

Ranking suggestion:
`score = 0.55*avg_info_gain + 0.25*(1-dropoff_rate) + 0.20*popularity_weight`