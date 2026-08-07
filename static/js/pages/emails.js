document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("email-form");
  const results = document.getElementById("email-results");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const email = document.getElementById("email-input").value.trim();
    if (!email) return;

    results.innerHTML = `<div class="panel bracketed fade-in"><div class="loading-row"><span class="pulse-dot"></span>Consultando MX, DNS, Gravatar y GitHub…</div></div>`;

    try {
      const data = await OSP.Api.email(email);
      OSP.Storage.addHistory({ tipo: "email", tipo_label: "Email", consulta: email, seccion: "emails" });

      const mx = Array.isArray(data.mx)
        ? `<table class="data"><thead><tr><th>Prioridad</th><th>Servidor</th></tr></thead><tbody>${data.mx
            .map((m) => `<tr><td>${m.prioridad}</td><td>${OSP.Render.esc(m.servidor)}</td></tr>`)
            .join("")}</tbody></table>`
        : `<p class="text-dim">${OSP.Render.esc(data.mx.error || "Sin registros MX.")}</p>`;

      const gravatarImg = data.gravatar.existe
        ? `<img src="${OSP.Render.esc(data.gravatar.avatar_url)}" alt="avatar" style="width:64px;height:64px;border-radius:8px;border:1px solid var(--line-strong);">`
        : `<div class="text-dim">Sin avatar público en Gravatar.</div>`;

      const githubRows = (data.github.resultados || [])
        .map(
          (u) =>
            `<tr><td><img src="${OSP.Render.esc(u.avatar)}" style="width:22px;height:22px;border-radius:4px;vertical-align:middle;margin-right:6px;">${OSP.Render.esc(u.usuario)}</td><td><a href="${OSP.Render.esc(u.perfil)}" target="_blank" rel="noopener">${OSP.Render.esc(u.perfil)}</a></td></tr>`
        )
        .join("");

      results.innerHTML = `
        <div class="grid cols-2 stagger">
          <div class="panel bracketed">
            <div class="panel-head"><h3 class="panel-title"><span class="sq"></span>Dominio &amp; DNS</h3></div>
            ${OSP.Render.kvTable({ dominio: data.dominio, ...data.dns })}
          </div>
          <div class="panel bracketed">
            <div class="panel-head"><h3 class="panel-title"><span class="sq"></span>Registros MX</h3></div>
            ${mx}
          </div>
          <div class="panel bracketed">
            <div class="panel-head"><h3 class="panel-title"><span class="sq"></span>Gravatar</h3></div>
            <div style="display:flex;align-items:center;gap:14px;">
              ${gravatarImg}
              <div class="text-dim" style="font-family:var(--font-mono);font-size:12px;">${OSP.Render.esc(data.gravatar.hash)}</div>
            </div>
          </div>
          <div class="panel bracketed">
            <div class="panel-head"><h3 class="panel-title"><span class="sq"></span>GitHub</h3>${OSP.Render.badge((data.github.total || 0) + " coincidencias", "info")}</div>
            ${githubRows ? `<table class="data"><thead><tr><th>Usuario</th><th>Perfil</th></tr></thead><tbody>${githubRows}</tbody></table>` : `<p class="text-dim">${OSP.Render.esc(data.github.nota || "Sin coincidencias públicas.")}</p>`}
          </div>
        </div>`;
    } catch (err) {
      results.innerHTML = `<div class="panel bracketed">${OSP.Render.emptyState("", "Error: " + err.message)}</div>`;
    }
  });
});
