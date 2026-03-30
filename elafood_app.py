import streamlit as st
from urllib.parse import quote

# =========================
# CONFIGURACIÓN BÁSICA
# =========================
st.set_page_config(page_title="ElaFood - Pedidos", page_icon="🍽️", layout="centered")

# Cambia estos datos por los tuyos
WHATSAPP_NUMBER = "17865551234"  # Formato internacional sin + ni espacios, ej: 1786xxxxxxx
ZELLE_EMAIL = "tuzelle@example.com"
ZELLE_NAME = "ElaFood"

# =========================
# CATÁLOGO DE PRODUCTOS
# =========================
PRODUCTOS = [
    {
        "categoria": "Lunch",
        "nombre": "Lunch Ejecutivo Pollo",
        "descripcion": "Pollo a la plancha, arroz, ensalada.",
        "precio": 12.0,
    },
    {
        "categoria": "Lunch",
        "nombre": "Lunch Ejecutivo Carne",
        "descripcion": "Carne guisada, arroz, ensalada.",
        "precio": 13.0,
    },
    {
        "categoria": "Comida rápida",
        "nombre": "Hamburguesa Clásica",
        "descripcion": "Carne, queso, lechuga, tomate, salsas.",
        "precio": 8.0,
    },
    {
        "categoria": "Comida rápida",
        "nombre": "Tequeños (6 unidades)",
        "descripcion": "Rellenos de queso.",
        "precio": 6.0,
    },
    {
        "categoria": "Postres",
        "nombre": "Tres Leches",
        "descripcion": "Postre tradicional, porción individual.",
        "precio": 5.0,
    },
    {
        "categoria": "Postres",
        "nombre": "Quesillo",
        "descripcion": "Flan venezolano casero.",
        "precio": 4.5,
    },
]

# =========================
# ESTADO DEL CARRITO
# =========================
if "cantidades" not in st.session_state:
    st.session_state.cantidades = {p["nombre"]: 0 for p in PRODUCTOS}


def actualizar_cantidad(nombre, cantidad):
    st.session_state.cantidades[nombre] = cantidad


# =========================
# UI PRINCIPAL
# =========================
st.title("ElaFood 🍽️")
st.subheader("Pedidos de lunch, comida rápida y postres")

st.markdown(
    "Selecciona los productos y cantidades que deseas, revisa el total y envía tu pedido por WhatsApp."
)

st.divider()

# Datos del cliente
st.header("Tus datos")
col_nombre, col_direccion = st.columns(2)
with col_nombre:
    nombre_cliente = st.text_input("Nombre", "")
with col_direccion:
    direccion_cliente = st.text_input("Dirección (opcional)", "")

metodo_pago = st.selectbox(
    "Método de pago preferido",
    ["Zelle", "Efectivo", "Otro"],
)

st.divider()

# =========================
# CATÁLOGO + SELECCIÓN
# =========================
st.header("Menú ElaFood")

categorias = sorted(set(p["categoria"] for p in PRODUCTOS))
for cat in categorias:
    st.subheader(cat)
    cat_items = [p for p in PRODUCTOS if p["categoria"] == cat]

    for p in cat_items:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{p['nombre']}**  \n${p['precio']:.2f}")
            st.caption(p["descripcion"])
        with col2:
            cantidad = st.number_input(
                "Cant.",
                min_value=0,
                max_value=50,
                step=1,
                key=f"qty_{p['nombre']}",
                value=st.session_state.cantidades[p["nombre"]],
            )
            actualizar_cantidad(p["nombre"], cantidad)

    st.markdown("---")

# =========================
# RESUMEN DEL PEDIDO
# =========================
st.header("Resumen del pedido")

items_seleccionados = []
total = 0.0

for p in PRODUCTOS:
    qty = st.session_state.cantidades[p["nombre"]]
    if qty > 0:
        subtotal = qty * p["precio"]
        total += subtotal
        items_seleccionados.append((p["nombre"], qty, p["precio"], subtotal))

if not items_seleccionados:
    st.info("No has seleccionado ningún producto todavía.")
else:
    for nombre, qty, precio, subtotal in items_seleccionados:
        st.markdown(
            f"- **{qty}x {nombre}** — ${precio:.2f} c/u = **${subtotal:.2f}**"
        )

    st.markdown(f"### Total a pagar: **${total:.2f}**")

st.divider()

# =========================
# GENERAR MENSAJE DE PEDIDO
# =========================
def construir_mensaje_whatsapp():
    if not items_seleccionados:
        return ""

    lineas = ["Pedido ElaFood", "----------------------"]
    for nombre, qty, precio, subtotal in items_seleccionados:
        lineas.append(f"{qty}x {nombre} - ${subtotal:.2f}")

    lineas.append("")
    lineas.append(f"Total: ${total:.2f}")
    lineas.append("")
    lineas.append(f"Nombre del cliente: {nombre_cliente or 'No indicado'}")
    if direccion_cliente:
        lineas.append(f"Dirección: {direccion_cliente}")
    lineas.append(f"Método de pago: {metodo_pago}")
    if metodo_pago == "Zelle":
        lineas.append("")
        lineas.append("Datos para Zelle (una vez confirmado el pedido):")
        lineas.append(f"Nombre: {ZELLE_NAME}")
        lineas.append(f"Correo: {ZELLE_EMAIL}")
        lineas.append(f"Monto: ${total:.2f}")

    return "\n".join(lineas)


st.header("Enviar pedido")

if not items_seleccionados:
    st.warning("Selecciona al menos un producto para poder enviar el pedido.")
else:
    mensaje = construir_mensaje_whatsapp()
    mensaje_codificado = quote(mensaje)

    url_whatsapp = f"https://wa.me/{WHATSAPP_NUMBER}?text={mensaje_codificado}"

    st.markdown("Revisa tu pedido y, si todo está bien, envíalo por WhatsApp:")

    st.text_area("Vista previa del mensaje", mensaje, height=200)

    st.markdown(
        f"[📲 Enviar pedido por WhatsApp]({url_whatsapp})",
        unsafe_allow_html=True,
    )

    st.info(
        f"Una vez que confirmemos tu pedido, podrás realizar el pago por Zelle a **{ZELLE_EMAIL}** por el monto de **${total:.2f}**."
    )