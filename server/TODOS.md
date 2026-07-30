# AI task suggestions

- Debounce suggestion requests (500–1000 ms after user stops typing).
- Cancel in-flight requests when a new one starts (AbortController).
- Attach a request version/ID and ignore stale responses that arrive out of order.
- Trigger suggestions only after sufficient input length or explicit refresh.

# Embeddings

- Move embedding generation to background workers.
- Batch/recompute embeddings for existing tasks if the embedding model changes.

# Backend

- Restrict CORS to trusted origins instead of "*".
- Design a consistent application-wide error handling strategy.

# LLM

- Retry malformed JSON responses.
- Add timeout handling.
- Log prompt latency and parsing failures.
- Cache identical suggestion requests.
