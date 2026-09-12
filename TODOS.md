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

# Refactor models

- Database Constraints: Enforce invariants at the database layer—temporal ordering (expires_at > created_at), enum validity (status IN (...)), XOR logic (revoked OR replaced, not both), and cross-field relationships.

- Strategic Indexing: Beyond single-column indexes on foreign keys, add composite indexes on common query patterns (e.g., (user_id, status, created_at) for filtering; (user_id, expires_at) for expiration checks). Index nullable fields that are frequently filtered (revoked_at, deleted_at).

- Explicit Relationship Loading: Replace default lazy loading with lazy="raise" to surface N+1 query bugs during development, then strategically use lazy="joined" or lazy="selectin" only where needed—never hide performance problems.

- Business Logic Methods: Encapsulate state validation in model methods (is_valid(), is_expired(), can_transition_to()) rather than scattering logic across service layers. This keeps invariants close to the data they protect.

- Consistent Field Typing & Constraints: Use bounded String(N) over unbounded types, specify nullable=False explicitly, leverage PostgreSQL-specific types (UUID, JSON), and match Python types exactly (avoid str | None without nullable=True). Document why fields are nullable.

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
