/**
 * @param {Response} response
 * @returns {Promise<any>}
 */
export async function parseJson(response) {
    if (!response.ok) {
        throw new Error(`Request failed (${response.status})`);
    }

    if (response.status === 204) {
        return null;
    }

    return response.json();
}
