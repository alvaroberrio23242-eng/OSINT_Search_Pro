document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("ip-form");
  const results = document.getElementById("ip-results");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const ip = document.getElementById("ip-input").value.trim();
    const escanear = document.getElementById("ip-scan-toggle").checked;
    if (!ip) return;

    results.innerHTML = `<div class="panel bracketed fade-in"><div class="loading-row"><span class="pulse-dot"></span>Geolocalizando${escanear ? " y escaneando puertos" : ""}…</div></div>`;

    try {
      const data = await OSP.Api.ip(ip, escanear);
      OSP.Storage.addHistory({ tipo: "ip", tipo_label: "IP", consulta: ip, seccion: "ips" });

      const geo = data.geolocalizacion || {};
      const geoTable = geo.error
        ? `<p class="text-dim">${OSP.Render.esc(geo.error)}</p>`
        : OSP.Render.kvTable({
            país: `${geo.country || "—"} (${geo.countryCode || "—"})`,
            región: geo.regionName,
            ciudad: geo.city,
            isp: geo.isp,
            organización: geo.org,
            asn: geo.as,
            reverse_dns: data.reverse_dns,
            coordenadas: geo.lat ? `${geo.lat}, ${geo.lon}` : null,
          });

      let portsBlock = `<p class="text-dim">Escaneo de puertos desactivado.</p>`;
      if (data.puertos) {
        portsBlock = `<table class="data"><thead><tr><th>Puerto</th><th>Servicio</th><th>Estado</th></tr></thead><tbody>
          ${data.puertos
            .map(
              (p) =>
                `<tr><td class="mono">${p.puerto}</td><td>${OSP.Render.esc(p.servicio)}</td><td>${
                  p.abierto ? OSP.Render.badge("Abierto", "ok") : OSP.Render.badge("Cerrado", "warn")
                }</td></tr>`
            )
            .join("")}
        </tbody></table>`;
      }

      const mapaLink = geo.lat
        ? `<a class="btn sm ghost" target="_blank" rel="noopener" href="https://www.openstreetmap.org/?mlat=${geo.lat}&mlon=${geo.lon}#map=10/${geo.lat}/${geo.lon}">Ver en el mapa ↗</a>`
        : "";

      results.innerHTML = `
        <div class="grid cols-2 stagger">
          <div class="panel bracketed">
            <div class="panel-head"><h3 class="panel-title"><span class="sq"></span>Geolocalización · ${OSP.Render.esc(ip)}</h3>${mapaLink}</div>
            ${geoTable}
          </div>
          <div class="panel bracketed">
            <div class="panel-head"><h3 class="panel-title"><span class="sq"></span>Puertos comunes</h3></div>
            ${portsBlock}
          </div>
        </div>`;
    } catch (err) {
      results.innerHTML = `<div class="panel bracketed">${OSP.Render.emptyState("", "Error: " + err.message)}</div>`;
    }
  });
});
