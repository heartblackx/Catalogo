from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')
marker = 'CATALOGO_V40_APPOINTMENT_TRUST'
if marker in text:
    print('V40 already installed')
    raise SystemExit(0)

replacements = [
    (
        '        <h3>Agenda tu cita</h3>\n        <p>Completa estos 4 datos para solicitar tu cita. Un asesor se pondrá en contacto contigo para dar seguimiento y confirmar los detalles.</p>',
        '        <h3>Agenda una visita al terreno</h3>\n        <p>Conoce el terreno sin compromiso, revisa su ubicación y recibe información adicional directamente con un asesor. Completa estos 4 datos para solicitar tu visita.</p>\n        <div class="appointment-visit-note"><strong>Visita sin compromiso</strong><span>Agendar y conocer el terreno no te obliga a comprar ni a realizar ningún pago.</span></div>'
    ),
    (
        '<button class="appointment-submit" id="citaSubmit" type="submit">Confirmar cita</button>',
        '<button class="appointment-submit" id="citaSubmit" type="submit">Agendar visita</button>'
    ),
    ('  msg.textContent="Confirmando tu cita…";\n  btn.disabled=true;\n  btn.textContent="Confirmando…";',
     '  msg.textContent="Agendando tu visita…";\n  btn.disabled=true;\n  btn.textContent="Agendando…";'),
    ('    btn.textContent="Confirmar cita";', '    btn.textContent="Agendar visita";'),
    (
'''        <h3>Cita confirmada</h3>
        <p>Tu cita quedó registrada. Un asesor se pondrá en contacto contigo para dar seguimiento y confirmar los detalles.</p>
        <div class="success-details">''',
'''        <h3>Visita registrada</h3>
        <p>Tu visita quedó registrada. Un asesor se pondrá en contacto contigo para confirmar la hora, acompañarte a conocer el terreno y resolver cualquier duda, sin compromiso de compra.</p>
        <div class="success-details">'''
    ),
    (
'''        </div>
        <button class="success-close" onclick="closeQuoteModal()">Cerrar</button>
      </div>`;''',
'''        </div>
        <div class="appointment-trust">
          <div class="appointment-trust-head"><span>🛡️</span><div><small>Tu seguridad es primero</small><strong>Compra y aparta con un proceso claro</strong></div></div>
          <p><b>Todos los acuerdos, contratos y trámites se formalizan en oficinas de Vive La Baja.</b> La visita al terreno es informativa y no te obliga a entregar dinero.</p>
          <div class="appointment-trust-list">
            <div><b>1</b><span>Si decides apartar o dar enganche durante la visita, hazlo <strong>únicamente por transferencia</strong> dentro del proceso que tu asesor te confirme.</span></div>
            <div><b>2</b><span>Antes de transferir, confirma con tu asesor el <strong>concepto, monto y cuenta receptora</strong>. No entregues efectivo en campo.</span></div>
            <div><b>3</b><span>Conserva tu comprobante y solicita tu <strong>recibo de pago el mismo día</strong> o, como máximo, dentro de las siguientes 48 horas.</span></div>
            <div><b>4</b><span>Si este desarrollo permite un <strong>apartado desde $200 USD</strong>, tu asesor te lo indicará antes de cualquier transferencia y te explicará los pasos a seguir.</span></div>
          </div>
          <p class="appointment-trust-foot">Ante cualquier duda, consulta a tu asesor antes de pagar. Tu asesor debe explicarte el proceso, los documentos y dónde se formaliza cada trámite.</p>
        </div>
        <button class="success-close" onclick="closeQuoteModal()">Cerrar</button>
      </div>`;'''
    ),
]

for old, new in replacements:
    if old not in text:
        raise SystemExit(f'Expected pattern not found: {old[:80]!r}')
    text = text.replace(old, new, 1)

# Remove the external interactive-plan button from the official SVG controls.
old_external = '''    const external=document.createElement("a");external.href="https://gcmaps.grupoconcordia.info/";external.target="_blank";external.rel="noopener noreferrer";external.textContent="Plano interactivo ↗";
    const src=document.createElement("span");src.className="quote-plan-source";src.textContent=`Plano: ${source}`;
    localBtn.onclick=()=>{svg.setAttribute("viewBox",local);localBtn.classList.add("active");fullBtn.classList.remove("active")};
    fullBtn.onclick=()=>{svg.setAttribute("viewBox",original.raw);fullBtn.classList.add("active");localBtn.classList.remove("active")};
    tools.append(localBtn,fullBtn,external,src);section.appendChild(tools);'''
new_external = '''    const src=document.createElement("span");src.className="quote-plan-source";src.textContent=`Plano: ${source}`;
    localBtn.onclick=()=>{svg.setAttribute("viewBox",local);localBtn.classList.add("active");fullBtn.classList.remove("active")};
    fullBtn.onclick=()=>{svg.setAttribute("viewBox",original.raw);fullBtn.classList.add("active");localBtn.classList.remove("active")};
    tools.append(localBtn,fullBtn,src);section.appendChild(tools);'''
if old_external not in text:
    raise SystemExit('Interactive-plan control block not found')
text = text.replace(old_external, new_external, 1)

styles = r'''

<!-- CATALOGO_V40_APPOINTMENT_TRUST -->
<style id="catalogo-v40-appointment-trust-style">
  .appointment-visit-note{
    margin:16px 0 18px;padding:14px 15px;border:1px solid rgba(102,224,215,.22);border-radius:16px;
    background:rgba(104,224,214,.09);color:#d9f1f1
  }
  .appointment-visit-note strong{display:block;margin-bottom:4px;color:#7be2d9;font-size:.86rem}
  .appointment-visit-note span{display:block;font-size:.78rem;line-height:1.5;color:#c3dfe0}
  .appointment-trust{
    margin-top:18px;padding:18px;border-radius:20px;background:linear-gradient(145deg,#f2fbf9,#e8f5f3);
    border:1px solid rgba(11,89,104,.13);color:#24454f;text-align:left
  }
  .appointment-trust-head{display:flex;align-items:center;gap:11px;margin-bottom:12px}
  .appointment-trust-head>span{width:42px;height:42px;display:grid;place-items:center;border-radius:14px;background:#0b5968;font-size:1.15rem}
  .appointment-trust-head small{display:block;color:#0b6f78;font-size:.67rem;font-weight:950;letter-spacing:.09em;text-transform:uppercase}
  .appointment-trust-head strong{display:block;margin-top:2px;color:#173b46;font-size:.96rem}
  .appointment-trust>p{margin:0 0 13px;font-size:.79rem;line-height:1.55;color:#53686f}
  .appointment-trust>p b{color:#173b46}
  .appointment-trust-list{display:grid;gap:9px}
  .appointment-trust-list>div{display:grid;grid-template-columns:28px 1fr;gap:9px;align-items:start;padding:10px 11px;border-radius:13px;background:#fff;border:1px solid rgba(11,89,104,.08)}
  .appointment-trust-list>div>b{width:28px;height:28px;display:grid;place-items:center;border-radius:9px;background:#0b5968;color:#fff;font-size:.75rem}
  .appointment-trust-list span{font-size:.75rem;line-height:1.5;color:#52676f}
  .appointment-trust-list strong{color:#193e49}
  .appointment-trust .appointment-trust-foot{margin:12px 0 0;padding-top:11px;border-top:1px solid rgba(11,89,104,.12);font-size:.73rem;color:#60757c}
  @media(max-width:680px){
    .appointment-trust{padding:15px;border-radius:17px}
    .appointment-trust-list>div{grid-template-columns:26px 1fr;padding:9px}
    .appointment-trust-list>div>b{width:26px;height:26px}
  }
</style>
<!-- /CATALOGO_V40_APPOINTMENT_TRUST -->
'''

if '</body>' not in text:
    raise SystemExit('No </body> found')
text = text.replace('</body>', styles + '\n</body>', 1)
path.write_text(text, encoding='utf-8')
print('Installed CATALOGO_V40_APPOINTMENT_TRUST')
