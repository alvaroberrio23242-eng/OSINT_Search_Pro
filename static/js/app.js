const OSP = window.OSP || {};

OSP.toast = function (mensaje, tipo = "info") {
  let holder = document.getElementById("osp-toasts");
  if (!holder) {
    holder = document.createElement("div");
    holder.id = "osp-toasts";
    holder.style.cssText =
      "position:fixed;bottom:20px;right:20px;z-index:999;display:flex;flex-direction:column;gap:8px;";
    document.body.appendChild(holder);
  }
  const el = document.createElement("div");
  const colors = { info: "var(--cyan)", ok: "var(--ok)", error: "var(--danger)" };
  el.className = "fade-in";
  el.style.cssText = `background:var(--panel-2);border:1px solid var(--line-strong);border-left:3px solid ${colors[tipo] || colors.info};padding:10px 14px;border-radius:6px;font-family:var(--font-mono);font-size:12.5px;color:var(--text-hi);box-shadow:var(--shadow-panel);max-width:320px;`;
  el.textContent = mensaje;
  holder.appendChild(el);
  setTimeout(() => el.remove(), 3800);
};

document.addEventListener("DOMContentLoaded", () => {
  // Toggle sidebar en móvil
  const toggle = document.querySelector(".menu-toggle");
  const sidebar = document.querySelector(".sidebar");
  if (toggle && sidebar) {
    toggle.addEventListener("click", () => sidebar.classList.toggle("open"));
    document.addEventListener("click", (e) => {
      if (
        sidebar.classList.contains("open") &&
        !sidebar.contains(e.target) &&
        !toggle.contains(e.target)
      ) {
        sidebar.classList.remove("open");
      }
    });
  }

  // Marca el link activo del sidebar según la ruta actual
  const path = window.location.pathname;
  document.querySelectorAll(".nav-link[data-path]").forEach((link) => {
    if (link.dataset.path === path) link.classList.add("active");
  });

  // Chips de selección (motores, opciones)
  document.querySelectorAll(".chip-select").forEach((group) => {
    group.querySelectorAll(".chip").forEach((chip) => {
      const input = chip.querySelector("input");
      const sync = () => chip.classList.toggle("checked", input.checked);
      sync();
      chip.addEventListener("click", (e) => {
        if (e.target.tagName !== "INPUT") input.checked = !input.checked;
        sync();
      });
    });
  });

  // Tabs genéricas [data-tabs] / [data-tab-target]
  document.querySelectorAll("[data-tabs]").forEach((tabGroup) => {
    const buttons = tabGroup.querySelectorAll(".tab-btn");
    buttons.forEach((btn) => {
      btn.addEventListener("click", () => {
        buttons.forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        const targetSel = btn.dataset.tabTarget;
        const scope = document.querySelector(tabGroup.dataset.tabs);
        scope.querySelectorAll("[data-tab-panel]").forEach((p) => (p.hidden = true));
        const panel = scope.querySelector(`[data-tab-panel="${targetSel}"]`);
        if (panel) panel.hidden = false;
      });
    });
  });
});

window.OSP = OSP;
