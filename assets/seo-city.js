(() => {
  const cfg = window.SEO_CITY_CONFIG || {};
  const endpoint = 'https://cisiancuphdkybkddwmq.supabase.co/functions/v1/catalogo-ciudad-publico';
  const grid = document.getElementById('developmentGrid');
  const status = document.getElementById('availabilityStatus');
  const counter = document.getElementById('availableCount');

  const esc = (s) => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[c]));
  const fmt = (n) => Number.isFinite(Number(n)) ? Number(n).toLocaleString('es-MX', { maximumFractionDigits: 1 }) : '—';

  async function init() {
    try {
      status.textContent = 'Consultando disponibilidad real…';
      const res = await fetch(`${endpoint}?city=${encodeURIComponent(cfg.slug)}`, { headers: { Accept: 'application/json' } });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      const rows = Array.isArray(data.developments) ? data.developments : [];

      counter.textContent = `${Number(data.total_lots || 0).toLocaleString('es-MX')} lotes disponibles`;
      status.textContent = `Disponibilidad consultada directamente del inventario registrado para ${cfg.city}.`;

      if (!rows.length) {
        grid.innerHTML = '<div class="empty">No hay desarrollos con lotes disponibles en este momento.</div>';
        return;
      }

      grid.innerHTML = rows.map((d) => {
        const range = d.min_m2 == null ? 'Superficie por consultar' : (Math.abs(Number(d.max_m2) - Number(d.min_m2)) < 0.01 ? `${fmt(d.min_m2)} m²` : `${fmt(d.min_m2)}–${fmt(d.max_m2)} m²`);
        const quoteUrl = `../?ciudad=${encodeURIComponent(cfg.city)}&desarrollo=${encodeURIComponent(d.name)}#desarrollos`;
        const mapLink = d.maps_url ? `<a class="map-link" target="_blank" rel="noopener" href="${esc(d.maps_url)}">Ver ubicación ↗</a>` : '';
        return `<article class="dev-card">
          <div class="dev-top"><span>Desarrollo</span><strong>${esc(d.name)}</strong></div>
          <div class="dev-stats">
            <div><small>Lotes disponibles</small><b>${Number(d.available_lots || 0).toLocaleString('es-MX')}</b></div>
            <div><small>Superficie</small><b>${range}</b></div>
          </div>
          ${d.address ? `<p>${esc(d.address)}</p>` : ''}
          <div class="dev-actions">${mapLink}<a class="primary" href="${quoteUrl}">Ver terrenos y cotizar →</a></div>
        </article>`;
      }).join('');
    } catch (err) {
      console.error(err);
      status.textContent = 'No fue posible consultar la disponibilidad en este momento.';
      grid.innerHTML = '<div class="empty">Puedes abrir el catálogo general para consultar la disponibilidad actualizada.<br><a class="fallback" href="../">Abrir catálogo →</a></div>';
    }
  }

  init();
})();
