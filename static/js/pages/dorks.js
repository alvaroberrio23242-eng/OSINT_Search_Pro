document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("dorks-form");
  const results = document.getElementById("dorks-results");

  function copyBtn(texto) {
    return `<button class="btn sm ghost copy-btn" data-copy="${OSP.Render.esc(texto)}">Copiar</button>`;
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const consulta = document.getElementById("dorks-input").value.trim();
    if (!consulta) return;

    results.innerHTML = `<div class="panel bracketed fade-in">${OSP.Render.skeleton(4)}</div>`;

    try {
      const data = await OSP.Api.dorks(consulta);

      const presets = data.presets
        .map(
          (p) => `<tr>
            <td>${OSP.Render.esc(p.nombre)}</td>
            <td class="mono">${OSP.Render.esc(p.query)}</td>
            <td>${copyBtn(p.query)}</td>
          </tr>`
        )
        .join("");

      const operadores = data.operadores
        .map(
          (o) => `<tr>
            <td class="mono">${OSP.Render.esc(o.op)}</td>
            <td class="mono">${OSP.Render.esc(o.query)}</td>
            <td class="text-dim" style="font-size:12.5px;">${OSP.Render.esc(o.descripcion)}</td>
            <td>${copyBtn(o.query)}</td>
          </tr>`
        )
        .join("");

      results.innerHTML = `
        <div class="grid cols-2 stagger">
          <div class="panel bracketed">
            <div class="panel-head"><h3 class="panel-title"><span class="sq"></span>Combinaciones sugeridas</h3></div>
            <table class="data"><thead><tr><th>Preset</th><th>Query</th><th></th></tr></thead><tbody>${presets}</tbody></table>
          </div>
          <div class="panel bracketed">
            <div class="panel-head"><h3 class="panel-title"><span class="sq"></span>Operadores individuales</h3></div>
            <table class="data"><thead><tr><th>Op.</th><th>Query</th><th>Uso</th><th></th></tr></thead><tbody>${operadores}</tbody></table>
          </div>
        </div>`;

      results.querySelectorAll(".copy-btn").forEach((btn) => {
        btn.addEventListener("click", () => {
          navigator.clipboard.writeText(btn.dataset.copy);
          OSP.toast("Dork copiado al portapapeles", "ok");
        });
      });
    } catch (err) {
      results.innerHTML = `<div class="panel bracketed">${OSP.Render.emptyState("", "Error: " + err.message)}</div>`;
    }
  });
});
