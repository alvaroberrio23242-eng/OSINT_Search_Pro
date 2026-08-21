document.addEventListener("DOMContentLoaded", () => {
  const personaForm = document.getElementById("persona-form");
  const personaResults = document.getElementById("persona-results");

  if (personaForm) {
    personaForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const nombre = document.getElementById("persona-input").value.trim();
      if (!nombre) return;

      personaResults.innerHTML = `<div class="panel bracketed fade-in"><div class="loading-row"><span class="pulse-dot"></span>Buscando menciones y armando enlaces…</div></div>`;

      try {
        const data = await OSP.Api.persona(nombre);
        personaResults.innerHTML = renderPersona(data);
      } catch (err) {
        personaResults.innerHTML = `<div class="panel bracketed">${OSP.Render.emptyState("", "Error: " + err.message)}</div>`;
      }
    });
  }

  function renderMenciones(menciones) {
    return menciones
      .map((m) => {
        if (!m.resultados || !m.resultados.length) {
          return `<div class="panel" style="margin-bottom:14px;">
            <div class="panel-head"><h3 class="panel-title">${OSP.Render.esc(m.motor)}</h3>${OSP.Render.badge("0 resultados", "warn")}</div>
          </div>`;
        }
        const badges = m.demo
          ? `${OSP.Render.badge(m.resultados.length + " resultados", "ok")}${OSP.Render.badge("Demostración", "warn")}`
          : OSP.Render.badge(m.resultados.length + " resultados", "ok");
        const aviso = m.demo
          ? `<p class="text-dim" style="margin:6px 0 12px;font-size:.85em;">Este motor está bloqueando las búsquedas automáticas ahora mismo, así que se muestran resultados de ejemplo.</p>`
          : "";
        const items = m.resultados
          .map((r) =>
            m.demo
              ? `<div class="result-item">
                  <div class="title" style="opacity:.75;">${OSP.Render.esc(r.titulo)}</div>
                  <div class="desc">${OSP.Render.esc(r.descripcion)}</div>
                </div>`
              : `<div class="result-item">
                  <div class="url">${OSP.Render.esc(r.url)}</div>
                  <div class="title"><a href="${OSP.Render.esc(r.url)}" target="_blank" rel="noopener">${OSP.Render.esc(r.titulo)}</a></div>
                  <div class="desc">${OSP.Render.esc(r.descripcion)}</div>
                </div>`
          )
          .join("");
        return `<div class="panel" style="margin-bottom:14px;">
          <div class="panel-head"><h3 class="panel-title">${OSP.Render.esc(m.motor)}</h3><div style="display:flex;gap:8px;">${badges}</div></div>
          ${aviso}${items}
        </div>`;
      })
      .join("");
  }

  function renderEnlaces(titulo, lista) {
    const chips = lista
      .map(
        (e) =>
          `<a href="${OSP.Render.esc(e.url)}" target="_blank" rel="noopener" class="badge" style="margin:4px 6px 4px 0;">${OSP.Render.esc(e.nombre)} ↗</a>`
      )
      .join("");
    return `<div style="margin-bottom:14px;"><div class="text-dim" style="margin-bottom:6px;font-size:.85em;">${titulo}</div>${chips}</div>`;
  }

  function renderPersona(data) {
    return `
      <div class="panel bracketed fade-in" style="margin-bottom:16px;">
        <div class="panel-head"><h3 class="panel-title"><span class="sq"></span>Menciones en la web — "${OSP.Render.esc(data.nombre)}"</h3></div>
        ${renderMenciones(data.menciones_web)}
      </div>
      <div class="panel bracketed fade-in">
        <div class="panel-head"><h3 class="panel-title"><span class="sq"></span>Enlaces directos para revisar manualmente</h3></div>
        <p class="text-dim" style="margin-bottom:14px;font-size:.85em;">${OSP.Render.esc(data.aviso)}</p>
        ${renderEnlaces("Redes profesionales / sociales", data.enlaces_dirigidos.redes_profesionales)}
        ${renderEnlaces("Educación y cursos", data.enlaces_dirigidos.educacion_cursos)}
        ${renderEnlaces("Registros legales (Colombia)", data.enlaces_dirigidos.registros_legales_co)}
      </div>`;
  }

  const form = document.getElementById("username-form");
  const results = document.getElementById("username-results");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const usuario = document.getElementById("username-input").value.trim();
    if (!usuario) return;

    results.innerHTML = `<div class="panel bracketed fade-in"><div class="loading-row"><span class="pulse-dot"></span>Consultando plataformas…</div></div>`;

    try {
      const data = await OSP.Api.username(usuario);

      const encontrados = data.plataformas.filter((p) => p.existe === true).length;
      const filas = data.plataformas
        .map((p) => {
          let estado = OSP.Render.badge("Sin verificar", "error");
          if (p.existe === true) estado = OSP.Render.badge("Encontrado", "ok");
          else if (p.existe === false) estado = OSP.Render.badge("No encontrado", "warn");
          else if (p.bloqueado) estado = OSP.Render.badge("Bloqueado por el sitio", "warn");
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
