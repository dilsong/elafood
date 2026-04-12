import urllib.parse

from modules.i18n import tr
from modules.menu_semana import etiqueta_dia
from modules.productos import es_comida_lunch_o_rapida_por_nombre


def _nombre_linea_pedido(item: dict) -> str:
    producto = item["producto"]
    dia = item.get("dia")
    if dia and es_comida_lunch_o_rapida_por_nombre(producto):
        return f"{etiqueta_dia(dia)} — {producto}"
    return producto


def generar_mensaje(carrito, total, cliente):
    mensaje = tr("Pedido ElaFood:\n\n", "ElaFood Order:\n\n")

    mensaje += f"{tr('Cliente', 'Customer')}: {cliente['nombre']}\n"
    mensaje += f"{tr('Teléfono', 'Phone')}: {cliente['telefono']}\n"
    mensaje += f"{tr('Dirección', 'Address')}: {cliente['direccion']}\n"
    mensaje += f"{tr('Notas', 'Notes')}: {cliente['notas']}\n\n"

    for item in carrito:
        nombre = _nombre_linea_pedido(item)
        linea = f"- {item['cantidad']} x {nombre} = ${item['precio'] * item['cantidad']}"
        mensaje += linea + "\n"

    mensaje += f"\n{tr('Total', 'Total')}: ${total}"
    return mensaje


def _truncar_texto_para_url(texto: str, base_url: str, max_total: int = 7000) -> str:
    """Evita URLs tan largas que el navegador o WhatsApp las ignore."""
    t = texto or ""
    while len(base_url + urllib.parse.quote(t, safe="")) > max_total and len(t) > 80:
        t = t[:-120].rstrip() + "\n[...]"
    return t


def generar_link_whatsapp(telefono, mensaje):
    # Solo dígitos en el número (wa.me / api.whatsapp.com).
    telefono = "".join(c for c in (telefono or "") if c.isdigit())
    base = f"https://api.whatsapp.com/send?phone={telefono}&text="
    t = _truncar_texto_para_url(mensaje, base)
    return base + urllib.parse.quote(t, safe="")


def generar_link_sms(telefono, mensaje):
    # Conserva + para E.164 en iOS/Android cuando exista.
    telefono_limpio = (telefono or "").replace(" ", "").strip()
    base = f"sms:{telefono_limpio}?body="
    t = _truncar_texto_para_url(mensaje, base, max_total=2500)
    return base + urllib.parse.quote(t, safe="")