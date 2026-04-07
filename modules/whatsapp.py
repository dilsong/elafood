import urllib.parse

from modules.menu_semana import etiqueta_dia
from modules.productos import es_comida_lunch_o_rapida_por_nombre


def _nombre_linea_pedido(item: dict) -> str:
    producto = item["producto"]
    dia = item.get("dia")
    if dia and es_comida_lunch_o_rapida_por_nombre(producto):
        return f"{etiqueta_dia(dia)} — {producto}"
    return producto


def generar_mensaje(carrito, total, cliente):
    mensaje = "Pedido ElaFood:\n\n"

    mensaje += f"Cliente: {cliente['nombre']}\n"
    mensaje += f"Teléfono: {cliente['telefono']}\n"
    mensaje += f"Dirección: {cliente['direccion']}\n"
    mensaje += f"Notas: {cliente['notas']}\n\n"

    for item in carrito:
        nombre = _nombre_linea_pedido(item)
        linea = f"- {item['cantidad']} x {nombre} = ${item['precio'] * item['cantidad']}"
        mensaje += linea + "\n"

    mensaje += f"\nTotal: ${total}"
    return mensaje


def generar_link_whatsapp(telefono, mensaje):
    telefono = telefono.replace("+", "").replace(" ", "")
    mensaje_codificado = urllib.parse.quote(mensaje)
    return f"https://wa.me/{telefono}?text={mensaje_codificado}"


def generar_link_sms(telefono, mensaje):
    telefono_limpio = telefono.replace(" ", "")
    mensaje_codificado = urllib.parse.quote(mensaje)
    return f"sms:{telefono_limpio}?body={mensaje_codificado}"