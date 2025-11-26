document.addEventListener("DOMContentLoaded", () => {
  const ENDPOINT = "/api/notifications/counters";

  function updateBadge(target, count) {
    const els = document.querySelectorAll(`[data-notif-target="${target}"]`);
    els.forEach((el) => {
      if (!el) return;

      if (!count || count <= 0) {
        el.classList.add("hidden");
        el.textContent = "";
        return;
      }

      el.classList.remove("hidden");
      el.textContent = count > 9 ? "9+" : String(count);
    });
  }

  function refreshNotifications() {
    fetch(ENDPOINT, {
      headers: { "X-Requested-With": "XMLHttpRequest" },
    })
      .then((res) => {
        if (res.status === 401) return null;
        return res.json();
      })
      .then((data) => {
        if (!data) return;
        updateBadge("changes-required", data.changes_required || 0);
        updateBadge("admin-pending", data.pending_recipes || 0);
      })
      .catch((err) => {
        console.error("Erreur notifications:", err);
      });
  }

  window.refreshNotifications = refreshNotifications;

  refreshNotifications();
  setInterval(refreshNotifications, 30000);
});
