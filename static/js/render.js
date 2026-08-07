const OSP = window.OSP || {};

OSP.Render = (() => {
  function esc(str) {
    if (str === null || str === undefined) return "";
    return String(str)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;");
  }

  function kvTable(obj) {
    if (!obj || typeof obj !== "object") return `<p class="text-dim">Sin datos.</p>`;
    const rows = Object.entries(obj)
      .map(([k, v]) => {
        let val = v;
        if (Array.isArray(v)) val = v.length ? esc(v.join(", ")) : '<span class="text-dim">—</span>';
        else if (v && typeof v === "object") val = `<code>${esc(JSON.stringify(v))}</code>`;
        else val = v === null || v === undefined || v === "" ? '<span class="text-dim">—</span>' : esc(v);
        return `<tr><th style="width:38%">${esc(k)}</th><td>${val}</td></tr>`;
      })
      .join("");
    return `<table class="data"><tbody>${rows}</tbody></table>`;
  }

  function consoleLog(lines) {
    return `<div class="console">${lines
      .map(
        (l, i) =>
          `<div class="line" style="animation-delay:${i * 0.12}s"><span class="t">[${String(i + 1).padStart(2, "0")}]</span>${esc(l)}</div>`
      )
      .join("")}</div>`;
  }

  function badge(text, tipo = "info") {
    const cls = { ok: "ok", warn: "warn", error: "danger", info: "" }[tipo] || "";
    return `<span class="badge ${cls}"><span class="dot"></span>${esc(text)}</span>`;
  }

  function skeleton(lines = 3) {
    return Array.from({ length: lines })
      .map((_, i) => `<div class="skeleton" style="height:14px;width:${90 - i * 12}%;margin-bottom:10px;"></div>`)
      .join("");
  }

  function emptyState(icon, mensaje) {
    return `<div class="empty-state">${icon || ""}<p>${esc(mensaje)}</p></div>`;
  }

  return { esc, kvTable, consoleLog, badge, skeleton, emptyState };
})();

window.OSP = OSP;
