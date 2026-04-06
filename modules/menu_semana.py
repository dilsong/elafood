# -*- coding: utf-8 -*-
"""Menú semanal: días (lun–dom) + bloque Especial (Postres y Especialidades en Home)."""

import json
import os

from modules.productos import PRODUCTOS

MENU_SEMANA_FILE = "data/menu_semana.json"

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


def menu_semana_por_defecto() -> dict:
    return {
        "dias": {d: _bloque_vacio() for d in DIAS_ORDEN},
        "especial": _bloque_vacio(),
    }


def cargar_menu_semana() -> dict:
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

    base = menu_semana_por_defecto()
    dias = data.get("dias") or {}
    for d in DIAS_ORDEN:
        bloque = dias.get(d) or {}
        base["dias"][d] = {
            "comidas": list(bloque.get("comidas") or []),
            "postres": list(bloque.get("postres") or []),
            "otros": list(bloque.get("otros") or []),
        }
    esp = data.get("especial") or {}
    base["especial"] = {
        "comidas": list(esp.get("comidas") or []),
        "postres": list(esp.get("postres") or []),
        "otros": list(esp.get("otros") or []),
    }
    return base


def guardar_menu_semana(data: dict) -> None:
    os.makedirs(os.path.dirname(MENU_SEMANA_FILE), exist_ok=True)
    with open(MENU_SEMANA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


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
