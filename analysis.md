# Reading the plans

Compare Execution Time and shared hit/read blocks. Small relations can retain sequential scans even after indexes. The customer join can use nested loops with indexed probes. Aggregation may still favor a full scan and hash aggregate. The date index narrows a range, the expression index supports lowercase prefix search, and the partial index narrows expensive orders. Review actual row estimates before concluding an index is beneficial.
