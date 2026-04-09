import csv
import os

CSV_CLIENTES = "data/clientes_privados.csv"


def registrar_cliente_csv(cliente: dict, canal: str) -> None:
    # Guarda/actualiza cliente por teléfono (clave) con canal WSP/MSG.
    telefono = (cliente.get("telefono") or "").strip()
    if not telefono:
        return

    nombre = (cliente.get("nombre") or "").strip()
    direccion = (cliente.get("direccion") or "").strip()
    canal = (canal or "").strip().upper()
    if canal not in {"WSP", "MSG"}:
        return

    os.makedirs(os.path.dirname(CSV_CLIENTES), exist_ok=True)
    filas = []
    if os.path.exists(CSV_CLIENTES):
        with open(CSV_CLIENTES, "r", encoding="utf-8", newline="") as f:
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

    with open(CSV_CLIENTES, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["telefono", "nombre", "direccion", "canal"])
        w.writeheader()
        w.writerows(filas)
