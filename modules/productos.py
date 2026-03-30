# modules/productos.py

productos = {
    "Lunch": [
        {"nombre": "Pabellón", 
         "precio": 12, 
         "imagen": "Imagenes/Comidas/Lunch/pabellon.jpg",
         "descripcion": "El pabellón criollo es un plato tradicional venezolano que consiste en arroz blanco, carne mechada (carne de res deshebrada), caraotas negras (frijoles) y tajadas de plátano maduro frito. Es un plato muy popular en Venezuela y se considera uno de los platos nacionales del país."},
        
        {"nombre": "Pollo a la plancha", 
         "precio": 10, 
         "imagen": "Imagenes/Comidas/Lunch/pollo.jpg",
         "descripcion": "El pollo a la plancha es un plato sencillo y saludable que consiste en pechugas de pollo cocinadas a la parrilla o en una sartén sin aceite. Es una opción popular para aquellos que buscan una comida baja en grasas y rica en proteínas."},
    ],
    "Comida Rápida": [
        {"nombre": "Hamburguesa", 
         "precio": 8, 
         "imagen": "Imagenes/Comidas/Rapidas/hamburguesa.jpg",
         "descripcion": "La hamburguesa es un plato de comida rápida que consiste en una o más carnes molidas (generalmente de res) cocinadas y servidas dentro de un pan redondo. A menudo se acompaña con ingredientes como queso, lechuga, tomate, cebolla, pepinillos y salsas."},
        
        {"nombre": "Perro caliente", 
         "precio": 6, 
         "imagen": "Imagenes/Comidas/Rapidas/perro.jpg",
         "descripcion": "El perro caliente es un plato de comida rápida que consiste en un pan de hot dog con una salchicha cocinada y acompañada con diversos ingredientes como ketchup, mostaza, cebolla, pepinillos y otros."},
    ],
    "Postres": [
        {"nombre": "Tres leches", 
         "precio": 5, 
         "imagen": "Imagenes/Comidas/Postres/tresleches.jpg",
         "descripcion": "El tres leches es un postre venezolano compuesto por capas de bizcocho empapado en leche condensada y crema de leche."},
        {"nombre": "Quesillo", 
         "precio": 4, 
         "imagen": "Imagenes/Comidas/Postres/quesillo.jpeg",
         "descripcion": "El quesillo es un postre venezolano hecho de queso fresco, azúcar y leche condensada, generalmente servido frío."},
    ],
    "Otros": [
        {"nombre": "Agua", 
         "precio": 1, 
         "imagen": "Imagenes/Comidas/Otros/agua.jpg",
         "descripcion": "El agua es una bebida esencial para la hidratación del cuerpo."},
        {"nombre": "Refresco", 
         "precio": 2, 
         "imagen": "Imagenes/Comidas/Otros/refresco.jpg",
         "descripcion": "El refresco es una bebida carbonatada dulce que se consume comúnmente como aperitivo o acompañamiento de comidas."},
        {"nombre": "Ponche Crema", 
         "precio": 2, 
         "imagen": "Imagenes/Comidas/Otros/ponche.jpeg",
         "descripcion": "El ponche crema es una bebida venezolana hecha con leche condensada, crema de leche y frutas."},
    ]
}

def obtener_productos(categoria):
    return productos.get(categoria, [])