document.addEventListener("DOMContentLoaded", () => {
  const $ = (id) => document.getElementById(id);

  // ---------- Base64 ----------
  $("b64-encode").addEventListener("click", async () => {
    const texto = $("b64-text").value;
    const data = await OSP.Api.tools.base64(texto, "encode");
    $("b64-out").innerHTML = `<div class="panel" style="margin-top:0;"><code class="mono" style="word-break:break-all;">${OSP.Render.esc(data.resultado)}</code></div>`;
  });
  $("b64-decode").addEventListener("click", async () => {
    const texto = $("b64-text").value;
    const data = await OSP.Api.tools.base64(texto, "decode");
    $("b64-out").innerHTML = data.ok
      ? `<div class="panel" style="margin-top:0;"><code class="mono" style="word-break:break-all;">${OSP.Render.esc(data.resultado)}</code></div>`
      : `<p class="text-dim">Error: ${OSP.Render.esc(data.error)}</p>`;
  });

  // ---------- Hash generator ----------
  $("hash-run").addEventListener("click", async () => {
    const texto = $("hash-text").value;
    const data = await OSP.Api.tools.hash(texto);
    $("hash-out").innerHTML = OSP.Render.kvTable(data);
  });

  // ---------- Hash identifier ----------
  $("hashid-run").addEventListener("click", async () => {
    const valor = $("hashid-text").value;
    const data = await OSP.Api.tools.hashIdentify(valor);
    $("hashid-out").innerHTML = OSP.Render.kvTable({
      longitud: data.longitud,
      hexadecimal: data.hex_valido ? "sí" : "no",
      posibles_algoritmos: data.posibles,
    });
  });

  // ---------- URL decoder ----------
  $("url-run").addEventListener("click", async () => {
    const texto = $("url-text").value;
    const data = await OSP.Api.tools.url(texto);
    $("url-out").innerHTML = `
      <div class="panel" style="margin-bottom:12px;"><code class="mono" style="word-break:break-all;">${OSP.Render.esc(data.decoded)}</code></div>
      ${OSP.Render.kvTable(data.partes)}`;
  });

  // ---------- QR ----------
  $("qr-run").addEventListener("click", async () => {
    const texto = $("qr-text").value;
    if (!texto) return;
    const data = await OSP.Api.tools.qr(texto, 260);
    $("qr-out").innerHTML = `<img src="${OSP.Render.esc(data.url)}" alt="QR" style="border-radius:8px;border:1px solid var(--line-strong);">`;
  });

  // ---------- Password generator ----------
  $("pw-run").addEventListener("click", async () => {
    const data = await OSP.Api.tools.password({
      longitud: parseInt($("pw-length").value || "16", 10),
      mayus: $("pw-mayus").checked,
      numeros: $("pw-numeros").checked,
      simbolos: $("pw-simbolos").checked,
    });
    $("pw-out").innerHTML = `<div class="panel" style="margin-top:0;display:flex;align-items:center;justify-content:space-between;gap:10px;">
      <code class="mono" style="font-size:15px;">${OSP.Render.esc(data.password)}</code>
      <button class="btn sm ghost" id="pw-copy">Copiar</button>
    </div>`;
    $("pw-copy").addEventListener("click", () => {
      navigator.clipboard.writeText(data.password);
      OSP.toast("Contraseña copiada", "ok");
    });
  });

  // ---------- DNS lookup ----------
  $("dns-run").addEventListener("click", async () => {
    const dominio = $("dns-text").value;
    const data = await OSP.Api.tools.dns(dominio);
    $("dns-out").innerHTML = OSP.Render.kvTable(data);
  });

  // ---------- Robots.txt ----------
  $("robots-run").addEventListener("click", async () => {
    const dominio = $("robots-text").value;
    const data = await OSP.Api.tools.robots(dominio);
    $("robots-out").innerHTML = data.ok
      ? `<div class="console" style="max-height:320px;">${OSP.Render.esc(data.contenido).split("\n").map((l) => `<div class="line" style="animation:none;opacity:1;">${l || "&nbsp;"}</div>`).join("")}</div>`
      : `<p class="text-dim">${OSP.Render.esc(data.error)}</p>`;
  });

  // ---------- HTTP headers ----------
  $("headers-run").addEventListener("click", async () => {
    const url = $("headers-text").value;
    const data = await OSP.Api.tools.headers(url);
    $("headers-out").innerHTML = data.ok
      ? OSP.Render.kvTable({ status: data.status, url_final: data.url, ...data.headers })
      : `<p class="text-dim">${OSP.Render.esc(data.error)}</p>`;
  });
});
