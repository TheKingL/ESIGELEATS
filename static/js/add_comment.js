document.addEventListener("DOMContentLoaded", () => {
  const section = document.getElementById("comments-section");
  if (!section) return;

  const listEl = section.querySelector("#comments-list");
  const countEl = section.querySelector("#comments-count");
  const emptyEl = section.querySelector("#comments-empty");
  const formEl = section.querySelector("#comment-form");
  const textareaEl = section.querySelector("#comment-content");
  const errorEl = section.querySelector("#comment-error");

  const commentsUrl = section.dataset.commentsUrl;
  const postUrl = section.dataset.postUrl;

  if (!listEl || !commentsUrl) return;

  function updateCount() {
    const count = listEl.children.length;
    if (countEl) {
      countEl.textContent = count + " commentaire" + (count > 1 ? "s" : "");
    }
    if (emptyEl) {
      if (count === 0) {
        emptyEl.classList.remove("hidden");
      } else {
        emptyEl.classList.add("hidden");
      }
    }
  }

  function roleBadge(user) {
    if (user.is_admin) {
      return `
        <span class="inline-flex items-center gap-1 rounded-full bg-rose-100 px-2 py-0.5 text-[10px] font-semibold text-rose-700 dark:bg-rose-900/50 dark:text-rose-300">
          <i class="fa-solid fa-shield-halved text-[9px]"></i>
          Admin
        </span>
      `;
    }
    if (user.is_profile_public) {
      return `
        <span class="inline-flex items-center gap-1 rounded-full bg-emerald-100 px-2 py-0.5 text-[10px] font-semibold text-emerald-700 dark:bg-emerald-900/50 dark:text-emerald-300">
          Public
        </span>
      `;
    }
    return `
      <span class="inline-flex items-center gap-1 rounded-full bg-amber-100 px-2 py-0.5 text-[10px] font-semibold text-amber-700 dark:bg-amber-900/50 dark:text-amber-300">
        Privé
      </span>
    `;
  }

  function avatarInitial(user) {
    const base = user.display_name || user.username || "?";
    return base.trim().charAt(0).toUpperCase();
  }

  function formatDateLabel(raw) {
    if (!raw) return "";
    return raw;
  }

  function createCommentElement(comment) {
    const user = comment.user || {};
    const el = document.createElement("article");

    el.className =
      "rounded-2xl border border-primary-50 bg-surface-light px-3 py-3 text-sm shadow-sm " +
      "dark:border-primary-800/60 dark:bg-surface-dark";

    el.innerHTML = `
      <div class="flex items-start gap-3">
        <a href="/users/${user.id || ""}"
           class="flex h-9 w-9 flex-shrink-0 items-center justify-center rounded-full bg-primary-100 text-xs font-semibold text-primary-700 dark:bg-primary-800/60 dark:text-primary-50">
          ${avatarInitial(user)}
        </a>

        <div class="flex-1 space-y-1">
          <div class="flex flex-wrap items-center justify-between gap-1">
            <div class="flex flex-wrap items-center gap-2">
              <a href="/users/${user.id || ""}"
                 class="text-xs font-semibold text-ink dark:text-ink-inverted hover:text-primary-700 dark:hover:text-primary-100">
                ${user.display_name || user.username || "Utilisateur"}
              </a>
              <span class="text-[11px] text-ink-soft dark:text-ink-lighter">
                @${user.username || "?"}
              </span>
              ${roleBadge(user)}
            </div>
            <span class="text-[10px] text-ink-soft dark:text-ink-lighter">
              ${formatDateLabel(comment.created_at)}
            </span>
          </div>

          <p class="text-xs leading-relaxed text-ink dark:text-ink-inverted">
            ${comment.content.replace(/</g, "&lt;").replace(/>/g, "&gt;")}
          </p>
        </div>
      </div>
    `;

    return el;
  }

  function renderComments(comments) {
    listEl.innerHTML = "";
    comments.forEach((c) => {
      listEl.appendChild(createCommentElement(c));
    });
    updateCount();
  }

  function appendComment(comment) {
    listEl.appendChild(createCommentElement(comment));
    updateCount();
  }

  function loadComments() {
    fetch(commentsUrl, {
      headers: { "X-Requested-With": "XMLHttpRequest" },
    })
      .then((res) => {
        if (res.status === 401) {
          window.location.href = "/login";
          return null;
        }
        if (res.status === 403) {
          window.location.href = "/";
          return null;
        }
        return res.json();
      })
      .then((data) => {
        if (!data) return;
        renderComments(data);
      })
      .catch((err) => {
        console.error("Erreur chargement commentaires:", err);
      });
  }

  if (formEl && textareaEl && postUrl) {
    formEl.addEventListener("submit", (e) => {
      e.preventDefault();
      if (errorEl) {
        errorEl.classList.add("hidden");
        errorEl.textContent = "";
      }

      const content = (textareaEl.value || "").trim();
      if (!content) {
        if (errorEl) {
          errorEl.textContent =
            "Ton commentaire est vide. Dis-nous au moins si c’était bon !";
          errorEl.classList.remove("hidden");
        }
        return;
      }

      fetch(postUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-Requested-With": "XMLHttpRequest",
        },
        body: JSON.stringify({ content }),
      })
        .then((res) => {
          if (res.status === 401) {
            window.location.href = "/login";
            return null;
          }
          if (res.status === 403) {
            window.location.href = "/";
            return null;
          }
          return res.json().then((data) => ({ status: res.status, data }));
        })
        .then((result) => {
          if (!result) return;
          const { status, data } = result;

          if (status >= 400 || data.error) {
            if (errorEl) {
              errorEl.textContent = data.error || "Une erreur est survenue.";
              errorEl.classList.remove("hidden");
            }
            return;
          }

          textareaEl.value = "";
          appendComment(data);
        })
        .catch((err) => {
          console.error("Erreur ajout commentaire:", err);
          if (errorEl) {
            errorEl.textContent = "Impossible d’envoyer le commentaire.";
            errorEl.classList.remove("hidden");
          }
        });
    });
  }

  loadComments();
});
