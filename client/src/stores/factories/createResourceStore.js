/**
 * @typedef {'idle' | 'loading' | 'success' | 'error'} ResourceStatus
 */

/**
 * @template T
 * @callback ResourceFetcher
 * @param {string} key
 * @param {AbortSignal} signal
 * @returns {Promise<T>}
 */

/**
 * @template T
 * @param {ResourceFetcher<T>} fetcher
 */
export function createResourceStore(fetcher) {
    const state = {
        items: /** @type {Record<string, T>} */ ({}),
        status: /** @type {Record<string, ResourceStatus>} */ ({}),
        errors: /** @type {Record<string, Error | null>} */ ({}),
    };

    /** @type {Map<string, Promise<T>>} */
    const inflight = new Map();

    /** @type {Map<string, AbortController>} */
    const controllers = new Map();

    const actions = {
        /**
         * @param {string} key
         * @param {{ force?: boolean }} [options]
         * @returns {Promise<T | undefined>}
         */
        async fetch(key, options = {}) {
            const force = options.force ?? false;

            if (
                !force &&
                state.status[key] === "success" &&
                state.items[key] !== undefined
            ) {
                return state.items[key];
            }

            if (!force && inflight.has(key)) {
                return inflight.get(key);
            }

            controllers.get(key)?.abort();
            const controller = new AbortController();
            controllers.set(key, controller);

            state.status[key] = "loading";
            state.errors[key] = null;

            const promise = fetcher(key, controller.signal)
                .then((data) => {
                    state.items[key] = data;
                    state.status[key] = "success";
                    return data;
                })
                .catch((error) => {
                    const normalizedError =
                        error instanceof Error
                            ? error
                            : new Error(String(error));
                    state.status[key] = "error";
                    state.errors[key] = normalizedError;
                    throw normalizedError;
                })
                .finally(() => {
                    inflight.delete(key);
                    controllers.delete(key);
                });

            inflight.set(key, promise);
            return promise;
        },

        /**
         * @param {string} key
         */
        invalidate(key) {
            controllers.get(key)?.abort();
            controllers.delete(key);
            inflight.delete(key);
            delete state.items[key];
            delete state.status[key];
            delete state.errors[key];
        },
    };

    return { state, actions };
}
