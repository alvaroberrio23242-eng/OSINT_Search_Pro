var OSP = window.OSP || {};

OSP.Api = (() => {
  async function post(path, body) {
    const res = await fetch(path, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body || {}),
    });
    if (!res.ok) {
      let msg = `Error ${res.status}`;
      try {
        const data = await res.json();
        msg = data.error || msg;
      } catch (e) {}
      throw new Error(msg);
    }
    return res.json();
  }

  async function get(path) {
    const res = await fetch(path);
    if (!res.ok) throw new Error(`Error ${res.status}`);
    return res.json();
  }

  return {
    detect: (consulta) => post("/api/detect", { consulta }),
    search: (consulta, motores) => post("/api/search", { consulta, motores }),
    dorks: (consulta) => post("/api/dorks", { consulta }),
    email: (email) => post("/api/lookup/email", { email }),
    domain: (dominio) => post("/api/lookup/domain", { dominio }),
    ip: (ip, escanear_puertos = true) => post("/api/lookup/ip", { ip, escanear_puertos }),
    username: (usuario) => post("/api/lookup/username", { usuario }),
    persona: (nombre) => post("/api/lookup/persona", { nombre }),
    tools: {
      base64: (texto, modo) => post("/api/tools/base64", { texto, modo }),
      hash: (texto) => post("/api/tools/hash", { texto }),
      hashIdentify: (valor) => post("/api/tools/hash-identify", { valor }),
      url: (texto) => post("/api/tools/url", { texto }),
      password: (opts) => post("/api/tools/password", opts),
      dns: (dominio) => post("/api/tools/dns", { dominio }),
      robots: (dominio) => post("/api/tools/robots", { dominio }),
      headers: (url) => post("/api/tools/headers", { url }),
      qr: (texto, tamano) => post("/api/tools/qr", { texto, tamano }),
    },
    get,
    post,
  };
})();

window.OSP = OSP;
