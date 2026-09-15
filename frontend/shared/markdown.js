/**
 * Shared Markdown rendering for AI-generated text.
 * Requires marked.js and DOMPurify to be loaded first (see the <script> tags
 * this file's own comment block in each page that uses it).
 *
 * Include with:
 *   <script src="https://cdnjs.cloudflare.com/ajax/libs/marked/12.0.2/marked.min.js"></script>
 *   <script src="https://cdnjs.cloudflare.com/ajax/libs/dompurify/3.1.6/purify.min.js"></script>
 *   <script src="shared/markdown.js"></script>  (or "../shared/markdown.js" from dashboard/*.html)
 */

/**
 * Render Markdown text (e.g. from an LLM response) to sanitized HTML,
 * safe to assign to innerHTML.
 *
 * @param {string} text - raw Markdown text
 * @returns {string} sanitized HTML
 */
function renderMarkdownSafe(text) {
    if (!text) return '';
    const rawHtml = marked.parse(text, { breaks: true });
    return DOMPurify.sanitize(rawHtml);
}

/**
 * Escape text for safe insertion into HTML (use for plain, non-Markdown user
 * input that still needs to go through innerHTML).
 *
 * @param {string} text
 * @returns {string} HTML-escaped text
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text || '';
    return div.innerHTML;
}

/**
 * Strip common Markdown formatting markers from text, for display in plain-text
 * contexts (e.g. a <textarea>) that can't render HTML.
 *
 * @param {string} text - raw Markdown text
 * @returns {string} plain text with formatting markers removed
 */
function stripMarkdownFormatting(text) {
    if (!text) return '';
    return text
        .replace(/^#{1,6}\s+/gm, '')          // headers
        .replace(/\*\*(.*?)\*\*/g, '$1')      // bold
        .replace(/__(.*?)__/g, '$1')          // bold (underscore)
        .replace(/\*(.*?)\*/g, '$1')          // italic
        .replace(/_(.*?)_/g, '$1')            // italic (underscore)
        .replace(/^\s*[-*]\s+/gm, '• ')       // bullet lists -> simple bullet
        .trim();
}
