const ELEMENTS_TO_STRIP = ["script", "style", "template", "noscript"];

/** @type {HTMLDivElement | null} */
let sharedContainer = null;

/** @returns {HTMLDivElement | null} */
function getContainer() {
    if (typeof document === "undefined") return null;
    if (!sharedContainer) {
        sharedContainer = document.createElement("div");
    }
    return sharedContainer;
}

/**
 * @param {String} html
 * @returns {Boolean}
 */
export function isHtmlEmpty(html) {
    if (!html) return true;

    const doc = new DOMParser().parseFromString(html, "text/html");

    // real text content (nbsp counts as whitespace)
    const text = doc.body.textContent?.replace(/\u00a0/g, " ").trim();
    if (text?.length) return false;

    return true;
}

/**
 * @param {String} html
 * @returns {string}
 */
function stripHtmlWithRegex(html) {
    return (
        html
            // Drop script/style/template blocks entirely, including their content.
            .replace(/<(script|style|template)[^>]*>[\s\S]*?<\/\1>/gi, " ")
            // Convert block-ish closing tags to a space so words don't run together.
            .replace(/<\/(p|div|br|li|tr|h[1-6])>/gi, " ")
            // Strip remaining tags.
            .replace(/<[^>]*>/g, "")
            // Decode a small set of common named entities + numeric entities.
            .replace(/&nbsp;/gi, " ")
            .replace(/&amp;/gi, "&")
            .replace(/&lt;/gi, "<")
            .replace(/&gt;/gi, ">")
            .replace(/&quot;/gi, '"')
            .replace(/&#39;|&apos;/gi, "'")
            .replace(/&#(\d+);/g, (_, dec) => String.fromCodePoint(Number(dec)))
            .replace(/&#x([0-9a-f]+);/gi, (_, hex) =>
                String.fromCodePoint(parseInt(hex, 16))
            )
    );
}

/**
 * @param {unknown} html
 * @returns {string}
 */
export function htmlToText(html) {
    if (typeof html !== "string" || html.length === 0) return "";

    let text;
    const container = getContainer();

    if (container) {
        container.innerHTML = html;
        for (const tag of ELEMENTS_TO_STRIP) {
            const nodes = container.querySelectorAll(tag);
            nodes.forEach((node) => node.remove());
        }
        text = container.textContent ?? "";
        container.innerHTML = "";
    } else {
        text = stripHtmlWithRegex(html);
    }

    return text.replace(/\s+/g, " ").trim();
}

/**
 * @param {unknown} html
 * @param {number} [maxLength=160]
 * @returns {string}
 */
export function htmlPreview(html, maxLength = 160) {
    const text = htmlToText(html);

    const safeMaxLength =
        Number.isFinite(maxLength) && maxLength > 0
            ? Math.floor(maxLength)
            : 160;

    const chars = Array.from(text);

    if (chars.length <= safeMaxLength) {
        return text;
    }

    let truncated = chars.slice(0, safeMaxLength).join("");

    const lastSpace = truncated.lastIndexOf(" ");
    if (lastSpace > safeMaxLength * 0.6) {
        truncated = truncated.slice(0, lastSpace);
    }

    return `${truncated.trimEnd()}…`;
}
