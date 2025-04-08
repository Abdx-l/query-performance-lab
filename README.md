# Query Performance Lab

Deterministic PostgreSQL data generation and five query-tuning experiments with before/after EXPLAIN ANALYZE BUFFERS JSON plans. Dataset size is configurable; no benchmark numbers are preclaimed.

## Run

Start PostgreSQL, set DATABASE_URL, install requirements.txt, run `python lab.py --customers 100000 --orders 1000000`. Plans and timings are written to results/. Run with smaller counts for a smoke check.
