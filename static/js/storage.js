/**
 * Capa de persistencia en localStorage.
 * Guarda historial de búsquedas/lookups, favoritos y estadísticas de uso reales
 * (no simuladas: se incrementan únicamente cuando ocurre una acción real).
 */
var OSP = window.OSP || {};

OSP.Storage = (() => {
  const KEYS = {
    HISTORY: "osp_history",
    FAVORITES: "osp_favorites",
    STATS: "osp_stats",
  };

  function _get(key, fallback) {
    try {
      const raw = localStorage.getItem(key);
      return raw ? JSON.parse(raw) : fallback;
    } catch (e) {
      return fallback;
    }
  }

  function _set(key, value) {
    try {
      localStorage.setItem(key, JSON.stringify(value));
    } catch (e) {
      console.warn("No se pudo guardar en localStorage", e);
    }
  }

  function getHistory() {
    return _get(KEYS.HISTORY, []);
  }

  function addHistory(entry) {
    const history = getHistory();
    history.unshift({
      id: crypto.randomUUID ? crypto.randomUUID() : String(Date.now()),
      fecha: new Date().toISOString(),
      ...entry,
    });
    _set(KEYS.HISTORY, history.slice(0, 300));
    _bumpStats(entry);
  }

  function clearHistory() {
    _set(KEYS.HISTORY, []);
  }

  function removeHistoryItem(id) {
    _set(KEYS.HISTORY, getHistory().filter((h) => h.id !== id));
  }

  function getFavorites() {
    return _get(KEYS.FAVORITES, []);
  }

  function toggleFavorite(entry) {
    const favs = getFavorites();
    const idx = favs.findIndex((f) => f.consulta === entry.consulta && f.tipo === entry.tipo);
    if (idx >= 0) {
      favs.splice(idx, 1);
    } else {
      favs.unshift({ ...entry, id: crypto.randomUUID ? crypto.randomUUID() : String(Date.now()) });
    }
    _set(KEYS.FAVORITES, favs);
    return idx < 0;
  }

  function isFavorite(consulta, tipo) {
    return getFavorites().some((f) => f.consulta === consulta && f.tipo === tipo);
  }

  function getStats() {
    return _get(KEYS.STATS, {
      total_busquedas: 0,
      por_tipo: {},
      por_motor: {},
      tiempo_total_seg: 0,
    });
  }

  function _bumpStats(entry) {
    const stats = getStats();
    stats.total_busquedas += 1;
    if (entry.tipo) {
      stats.por_tipo[entry.tipo] = (stats.por_tipo[entry.tipo] || 0) + 1;
    }
    if (Array.isArray(entry.motores)) {
      entry.motores.forEach((m) => {
        stats.por_motor[m] = (stats.por_motor[m] || 0) + 1;
      });
    }
    if (entry.duracion_seg) {
      stats.tiempo_total_seg += entry.duracion_seg;
    }
    _set(KEYS.STATS, stats);
  }

  return {
    getHistory,
    addHistory,
    clearHistory,
    removeHistoryItem,
    getFavorites,
    toggleFavorite,
    isFavorite,
    getStats,
  };
})();

window.OSP = OSP;
