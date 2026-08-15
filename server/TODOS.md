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
