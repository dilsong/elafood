import urllib.parse

def generar_mensaje(carrito, total, cliente):
    # MENSAJE LIMPIO (sin codificar)
    mensaje = "Pedido ElaFood:\n\n"

    mensaje += f"Cliente: {cliente['nombre']}\n"
    mensaje += f"Teléfono: {cliente['telefono']}\n"
    mensaje += f"Dirección: {cliente['direccion']}\n"
    mensaje += f"Notas: {cliente['notas']}\n\n"

    for item in carrito:
        linea = f"- {item['cantidad']} x {item['producto']} = ${item['precio'] * item['cantidad']}"
        mensaje += linea + "\n"

    mensaje += f"\nTotal: ${total}"
    return mensaje


def generar_link_whatsapp(telefono, mensaje):
    telefono = telefono.replace("+", "").replace(" ", "")
    mensaje_codificado = urllib.parse.quote(mensaje)
    return f"https://wa.me/{telefono}?text={mensaje_codificado}"