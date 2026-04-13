import csv
import os
from datetime import datetime, timezone
from uuid import uuid4

from modules.data_paths import ruta_csv_escribible


def _ruta_pedidos_csv() -> str:
    return ruta_csv_escribible("data/pedidos_privados.csv", "elafood_pedidos_privados.csv")


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
    if canal not in {"WSP", "MSG", "PED"}:
        return

    path_csv = _ruta_pedidos_csv()
    os.makedirs(os.path.dirname(path_csv), exist_ok=True)
    pedido_id = str(uuid4())
    fecha_hora = datetime.now(timezone.utc).isoformat()

    existe = os.path.exists(path_csv)
    with open(path_csv, "a", encoding="utf-8", newline="") as f:
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
