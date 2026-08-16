const requestCache = new Map();

const DEFAULT_TTL = 60_000;

/**
 * @template T
 * @param {string} key
 * @param {() => Promise<T>} fn
 * @param {Object} [options]
 * @param {number} [options.ttl]
 * @param {boolean} [options.forceRefresh]
 * @returns {Promise<T>}
 */
export function cachedRequest(
    key,
    fn,
    { ttl = DEFAULT_TTL, forceRefresh = false } = {}
) {
    const entry = requestCache.get(key);

    if (!forceRefresh && entry) {
        const isPending = entry.status === "pending";
        const isFresh =
            entry.status === "resolved" && Date.now() - entry.ts < ttl;

        if (isPending || isFresh) {
            return entry.promise;
        }
    }

    const promise = fn()
        .then((result) => {
            requestCache.set(key, {
                promise: Promise.resolve(result),
                status: "resolved",
                ts: Date.now(),
            });
            return result;
        })
        .catch((err) => {
            requestCache.delete(key);
            throw err;
        });

    requestCache.set(key, { promise, status: "pending", ts: Date.now() });

    return promise;
}

/** @param {String} prefix */
export function invalidateRequestCache(prefix) {
    for (const key of requestCache.keys()) {
        if (key.startsWith(prefix)) requestCache.delete(key);
    }
}
