document.addEventListener("DOMContentLoaded", () => {
  const statsGrid = document.getElementById("stats-grid");
  const histList = document.getElementById("hist-list");
  const favList = document.getElementById("fav-list");
  const filterInput = document.getElementById("hist-filter");

  function renderStats() {
    const stats = OSP.Storage.getStats();
    const tipoTop = Object.entries(stats.por_tipo).sort((a, b) => b[1] - a[1])[0];
    const motorTop = Object.entries(stats.por_motor).sort((a, b) => b[1] - a[1])[0];
    const cards = [
      { label: "Búsquedas realizadas", value: stats.total_busquedas },
      { label: "Tipo más consultado", value: tipoTop ? tipoTop[0] : "—" },
      { label: "Motor más usado", value: motorTop ? motorTop[0] : "—" },
      { label: "Tiempo acumulado", value: stats.tiempo_total_seg.toFixed(1) + "s" },
    ];
    statsGrid.innerHTML = cards
      .map(
        (c) => `<div class="panel stat-card">
          <div class="stat-value">${OSP.Render.esc(c.value)}</div>
          <div class="stat-label">${OSP.Render.esc(c.label)}</div>
        </div>`
      )
      .join("");
  }

  function itemRow(item, isFav) {
    const fav = OSP.Storage.isFavorite(item.consulta, item.tipo);
    return `<div class="result-item" style="display:flex;align-items:center;justify-content:space-between;gap:12px;">
      <div>
        ${OSP.Render.badge(item.tipo_label || item.tipo || "—", "info")}
        <span style="margin-left:8px;font-family:var(--font-mono);">${OSP.Render.esc(item.consulta)}</span>
        <div class="text-dim" style="font-size:11.5px;margin-top:4px;">${new Date(item.fecha).toLocaleString()} · ${OSP.Render.esc(item.seccion || "")}</div>
      </div>
      <div style="display:flex;gap:6px;flex:none;">
        <button class="btn sm ghost fav-btn" data-consulta="${OSP.Render.esc(item.consulta)}" data-tipo="${OSP.Render.esc(item.tipo)}">${fav ? "★" : "☆"}</button>
        ${!isFav ? `<button class="btn sm ghost del-btn" data-id="${item.id}">Eliminar</button>` : ""}
      </div>
    </div>`;
  }

  function renderHistory(filter = "") {
    let items = OSP.Storage.getHistory();
    if (filter) {
      const f = filter.toLowerCase();
      items = items.filter(
        (i) => i.consulta.toLowerCase().includes(f) || (i.tipo_label || "").toLowerCase().includes(f)
      );
    }
    histList.innerHTML = items.length
      ? items.map((i) => itemRow(i, false)).join("")
      : OSP.Render.emptyState("", "Aún no hay búsquedas registradas.");

    histList.querySelectorAll(".del-btn").forEach((b) =>
      b.addEventListener("click", () => {
        OSP.Storage.removeHistoryItem(b.dataset.id);
        renderHistory(filterInput.value);
      })
    );
    bindFavButtons(histList);
  }

  function renderFavorites() {
    const favs = OSP.Storage.getFavorites();
    favList.innerHTML = favs.length
      ? favs.map((f) => itemRow(f, true)).join("")
      : OSP.Render.emptyState("", "No has guardado ningún favorito todavía.");
    bindFavButtons(favList);
  }

  function bindFavButtons(scope) {
    scope.querySelectorAll(".fav-btn").forEach((b) =>
      b.addEventListener("click", () => {
        OSP.Storage.toggleFavorite({ consulta: b.dataset.consulta, tipo: b.dataset.tipo, tipo_label: b.dataset.tipo });
        renderHistory(filterInput.value);
        renderFavorites();
      })
    );
  }

  filterInput.addEventListener("input", () => renderHistory(filterInput.value));

  document.getElementById("hist-clear").addEventListener("click", () => {
    if (confirm("¿Vaciar todo el historial? Esta acción no se puede deshacer.")) {
      OSP.Storage.clearHistory();
      renderHistory();
    }
  });

  renderStats();
  renderHistory();
  renderFavorites();

  // Si llega ?tab=favoritos, activa esa pestaña
  if (new URLSearchParams(window.location.search).get("tab") === "favoritos") {
    document.querySelector('.tab-btn[data-tab-target="favoritos"]').click();
  }
});
