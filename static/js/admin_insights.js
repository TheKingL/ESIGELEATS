document.addEventListener("DOMContentLoaded", function () {
  if (typeof ApexCharts === "undefined") {
    console.warn("ApexCharts non chargé.");
    return;
  }

  const style = document.createElement("style");
  style.innerHTML = `
    .dark .apexcharts-tooltip {
      background-color: #1e293b !important;
      border-color: #334155 !important;
      color: #f8fafc !important;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
    }
    .dark .apexcharts-tooltip-title {
      background-color: #0f172a !important;
      border-bottom: 1px solid #334155 !important;
      font-family: inherit !important;
    }
    .dark .apexcharts-text {
      fill: #cbd5e1 !important;
    }
  `;
  document.head.appendChild(style);

  const endpoint = window.ADMIN_STATS_ENDPOINT || "/api/admin/stats/overview";

  const COLORS = {
    approved: "#10B981",
    pending: "#F59E0B",
    changes: "#F97316",
    rejected: "#EF4444",
    primary: "#6366F1",
    secondary: "#EC4899",
    tertiary: "#8B5CF6",
    quaternary: "#06B6D4",
    textLight: "#64748B",
    textDark: "#94A3B8",
  };

  function getThemeConfig() {
    const isDark = document.documentElement.classList.contains("dark");
    return {
      foreColor: isDark ? COLORS.textDark : COLORS.textLight,
      gridColor: isDark ? "#334155" : "#E2E8F0",
    };
  }

  const theme = getThemeConfig();

  const commonOptions = {
    chart: {
      foreColor: theme.foreColor,
      fontFamily: "inherit",
      toolbar: { show: false },
      zoom: { enabled: false },
      parentHeightOffset: 0,
    },
    grid: {
      borderColor: theme.gridColor,
      strokeDashArray: 4,
      padding: { top: 0, right: 20, bottom: 15, left: 15 },
    },
    dataLabels: { enabled: false },
    tooltip: {
      theme: document.documentElement.classList.contains("dark")
        ? "dark"
        : "light",
    },
  };

  function safeText(id, value) {
    const el = document.getElementById(id);
    if (!el) return;
    el.textContent = value;
  }

  function formatNumber(n) {
    if (n === null || typeof n === "undefined") return "—";
    return new Intl.NumberFormat("fr-FR").format(n);
  }

  function buildStatusChart(statusCounts) {
    const el = document.getElementById("chart-status");
    if (!el) return;

    const series = [
      statusCounts.APPROVED || 0,
      statusCounts.PENDING || 0,
      statusCounts.CHANGES_REQUIRED || 0,
      statusCounts.REJECTED || 0,
    ];
    const labels = ["Validées", "En attente", "À modifier", "Refusées"];
    const colors = [
      COLORS.approved,
      COLORS.pending,
      COLORS.changes,
      COLORS.rejected,
    ];

    const options = {
      chart: {
        type: "donut",
        height: "100%",
        foreColor: theme.foreColor,
        fontFamily: "inherit",
        toolbar: { show: false },
      },
      series: series,
      labels: labels,
      colors: colors,
      legend: {
        position: "top",
        itemMargin: { horizontal: 5, vertical: 0 },
      },
      dataLabels: { enabled: true },
      stroke: { width: 1 },
      plotOptions: {
        pie: {
          customScale: 0.9,
          donut: {
            size: "65%",
          },
        },
      },
      grid: {
        ...commonOptions.grid,
        padding: { bottom: 15 },
      },
    };

    new ApexCharts(el, options).render();
  }

  function buildRecipesByDayChart(recipesByDay) {
    const el = document.getElementById("chart-recipes-by-day");
    if (!el) return;

    const labels = recipesByDay.labels || [];
    const created = recipesByDay.created || [];
    const approved = recipesByDay.approved || [];

    const options = {
      ...commonOptions,
      chart: {
        type: "area",
        height: "100%",
        toolbar: { show: false },
        foreColor: theme.foreColor,
        parentHeightOffset: 0,
      },
      colors: [COLORS.quaternary, COLORS.approved],
      series: [
        { name: "Créées", data: created },
        { name: "Validées", data: approved },
      ],
      stroke: { curve: "smooth", width: 3 },
      xaxis: {
        categories: labels,
        labels: { rotate: -45, style: { fontSize: "10px" } },
        axisBorder: { show: false },
        axisTicks: { show: false },
      },
      legend: { position: "top", horizontalAlign: "right" },
    };

    new ApexCharts(el, options).render();
  }

  function buildRatingDistributionChart(ratingDist) {
    const el = document.getElementById("chart-rating-distribution");
    if (!el) return;

    const categories = ratingDist.ratings || [1, 2, 3, 4, 5];
    const counts = ratingDist.counts || [0, 0, 0, 0, 0];

    const options = {
      ...commonOptions,
      chart: {
        type: "bar",
        height: "100%",
        foreColor: theme.foreColor,
        parentHeightOffset: 0,
      },
      colors: [
        COLORS.rejected,
        "#F87171",
        "#FBBF24",
        "#34D399",
        COLORS.approved,
      ],
      plotOptions: {
        bar: {
          columnWidth: "50%",
          borderRadius: 4,
          distributed: true,
        },
      },
      series: [{ name: "Avis", data: counts }],
      xaxis: {
        categories: categories.map(String),
        labels: { style: { fontSize: "12px" } },
      },
      legend: { show: false },
    };

    new ApexCharts(el, options).render();
  }

  function buildTopAuthorsChart(topAuthors) {
    const el = document.getElementById("chart-top-authors");
    if (!el) return;

    if (!Array.isArray(topAuthors) || topAuthors.length === 0) {
      el.innerHTML =
        '<div class="h-full flex items-center justify-center text-sm text-gray-400">Pas assez de données</div>';
      return;
    }

    const labels = topAuthors.map((a) => a.label);
    const counts = topAuthors.map((a) => a.recipe_count);

    const options = {
      ...commonOptions,
      chart: {
        type: "bar",
        height: "100%",
        foreColor: theme.foreColor,
        parentHeightOffset: 0,
      },
      colors: [COLORS.primary],
      plotOptions: {
        bar: {
          horizontal: true,
          barHeight: "50%",
          borderRadius: 4,
        },
      },
      grid: {
        ...commonOptions.grid,
        padding: { top: 0, right: 20, bottom: 15, left: 10 },
      },
      series: [{ name: "Recettes", data: counts }],
      xaxis: {
        categories: labels,
      },
    };

    new ApexCharts(el, options).render();
  }

  function buildTopRecipesChart(topRecipes) {
    const el = document.getElementById("chart-top-recipes");
    if (!el) return;

    if (!Array.isArray(topRecipes) || topRecipes.length === 0) {
      el.innerHTML =
        '<div class="h-full flex items-center justify-center text-sm text-gray-400">Pas assez de données</div>';
      return;
    }

    const labels = topRecipes.map((r) => r.title);
    const favorites = topRecipes.map((r) => r.favorites || 0);
    const comments = topRecipes.map((r) => r.comments || 0);

    const options = {
      ...commonOptions,
      chart: {
        type: "bar",
        height: "100%",
        foreColor: theme.foreColor,
        parentHeightOffset: 0,
      },
      colors: [COLORS.secondary, COLORS.tertiary],
      plotOptions: {
        bar: {
          columnWidth: "60%",
          borderRadius: 4,
        },
      },
      grid: {
        ...commonOptions.grid,
        padding: { top: 0, right: 25, bottom: 15, left: 25 },
      },
      series: [
        { name: "Favoris", data: favorites },
        { name: "Commentaires", data: comments },
      ],
      xaxis: {
        categories: labels,
        labels: {
          style: { fontSize: "11px" },
          trim: true,
          rotate: -15,
        },
      },
      legend: { position: "top" },
    };

    new ApexCharts(el, options).render();
  }

  function renderStats(data) {
    const kpis = data.kpis || {};
    safeText("kpi-total-recipes", formatNumber(kpis.total_recipes));
    safeText("kpi-pending-recipes", formatNumber(kpis.pending_recipes));
    safeText(
      "kpi-changes-required",
      formatNumber(kpis.changes_required_recipes)
    );
    safeText("kpi-rejected-recipes", formatNumber(kpis.rejected_recipes));
    safeText("kpi-total-users", formatNumber(kpis.total_users));
    safeText("kpi-total-ratings", formatNumber(kpis.total_ratings));
    safeText("kpi-total-favorites", formatNumber(kpis.total_favorites));
    safeText("kpi-total-comments", formatNumber(kpis.total_comments));

    buildStatusChart(data.status_counts || {});
    buildRecipesByDayChart(data.recipes_by_day || {});
    buildRatingDistributionChart(data.rating_distribution || {});
    buildTopAuthorsChart(data.top_authors || []);
    buildTopRecipesChart(data.top_recipes_engagement || []);
  }

  function fetchStats() {
    fetch(endpoint, { headers: { "X-Requested-With": "XMLHttpRequest" } })
      .then((res) => (res.status === 200 ? res.json() : null))
      .then((data) => {
        if (data && !data.error) renderStats(data);
      })
      .catch((err) => console.error(err));
  }

  fetchStats();
});
