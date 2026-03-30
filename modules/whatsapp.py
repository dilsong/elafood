import urllib.parse

def generar_mensaje(carrito, total, cliente):
    mensaje = "Pedido ElaFood:%0A%0A"

    # Datos del cliente
    mensaje += urllib.parse.quote(f"Cliente: {cliente['nombre']}") + "%0A"
    mensaje += urllib.parse.quote(f"Teléfono: {cliente['telefono']}") + "%0A"
    mensaje += urllib.parse.quote(f"Dirección: {cliente['direccion']}") + "%0A"
    mensaje += urllib.parse.quote(f"Notas: {cliente['notas']}") + "%0A%0A"

    # Productos
    for item in carrito:
        linea = f"- {item['cantidad']} x {item['producto']} = ${item['precio'] * item['cantidad']}"
        mensaje += urllib.parse.quote(linea) + "%0A"

    mensaje += f"%0ATotal: ${total}"
    return mensaje

def generar_link_whatsapp(telefono, mensaje):
    telefono = telefono.replace("+", "").replace(" ", "")
    mensaje_codificado = urllib.parse.quote(mensaje)
    return f"https://wa.me/{telefono}?text={mensaje_codificado}"