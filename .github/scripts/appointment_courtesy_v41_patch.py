from pathlib import Path

p = Path('index.html')
t = p.read_text(encoding='utf-8')
marker = 'CATALOGO_V41_APPOINTMENT_COURTESY'
if marker in t:
    print('V41 already applied')
    raise SystemExit(0)

old_note = '<div class="appointment-visit-note"><strong>Visita sin compromiso</strong><span>Agendar y conocer el terreno no te obliga a comprar ni a realizar ningún pago.</span></div>'
new_note = '<div class="appointment-visit-note"><strong>Visita sin compromiso</strong><span>Conoce el terreno y resuelve tus dudas sin compromiso. Si necesitas cambiar el día u horario, avísanos con anticipación para ayudarnos a respetar el horario de todos.</span></div>'
if old_note not in t:
    raise SystemExit('No se encontró la nota de visita V40')
t = t.replace(old_note, new_note, 1)

old_trust = '''        <div class="appointment-trust">\n          <div class="appointment-trust-head"><span>🛡️</span><div><small>Tu seguridad es primero</small><strong>Compra y aparta con un proceso claro</strong></div></div>\n          <p><b>Todos los acuerdos, contratos y trámites se formalizan en oficinas de Vive La Baja.</b> La visita al terreno es informativa y no te obliga a entregar dinero.</p>\n          <div class="appointment-trust-list">\n            <div><b>1</b><span>Si decides apartar o dar enganche durante la visita, hazlo <strong>únicamente por transferencia</strong> dentro del proceso que tu asesor te confirme.</span></div>\n            <div><b>2</b><span>Antes de transferir, confirma con tu asesor el <strong>concepto, monto y cuenta receptora</strong>. No entregues efectivo en campo.</span></div>\n            <div><b>3</b><span>Conserva tu comprobante y solicita tu <strong>recibo de pago el mismo día</strong> o, como máximo, dentro de las siguientes 48 horas.</span></div>\n            <div><b>4</b><span>Si este desarrollo permite un <strong>apartado desde $200 USD</strong>, tu asesor te lo indicará antes de cualquier transferencia y te explicará los pasos a seguir.</span></div>\n          </div>\n          <p class="appointment-trust-foot">Ante cualquier duda, consulta a tu asesor antes de pagar. Tu asesor debe explicarte el proceso, los documentos y dónde se formaliza cada trámite.</p>\n        </div>'''
new_trust = '''        <div class="appointment-trust">\n          <div class="appointment-trust-head"><span>✓</span><div><small>Proceso claro</small><strong>Atención y trámites formales</strong></div></div>\n          <p>La formalización del trámite se realiza en oficinas de <b>Vive La Baja</b>. Durante la visita puedes conocer el terreno y resolver tus dudas sin compromiso.</p>\n          <p>Si decides apartar o dar enganche, tu asesor te indicará el proceso y la transferencia correspondiente. Conserva tu comprobante y solicita tu recibo de pago el mismo día o, como máximo, dentro de las siguientes 48 horas.</p>\n          <p>En desarrollos participantes, el apartado puede iniciar desde <b>$200 USD</b>. Confirma disponibilidad y condiciones con tu asesor antes de realizar la transferencia.</p>\n        </div>\n        <div class="appointment-courtesy">\n          <strong>¿Necesitas cambiar tu visita?</strong>\n          <span>Avísanos con anticipación si no puedes asistir o necesitas otro día u horario. Así podemos liberar ese espacio para otra persona y ayudarte a que las visitas se atiendan lo más puntual posible.</span>\n        </div>'''
if old_trust not in t:
    raise SystemExit('No se encontró el bloque de confianza V40')
t = t.replace(old_trust, new_trust, 1)

style = '''\n\n<!-- CATALOGO_V41_APPOINTMENT_COURTESY -->\n<style id="catalogo-v41-appointment-courtesy-style">\n  .appointment-courtesy{\n    margin-top:12px;padding:14px 15px;border-radius:16px;background:#fff;border:1px solid rgba(11,89,104,.11);\n    color:#50656c;text-align:left\n  }\n  .appointment-courtesy strong{display:block;margin-bottom:4px;color:#173b46;font-size:.86rem}\n  .appointment-courtesy span{display:block;font-size:.78rem;line-height:1.5}\n  .appointment-trust{padding:16px}\n  .appointment-trust>p{margin:0 0 9px}\n  .appointment-trust>p:last-child{margin-bottom:0}\n</style>\n<!-- /CATALOGO_V41_APPOINTMENT_COURTESY -->\n'''
if '</body>' not in t:
    raise SystemExit('No se encontró </body>')
t = t.replace('</body>', style + '\n</body>', 1)

p.write_text(t, encoding='utf-8')
print('V41 patch applied')
