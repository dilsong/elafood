import csv
import os

from modules.data_paths import ruta_csv_escribible


def _ruta_clientes_csv() -> str:
    return ruta_csv_escribible("data/clientes_privados.csv", "elafood_clientes_privados.csv")


def registrar_cliente_csv(cliente: dict, canal: str) -> None:
    # Guarda/actualiza cliente por teléfono (clave). Canal: WSP, MSG o PED (pendiente / envío por enlace).
    telefono = (cliente.get("telefono") or "").strip()
    if not telefono:
        return

    nombre = (cliente.get("nombre") or "").strip()
    direccion = (cliente.get("direccion") or "").strip()
    canal = (canal or "").strip().upper()
    if canal not in {"WSP", "MSG", "PED"}:
        return

    path_csv = _ruta_clientes_csv()
    os.makedirs(os.path.dirname(path_csv), exist_ok=True)
    filas = []
    if os.path.exists(path_csv):
        with open(path_csv, "r", encoding="utf-8", newline="") as f:
            filas = list(csv.DictReader(f))

    actualizado = False
    for fila in filas:
        if (fila.get("telefono") or "").strip() == telefono:
            fila["nombre"] = nombre
            fila["direccion"] = direccion
            fila["canal"] = canal
            actualizado = True
            break

    if not actualizado:
        filas.append(
            {
                "telefono": telefono,
                "nombre": nombre,
                "direccion": direccion,
                "canal": canal,
            }
        )

    with open(path_csv, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["telefono", "nombre", "direccion", "canal"])
        w.writeheader()
        w.writerows(filas)
