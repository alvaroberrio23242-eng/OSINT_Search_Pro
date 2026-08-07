document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("domain-form");
  const results = document.getElementById("domain-results");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const dominio = document.getElementById("domain-input").value.trim();
    if (!dominio) return;

    results.innerHTML = `<div class="panel bracketed fade-in"><div class="loading-row"><span class="pulse-dot"></span>Consultando WHOIS, DNS y crt.sh…</div></div>`;

    try {
      const data = await OSP.Api.domain(dominio);
      OSP.Storage.addHistory({ tipo: "domain", tipo_label: "Dominio", consulta: dominio, seccion: "dominios" });

      const subdominios = data.subdominios.subdominios || [];
      const subList = subdominios.length
        ? `<div style="max-height:260px;overflow-y:auto;">${subdominios
            .map((s) => `<div class="mono" style="padding:5px 0;border-bottom:1px solid var(--line);font-size:12.5px;">${OSP.Render.esc(s)}</div>`)
            .join("")}</div>`
        : `<p class="text-dim">${OSP.Render.esc(data.subdominios.nota || data.subdominios.error || "No se encontraron subdominios.")}</p>`;

      results.innerHTML = `
        <div class="grid cols-2 stagger">
          <div class="panel bracketed">
            <div class="panel-head"><h3 class="panel-title"><span class="sq"></span>WHOIS</h3></div>
            ${OSP.Render.kvTable(data.whois)}
          </div>
          <div class="panel bracketed">
            <div class="panel-head"><h3 class="panel-title"><span class="sq"></span>Registros DNS</h3></div>
            ${OSP.Render.kvTable(data.dns)}
          </div>
          <div class="panel bracketed" style="grid-column:1 / -1;">
            <div class="panel-head"><h3 class="panel-title"><span class="sq"></span>Subdominios (Certificate Transparency)</h3>${OSP.Render.badge((data.subdominios.total || 0) + " encontrados", "ok")}</div>
            ${subList}
          </div>
        </div>`;
    } catch (err) {
      results.innerHTML = `<div class="panel bracketed">${OSP.Render.emptyState("", "Error: " + err.message)}</div>`;
    }
  });
});
