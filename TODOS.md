# AI task suggestions

- Debounce suggestion requests (500–1000 ms after user stops typing).
- Cancel in-flight requests when a new one starts (AbortController).
- Attach a request version/ID and ignore stale responses that arrive out of order.
- Trigger suggestions only after sufficient input length or explicit refresh.

# LLM

- Retry malformed JSON responses.
- Add timeout handling.
- Log prompt latency and parsing failures.
- Cache identical suggestion requests.

# Optimization

- Caching — cache hot/read-heavy data; invalidate on mutation, with TTL as a fallback.
- Database indexing — indexes for actual query patterns; composite indexes where appropriate.
- Query optimization — avoid N+1 queries, unnecessary columns, huge scans, bad joins.
- Pagination — cursor/keyset pagination for large datasets instead of giant OFFSETs.
- Async I/O — don't block threads on DB/network/file operations.
- Connection pooling — tune DB/HTTP pools and watch for pool exhaustion.
- Background jobs — move expensive/non-urgent work to queues + workers.
- Rate limiting — prevent abusive traffic from consuming resources.
- Observability — latency percentiles, traces, CPU/memory, DB latency, queue depth, errors.
- Load testing — find bottlenecks before production does.
- Idempotency — make retries safe for operations like payments/jobs.
- Concurrency control — transactions/locks/atomic operations around shared state.
