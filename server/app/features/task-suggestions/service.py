"""
A couple of implementation details make it feel polished:
- Debounce requests (e.g. 500–1000 ms after typing stops).
- Cancel the previous request if the user types again (using AbortController in the browser).
- Include a request ID/version so if an older response arrives after a newer one, you ignore it.
"""
