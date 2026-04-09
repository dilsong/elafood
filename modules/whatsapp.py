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


def generar_link_whatsapp(telefono, mensaje):
    telefono = telefono.replace("+", "").replace(" ", "")
    mensaje_codificado = urllib.parse.quote(mensaje)
    return f"https://wa.me/{telefono}?text={mensaje_codificado}"


def generar_link_sms(telefono, mensaje):
    telefono_limpio = telefono.replace(" ", "")
    mensaje_codificado = urllib.parse.quote(mensaje)
    return f"sms:{telefono_limpio}?body={mensaje_codificado}"