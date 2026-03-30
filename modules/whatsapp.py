import urllib.parse

def generar_mensaje(carrito, total):
    mensaje = "Pedido ElaFood:%0A%0A"

    for item in carrito:
        linea = f"- {item['cantidad']} x {item['producto']} = ${item['precio'] * item['cantidad']}"
        mensaje += urllib.parse.quote(linea) + "%0A"

    mensaje += f"%0ATotal: ${total}"
    return mensaje

def generar_link_whatsapp(telefono, mensaje):
    telefono = telefono.replace("+", "").replace(" ", "")
    return f"https://wa.me/{telefono}?text={mensaje}"