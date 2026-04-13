"""Aviso al chef sin depender de que se abra WhatsApp en el móvil del cliente."""

import json
import urllib.error
import urllib.request


def notificar_chef_pedido(mensaje: str, canal: str) -> None:
    """
    Si en Streamlit secrets hay credenciales, envía el texto del pedido al chef.

    Opciones (la primera que aplique):
    - TELEGRAM_BOT_TOKEN + TELEGRAM_CHEF_CHAT_ID (o TELEGRAM_CHAT_ID)
    - CHEF_WEBHOOK_URL (POST JSON {"text", "canal"})

    Fallos silenciosos: nunca debe romper el flujo del pedido.
    """
    if not (mensaje or "").strip():
        return
    try:
        import streamlit as st

        secrets = st.secrets
    except Exception:
        return

    canal = (canal or "").strip().upper() or "?"
    prefijo = f"[ElaFood · {canal}]\n\n"
    texto = (prefijo + mensaje.strip())[:4090]

    token = ""
    chat_id = ""
    webhook = ""
    try:
        token = str(secrets.get("TELEGRAM_BOT_TOKEN", "") or "").strip()
        chat_id = str(
            secrets.get("TELEGRAM_CHEF_CHAT_ID", "")
            or secrets.get("TELEGRAM_CHAT_ID", "")
            or ""
        ).strip()
        webhook = str(secrets.get("CHEF_WEBHOOK_URL", "") or "").strip()
    except Exception:
        return

    if token and chat_id:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        body = json.dumps({"chat_id": chat_id, "text": texto}).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            urllib.request.urlopen(req, timeout=12)
        except (urllib.error.URLError, OSError):
            pass
        return

    if webhook:
        body = json.dumps({"text": mensaje.strip(), "canal": canal}).encode("utf-8")
        req = urllib.request.Request(
            webhook,
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            urllib.request.urlopen(req, timeout=12)
        except (urllib.error.URLError, OSError):
            pass
