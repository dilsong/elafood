# modules/productos.py

productos = {
    "Lunch": [
        {"nombre": "Pabellón", "precio": 12},
        {"nombre": "Pollo a la plancha", "precio": 10},
    ],
    "Comida Rápida": [
        {"nombre": "Hamburguesa", "precio": 8},
        {"nombre": "Perro caliente", "precio": 6},
    ],
    "Postres": [
        {"nombre": "Tres leches", "precio": 5},
        {"nombre": "Quesillo", "precio": 4},
    ],
    "Otros": [
        {"nombre": "Agua", "precio": 1},
        {"nombre": "Refresco", "precio": 2},
    ]
}

def obtener_productos(categoria):
    return productos.get(categoria, [])