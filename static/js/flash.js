(function () {
  /**
   * Affiche un toast dans #flash-container
   * @param {string} message - texte du toast
   * @param {"success"|"error"|"warning"|"info"|"danger"} [category="info"]
   */
  function showFlash(message, category) {
    if (!message) return;

    const container = document.getElementById("flash-container");
    if (!container) return;

    let cat = (category || "info").toLowerCase();
    if (cat === "danger") cat = "error";

    const wrapper = document.createElement("div");
    wrapper.className =
      "flash-message toast pointer-events-auto flex w-full max-w-xs justify-center items-center gap-3 " +
      "rounded-lg border border-primary-100 bg-surface-soft px-4 py-3 text-sm text-ink shadow-lg " +
      "opacity-0 transition-opacity duration-200 " +
      "dark:border-primary-700/60 dark:bg-surface-dark dark:text-ink-inverted";

    let badgeClasses = "";
    let iconClass = "";

    if (cat === "success") {
      badgeClasses =
        "flex h-7 w-7 items-center justify-center rounded-full " +
        "bg-emerald-600 text-emerald-50 " +
        "dark:bg-emerald-900/40 dark:text-emerald-300";
      iconClass = "fa-solid fa-check text-xs";
    } else if (cat === "error") {
      badgeClasses =
        "flex h-7 w-7 items-center justify-center rounded-full " +
        "bg-rose-600 text-rose-50 " +
        "dark:bg-rose-900/40 dark:text-rose-300";
      iconClass = "fa-solid fa-xmark text-xs";
    } else {
      badgeClasses =
        "flex h-7 w-7 items-center justify-center rounded-full " +
        "bg-amber-600 text-amber-50 " +
        "dark:bg-amber-900/40 dark:text-amber-300";
      iconClass = "fa-solid fa-info text-xs";
    }

    wrapper.innerHTML = `
      <div class="mt-0.5">
        <span class="${badgeClasses}">
          <i class="${iconClass}"></i>
        </span>
      </div>
      <div class="flex-1">
        ${message}
      </div>
    `;

    container.appendChild(wrapper);

    requestAnimationFrame(() => {
      wrapper.classList.remove("opacity-0");
    });

    setTimeout(() => {
      wrapper.classList.add("opacity-0");
      setTimeout(() => wrapper.remove(), 200);
    }, 3000);
  }

  window.showFlash = showFlash;
})();
