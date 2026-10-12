/*
 * Datos para ubicar lotes dentro del plano real de cada desarrollo.
 * No agregar posiciones aproximadas. Solo usar coordenadas verificadas contra el plano oficial.
 *
 * Formato por desarrollo:
 * "lomas-del-valle": {
 *   image: "./assets/lot-plans/lomas-del-valle.webp",
 *   source: "Plano oficial",
 *   lots: {
 *     "69|1": { x: 10.2, y: 22.1, w: 3.1, h: 4.7 },
 *     "69|2": { polygon: [[10,20],[14,20],[14,25],[10,25]] }
 *   }
 * }
 *
 * x/y/w/h y los puntos del polygon se expresan como porcentaje del ancho/alto de la imagen.
 */
window.CATALOG_LOT_PLAN_DATA = window.CATALOG_LOT_PLAN_DATA || {
  version: 1,
  developments: {},
  officialInteractiveUrl: "https://gcmaps.grupoconcordia.info/"
};
