/**
 * Shared EduSense AI backend client for the frontend.
 * Include with: <script src="shared/api.js"></script> (or "../shared/api.js" from dashboard/*.html)
 */

// EduSense AI backend base URL (see ai_app/README.md to run it locally)
const EDUSENSE_API_BASE_URL = 'http://localhost:8000/api/v1';

/**
 * POST JSON to an EduSense AI backend endpoint and return the parsed response.
 * Throws an Error with a message safe to show directly to the user.
 *
 * @param {string} path - endpoint path, e.g. '/lesson-plan'
 * @param {object} body - request payload
 */
async function edusenseApiCall(path, body) {
    let response;
    try {
        response = await fetch(`${EDUSENSE_API_BASE_URL}${path}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(body)
        });
    } catch (networkError) {
        throw new Error(
            `Could not reach the EduSense AI backend at ${EDUSENSE_API_BASE_URL}. ` +
            `Make sure ai_app is running (see ai_app/README.md), and if you opened this page ` +
            `directly from disk, serve it over HTTP instead so CORS works.`
        );
    }

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Request failed (HTTP ${response.status})`);
    }

    return response.json();
}

/**
 * Show an inline status message in a page-level status element instead of alert().
 * Expects an element with the given id and a `.hidden` / visible toggle via display.
 *
 * @param {string} elementId - id of the status container element
 * @param {string} message - message to display
 * @param {'error'|'success'|'info'} type - visual style
 * @param {number} autoHideMs - if > 0, auto-hides after this many ms (0 = stays visible)
 */
function showInlineStatus(elementId, message, type = 'info', autoHideMs = 6000) {
    const el = document.getElementById(elementId);
    if (!el) {
        // Fall back so a missing status element never silently swallows an error
        if (type === 'error') {
            console.error(message);
        }
        return;
    }

    const colors = {
        error: { bg: 'rgba(239, 68, 68, 0.15)', border: '#ef4444', text: '#fca5a5' },
        success: { bg: 'rgba(34, 197, 94, 0.15)', border: '#22c55e', text: '#86efac' },
        info: { bg: 'rgba(59, 130, 246, 0.15)', border: '#3b82f6', text: '#93c5fd' }
    };
    const style = colors[type] || colors.info;

    el.textContent = message;
    el.style.display = 'block';
    el.style.background = style.bg;
    el.style.border = `1px solid ${style.border}`;
    el.style.color = style.text;
    el.style.borderRadius = '10px';
    el.style.padding = '0.75rem 1rem';
    el.style.marginTop = '0.75rem';
    el.style.marginBottom = '0.75rem';
    el.style.fontSize = '0.9rem';
    el.style.lineHeight = '1.5';

    if (el._hideTimeout) {
        clearTimeout(el._hideTimeout);
    }
    if (autoHideMs > 0) {
        el._hideTimeout = setTimeout(() => {
            el.style.display = 'none';
        }, autoHideMs);
    }
}
