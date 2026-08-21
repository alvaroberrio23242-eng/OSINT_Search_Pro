document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("hero-search-form");
  if (!form) return;

  const input = document.getElementById("hero-query");
  const typeLive = document.getElementById("type-live");
  const resultsWrap = document.getElementById("hero-results");
  const engineChips = () =>
    Array.from(document.querySelectorAll('#engine-picker input[type="checkbox"]:checked')).map(
      (i) => i.value
    );

  let detectTimer;
  input.addEventListener("input", () => {
    clearTimeout(detectTimer);
    const val = input.value.trim();
    if (!val) {
      typeLive.innerHTML = "";
      return;
    }
    detectTimer = setTimeout(async () => {
      try {
        const tipo = await OSP.Api.detect(val);
        typeLive.innerHTML = `Detectado como <strong>${OSP.Render.esc(tipo.label)}</strong> — pulsa Buscar o ve directo a la sección especializada.`;
      } catch (e) {
        typeLive.innerHTML = "";
      }
    }, 250);
  });

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const consulta = input.value.trim();
    if (!consulta) return;

    const motores = engineChips();
    resultsWrap.hidden = false;
    resultsWrap.innerHTML = `<div class="panel bracketed fade-in">${OSP.Render.skeleton(5)}</div>`;
    resultsWrap.scrollIntoView({ behavior: "smooth", block: "start" });

    try {
      const data = await OSP.Api.search(consulta, motores.length ? motores : null);
      renderResultados(data);
    } catch (err) {
      resultsWrap.innerHTML = `<div class="panel bracketed">${OSP.Render.emptyState("", "Error al buscar: " + err.message)}</div>`;
    }
  });

  function renderResultados(data) {
    const cabecera = `
      <div class="panel-head">
        <h3 class="panel-title"><span class="sq"></span>Resultados — "${OSP.Render.esc(data.consulta)}"</h3>
        <div style="display:flex;gap:8px;">
          ${OSP.Render.badge(data.tipo.label, "info")}
          ${OSP.Render.badge(data.total_resultados + " resultados", "ok")}
          ${OSP.Render.badge(data.duracion_seg + "s", "warn")}
        </div>
      </div>`;

    const bloques = data.motores
      .map((m) => {
        if (!m.ok) {
          return `<div class="panel" style="margin-bottom:14px;">
            <div class="panel-head"><h3 class="panel-title">${OSP.Render.esc(m.motor)}</h3>${OSP.Render.badge("sin respuesta", "error")}</div>
            <p class="text-dim">No se pudieron obtener resultados de este motor ahora mismo (${OSP.Render.esc(m.error || "error desconocido")}).</p>
          </div>`;
        }
        if (!m.resultados.length) {
          return `<div class="panel" style="margin-bottom:14px;">
            <div class="panel-head"><h3 class="panel-title">${OSP.Render.esc(m.motor)}</h3>${OSP.Render.badge("0 resultados", "warn")}</div>
          </div>`;
        }
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
        const badges = m.demo
          ? `${OSP.Render.badge(m.resultados.length + " resultados", "ok")}${OSP.Render.badge("Demostración", "warn")}`
          : OSP.Render.badge(m.resultados.length + " resultados", "ok");
        const aviso = m.demo
          ? `<p class="text-dim" style="margin:6px 0 12px;font-size:.85em;">Este motor está bloqueando las búsquedas automáticas ahora mismo (típico en hosting en la nube), así que se muestran resultados de ejemplo.</p>`
          : "";
        return `<div class="panel" style="margin-bottom:14px;">
          <div class="panel-head"><h3 class="panel-title">${OSP.Render.esc(m.motor)}</h3><div style="display:flex;gap:8px;">${badges}</div></div>
          ${aviso}${items}
        </div>`;
      })
      .join("");

    resultsWrap.innerHTML = `<div class="panel bracketed fade-in">${cabecera}</div><div class="fade-in" style="margin-top:16px;">${bloques}</div>`;
  }
});
