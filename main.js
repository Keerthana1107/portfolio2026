// Shared behaviour across all pages (currently: logout button)
document.addEventListener('DOMContentLoaded', () => {
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', async () => {
            await fetch('/logout', { method: 'POST' });
            window.location.href = '/login';
        });
    }
});
