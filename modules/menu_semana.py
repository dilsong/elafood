# -*- coding: utf-8 -*-
"""Menú semanal: días (lun–dom) + bloque Especial (Postres y Especialidades en Home)."""

import json
import os
import importlib

import streamlit as st
from modules.productos import PRODUCTOS

MENU_SEMANA_FILE = "data/menu_semana.json"
MENU_SEMANA_TABLE = "menu_semana_config"
MENU_SEMANA_ROW_ID = 1

DIAS_ORDEN = [
    "lunes",
    "martes",
    "miercoles",
    "jueves",
    "viernes",
    "sabado",
    "domingo",
]

ETIQUETA_DIA = {
    "lunes": "Lunes",
    "martes": "Martes",
    "miercoles": "Miércoles",
    "jueves": "Jueves",
    "viernes": "Viernes",
    "sabado": "Sábado",
    "domingo": "Domingo",
    "especial": "Especial",
}


def etiqueta_dia(clave: str) -> str:
    return ETIQUETA_DIA.get(clave, clave)


def _bloque_vacio() -> dict:
    return {"comidas": [], "postres": [], "otros": []}


def _filtrar_ids_validos(ids: list) -> list:
    # Mantiene solo productos que siguen existiendo en PRODUCTOS.
    return [pid for pid in ids if pid in PRODUCTOS]


def _supabase_client():
    try:
        supabase_mod = importlib.import_module("supabase")
        create_client = getattr(supabase_mod, "create_client", None)
    except Exception:
        return None
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


def _normalizar_menu(data: dict) -> tuple[dict, bool]:
    base = menu_semana_por_defecto()
    hubo_limpieza = False
    dias = (data or {}).get("dias") or {}
    for d in DIAS_ORDEN:
        bloque = dias.get(d) or {}
        comidas = list(bloque.get("comidas") or [])
        postres = list(bloque.get("postres") or [])
        otros = list(bloque.get("otros") or [])
        comidas_ok = _filtrar_ids_validos(comidas)
        postres_ok = _filtrar_ids_validos(postres)
        otros_ok = _filtrar_ids_validos(otros)
        if (comidas_ok != comidas) or (postres_ok != postres) or (otros_ok != otros):
            hubo_limpieza = True
        base["dias"][d] = {
            "comidas": comidas_ok,
            "postres": postres_ok,
            "otros": otros_ok,
        }

    esp = (data or {}).get("especial") or {}
    esp_comidas = list(esp.get("comidas") or [])
    esp_postres = list(esp.get("postres") or [])
    esp_otros = list(esp.get("otros") or [])
    esp_comidas_ok = _filtrar_ids_validos(esp_comidas)
    esp_postres_ok = _filtrar_ids_validos(esp_postres)
    esp_otros_ok = _filtrar_ids_validos(esp_otros)
    if (esp_comidas_ok != esp_comidas) or (esp_postres_ok != esp_postres) or (esp_otros_ok != esp_otros):
        hubo_limpieza = True
    base["especial"] = {
        "comidas": esp_comidas_ok,
        "postres": esp_postres_ok,
        "otros": esp_otros_ok,
    }
    return base, hubo_limpieza


def _cargar_menu_supabase():
    sb = _supabase_client()
    if sb is None:
        return None
    try:
        resp = (
            sb.table(MENU_SEMANA_TABLE)
            .select("data")
            .eq("id", MENU_SEMANA_ROW_ID)
            .limit(1)
            .execute()
        )
        rows = resp.data or []
        if not rows:
            return None
        return rows[0].get("data")
    except Exception:
        return None


def _guardar_menu_supabase(data: dict) -> bool:
    sb = _supabase_client()
    if sb is None:
        return False
    try:
        sb.table(MENU_SEMANA_TABLE).upsert(
            {"id": MENU_SEMANA_ROW_ID, "data": data},
            on_conflict="id",
        ).execute()
        return True
    except Exception:
        return False


def menu_semana_por_defecto() -> dict:
    return {
        "dias": {d: _bloque_vacio() for d in DIAS_ORDEN},
        "especial": _bloque_vacio(),
    }


def cargar_menu_semana() -> dict:
    # Fuente principal: Supabase (si está configurado). Fallback: archivo local.
    data_supabase = _cargar_menu_supabase()
    if data_supabase is not None:
        base, hubo_limpieza = _normalizar_menu(data_supabase)
        if hubo_limpieza:
            _guardar_menu_supabase(base)
        return base

    if not os.path.exists(MENU_SEMANA_FILE) or os.path.getsize(MENU_SEMANA_FILE) == 0:
        data = menu_semana_por_defecto()
        guardar_menu_semana(data)
        return data
    try:
        with open(MENU_SEMANA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, ValueError):
        data = menu_semana_por_defecto()
        guardar_menu_semana(data)
        return data

    base, hubo_limpieza = _normalizar_menu(data)
    if hubo_limpieza:
        guardar_menu_semana(base)
    return base


def guardar_menu_semana(data: dict) -> None:
    base, _ = _normalizar_menu(data or {})
    _guardar_menu_supabase(base)
    os.makedirs(os.path.dirname(MENU_SEMANA_FILE), exist_ok=True)
    with open(MENU_SEMANA_FILE, "w", encoding="utf-8") as f:
        json.dump(base, f, ensure_ascii=False, indent=2)


def ids_opcion_comidas() -> list:
    return sorted(
        [
            pid
            for pid, p in PRODUCTOS.items()
            if p["categoria"] in ("lunch", "comida_rapida")
        ],
        key=lambda x: PRODUCTOS[x]["nombre"].lower(),
    )


def ids_opcion_postres() -> list:
    return sorted(
        [pid for pid, p in PRODUCTOS.items() if p["categoria"] == "postres"],
        key=lambda x: PRODUCTOS[x]["nombre"].lower(),
    )


def ids_opcion_otros() -> list:
    return sorted(
        [pid for pid, p in PRODUCTOS.items() if p["categoria"] == "otros"],
        key=lambda x: PRODUCTOS[x]["nombre"].lower(),
    )


def nombre_producto(pid: str) -> str:
    return PRODUCTOS.get(pid, {}).get("nombre", pid)
