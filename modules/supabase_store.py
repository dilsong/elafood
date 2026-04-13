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
        key = (
            st.secrets.get("SUPABASE_SERVICE_KEY", "").strip()
            or st.secrets.get("SUPABASE_SERVICE_ROLE_KEY", "").strip()
            or st.secrets.get("SUPABASE_KEY", "").strip()
        )
    except Exception:
        return None
    if not url or not key:
        return None
    try:
        return create_client(url, key)
    except Exception:
        return None


def registrar_pedido_supabase(carrito: list, cliente: dict, canal: str) -> tuple[bool, str]:
    """Guarda cliente y líneas en Supabase. Retorna (éxito, mensaje_error)."""
    sb = _cliente_supabase()
    if create_client is None:
        return False, "supabase-py no instalado"
    if sb is None:
        try:
            st.secrets.get("SUPABASE_URL")
        except Exception:
            return False, "sin secrets (SUPABASE_URL / clave servicio)"
        return False, "revisa SUPABASE_URL y SUPABASE_SERVICE_KEY (o SUPABASE_SERVICE_ROLE_KEY)"
    if not carrito:
        return False, "carrito vacío"

    telefono = (cliente.get("telefono") or "").strip()
    nombre = (cliente.get("nombre") or "").strip()
    direccion = (cliente.get("direccion") or "").strip()
    if not telefono or not nombre:
        return False, "falta teléfono o nombre"
    canal = (canal or "").strip().upper()
    if canal not in {"WSP", "MSG", "PED"}:
        return False, "canal no válido"

    pedido_id = str(uuid4())
    fecha_hora = datetime.now(timezone.utc).isoformat()
    try:
        base_cliente = {
            "telefono": telefono,
            "nombre": nombre,
            "direccion": direccion,
        }
        try:
            sb.table("clientes").upsert(
                {**base_cliente, "updated_at": fecha_hora},
                on_conflict="telefono",
            ).execute()
        except Exception:
            try:
                sb.table("clientes").upsert(base_cliente, on_conflict="telefono").execute()
            except Exception:
                # Sin tabla clientes o conflicto de esquema: sigue con líneas de pedido.
                pass

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
        if not filas:
            return False, "ninguna línea con cantidad > 0"
        sb.table("pedidos_detalle").insert(filas).execute()
        return True, ""
    except Exception as e:
        return False, str(e)[:400]
