document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("username-form");
  const results = document.getElementById("username-results");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const usuario = document.getElementById("username-input").value.trim();
    if (!usuario) return;

    results.innerHTML = `<div class="panel bracketed fade-in"><div class="loading-row"><span class="pulse-dot"></span>Consultando plataformas…</div></div>`;

    try {
      const data = await OSP.Api.username(usuario);
      OSP.Storage.addHistory({ tipo: "username", tipo_label: "Usuario", consulta: usuario, seccion: "personas" });

      const encontrados = data.plataformas.filter((p) => p.existe === true).length;
      const filas = data.plataformas
        .map((p) => {
          let estado = OSP.Render.badge("Verificando error", "error");
          if (p.existe === true) estado = OSP.Render.badge("Encontrado", "ok");
          else if (p.existe === false) estado = OSP.Render.badge("No encontrado", "warn");
          return `<tr>
            <td>${OSP.Render.esc(p.plataforma)}</td>
            <td>${estado}</td>
            <td><a href="${OSP.Render.esc(p.url)}" target="_blank" rel="noopener">${OSP.Render.esc(p.url)}</a></td>
          </tr>`;
        })
        .join("");

      results.innerHTML = `
        <div class="panel bracketed fade-in">
          <div class="panel-head">
            <h3 class="panel-title"><span class="sq"></span>@${OSP.Render.esc(usuario)}</h3>
            ${OSP.Render.badge(encontrados + " / " + data.plataformas.length + " plataformas", "ok")}
          </div>
          <table class="data">
            <thead><tr><th>Plataforma</th><th>Estado</th><th>URL</th></tr></thead>
            <tbody>${filas}</tbody>
          </table>
        </div>`;
    } catch (err) {
      results.innerHTML = `<div class="panel bracketed">${OSP.Render.emptyState("", "Error: " + err.message)}</div>`;
    }
  });
});
