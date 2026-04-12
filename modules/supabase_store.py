from datetime import datetime, timezone
from uuid import uuid4

import streamlit as st

try:
    from supabase import create_client
except Exception:  # pragma: no cover
    create_client = None


def _cliente_supabase():
    # Devuelve cliente Supabase si hay secrets válidos.
    if create_client is None:
        return None
    try:
        url = st.secrets.get("SUPABASE_URL", "").strip()
        key = st.secrets.get("SUPABASE_SERVICE_KEY", "").strip()
    except Exception:
        return None
    if not url or not key:
        return None
    try:
        return create_client(url, key)
    except Exception:
        return None


def registrar_pedido_supabase(carrito: list, cliente: dict, canal: str) -> bool:
    # Guarda cliente y líneas de pedido. Retorna True si escribió en Supabase.
    sb = _cliente_supabase()
    if sb is None or not carrito:
        return False

    telefono = (cliente.get("telefono") or "").strip()
    nombre = (cliente.get("nombre") or "").strip()
    direccion = (cliente.get("direccion") or "").strip()
    if not telefono or not nombre:
        return False
    canal = (canal or "").strip().upper()
    if canal not in {"WSP", "MSG", "PED"}:
        return False

    pedido_id = str(uuid4())
    fecha_hora = datetime.now(timezone.utc).isoformat()
    try:
        sb.table("clientes").upsert(
            {
                "telefono": telefono,
                "nombre": nombre,
                "direccion": direccion,
                "updated_at": fecha_hora,
            },
            on_conflict="telefono",
        ).execute()

        filas = []
        for item in carrito:
            cantidad = int(item.get("cantidad") or 0)
            precio = float(item.get("precio") or 0)
            if cantidad <= 0:
                continue
            filas.append(
                {
                    "pedido_id": pedido_id,
                    "fecha_hora_utc": fecha_hora,
                    "telefono": telefono,
                    "nombre": nombre,
                    "producto": item.get("producto", ""),
                    "cantidad": cantidad,
                    "precio_unitario": precio,
                    "subtotal": cantidad * precio,
                    "canal": canal,
                }
            )
        if filas:
            sb.table("pedidos_detalle").insert(filas).execute()
        return True
    except Exception:
        return False
