import csv
import os
from datetime import datetime, timezone
from uuid import uuid4

CSV_PEDIDOS = "data/pedidos_privados.csv"


def registrar_pedido_csv(carrito: list, cliente: dict, canal: str) -> None:
    # Respaldo local: una fila por línea de producto del pedido.
    if not carrito:
        return
    telefono = (cliente.get("telefono") or "").strip()
    nombre = (cliente.get("nombre") or "").strip()
    direccion = (cliente.get("direccion") or "").strip()
    if not telefono or not nombre:
        return
    canal = (canal or "").strip().upper()
    if canal not in {"WSP", "MSG"}:
        return

    os.makedirs(os.path.dirname(CSV_PEDIDOS), exist_ok=True)
    pedido_id = str(uuid4())
    fecha_hora = datetime.now(timezone.utc).isoformat()

    existe = os.path.exists(CSV_PEDIDOS)
    with open(CSV_PEDIDOS, "a", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "pedido_id",
                "fecha_hora_utc",
                "telefono",
                "nombre",
                "direccion",
                "producto",
                "cantidad",
                "precio_unitario",
                "subtotal",
                "canal",
            ],
        )
        if not existe:
            w.writeheader()
        for item in carrito:
            cantidad = int(item.get("cantidad") or 0)
            precio = float(item.get("precio") or 0)
            if cantidad <= 0:
                continue
            w.writerow(
                {
                    "pedido_id": pedido_id,
                    "fecha_hora_utc": fecha_hora,
                    "telefono": telefono,
                    "nombre": nombre,
                    "direccion": direccion,
                    "producto": item.get("producto", ""),
                    "cantidad": cantidad,
                    "precio_unitario": precio,
                    "subtotal": cantidad * precio,
                    "canal": canal,
                }
            )
