# modules/productos.py

# Base de productos unificada para ElaFood
# Compatible con el Panel del Chef y con el sistema actual

PRODUCTOS = {
    "produ_001": {
        "nombre": "Pabellón",
        "precio": 15,
        "categoria": "lunch",
        "imagen": "Imagenes/Comidas/Lunch/pabellon.jpg",
        "descripcion": "El pabellón criollo es un plato tradicional venezolano que consiste en arroz blanco, carne mechada (carne de res deshebrada), caraotas negras (frijoles) y tajadas de plátano maduro frito."
        " The pabellón criollo is a traditional Venezuelan dish that consists of white rice, shredded beef, black beans, and fried ripe plantain slices."
    },
    "produ_0011": {
        "nombre": "Milanesa de Pollo",
        "precio": 15,
        "categoria": "lunch",
        "imagen": "Imagenes/Comidas/Lunch/milanesapollo.jpg",
        "descripcion": "La milanesa de pollo es un plato popular que consiste en pechugas de pollo empanizadas y fritas hasta obtener una textura crujiente por fuera y jugosa por dentro."
        " The chicken milanesa is a popular dish that consists of breaded and fried chicken breasts until they achieve a crispy texture on the outside and juicy on the inside."
    },
    "produ_0012": {
        "nombre": "Hervido de Res y Pollo",
        "precio": 15,
        "categoria": "lunch",
        "imagen": "Imagenes/Comidas/Lunch/hervidoderesypollo.jpg",
        "descripcion": "El hervido de res y pollo es un plato tradicional que consiste en carne de res y pollo cocinadas en una sopa cremosa."
        " The beef and chicken stew is a traditional dish that consists of beef and chicken cooked in a creamy soup."
    },

    "produ_0013": {
        "nombre": "Gordon Bleu",
        "precio": 15,
        "categoria": "lunch",
        "imagen": "Imagenes/Comidas/Lunch/gordonbleu.jpg",
        "descripcion": "El Gordon Bleu es un plato francés que consiste en pechugas de pollo rellenas de queso y empanizadas."
        " The Gordon Bleu is a French dish that consists of chicken breasts filled with cheese and breaded."
    },
    "produ_0014": {
        "nombre": "Fajitas",
        "precio": 15,
        "categoria": "lunch",
        "imagen": "Imagenes/Comidas/Lunch/fajitas.jpg",
        "descripcion": "Las fajitas son un plato mexicano que consiste en carne (generalmente pollo o res) servida con vegetales, granos y salsas."
        " Fajitas are a Mexican dish that consists of meat (usually chicken or beef) served with vegetables and salsas."
    },
    "produ_0015": {
        "nombre": "Chuleta de Cerdo",
        "precio": 15,
        "categoria": "lunch",
        "imagen": "Imagenes/Comidas/Lunch/chuletadecerdo.jpg",
        "descripcion": "La chuleta de cerdo es un plato delicioso que consiste en costillas de cerdo cocinadas a la parrilla o en el horno."
        " The pork rib is a delicious dish that consists of pork ribs cooked on the grill or in the oven."
    },
    "produ_0016": {
        "nombre": "Ceviche Mixto",
        "precio": 15,
        "categoria": "lunch",
        "imagen": "Imagenes/Comidas/Lunch/cevichemixto.jpg",
        "descripcion": "El ceviche mixto es un plato peruano que consiste en pescado y camaron crudo marinado en jugo de limón y acompañado con vegetales y salsas."
        " The mixed ceviche is a Peruvian dish that consists of raw fish and shrimp marinated in lime juice and served with vegetables and salsas."
    },

    "produ_002": {
        "nombre": "Pollo al Horno",
        "precio": 15,
        "categoria": "lunch",
        "imagen": "Imagenes/Comidas/Lunch/polloalhorno.jpg",
        "descripcion": "El pollo al horno es un plato sencillo y saludable que consiste en pechugas de pollo cocinadas en el horno."
        " The chicken in the oven is a simple and healthy dish that consists of chicken breasts cooked in the oven."
    },
    "produ_0021": {
        "nombre": "Pollo Guisado",
        "precio": 15,
        "categoria": "lunch",
        "imagen": "Imagenes/Comidas/Lunch/polloguisado.jpg",
        "descripcion": "El pollo guisado es un plato rico y sabroso que consiste en pechugas de pollo cocinadas en una salsa cremosa."
        " The chicken stew is a rich and flavorful dish that consists of chicken breasts cooked in a creamy sauce."
    },
    "produ_0022": {
        "nombre": "Pasticho",
        "precio": 15,
        "categoria": "lunch",
        "imagen": "Imagenes/Comidas/Lunch/pasticho.jpg",
        "descripcion": "El pasticho es un plato tradicional venezolano que consiste en carne molida cocinada con ingredientes especiados."
        " The pasticho is a traditional Venezuelan dish that consists of seasoned ground meat cooked with spices."
    },

    "produ_003": {
        "nombre": "Hamburguesa",
        "precio": 15,
        "categoria": "comida_rapida",
        "imagen": "Imagenes/Comidas/Rapidas/hamburguesa.jpg",
        "descripcion": "La hamburguesa es un plato de comida rápida que consiste en carne molida servida dentro de un pan redondo con ingredientes adicionales."
    },

    "produ_0041": {
        "nombre": "Enrrollado de Pollo-Carne",
        "precio": 15,
        "categoria": "comida_rapida",
        "imagen": "Imagenes/Comidas/Rapidas/enrrollado.jpg",
        "descripcion": "Un delicioso enrrollado de pollo y carne, relleno con ingredientes frescos y sazonados."
        " A delicious chicken and beef roll, filled with fresh and seasoned ingredients."
    },
    "produ_005": {
        "nombre": "Cuatro Leches",
        "precio": 50,
        "categoria": "postres",
        "imagen": "Imagenes/Comidas/Postres/cuatroleches.jpg",
        "descripcion": "Bizcocho esponjoso y suave, bañado en una deliciosa mezcla de cuatro leches que lo hacen extra jugoso y cremoso. Cubierto con una ligera capa de crema batida y un toque especial que lo vuelve irresistible."
        " A fluffy and soft sponge cake, soaked in a delicious four-milk mixture that makes it extra moist and creamy. Topped with a light layer of whipped cream and a special touch that makes it irresistible."
    },
    "produ_0051": {
        "nombre": "Cuatro Leches / Mediana",
        "precio": 35,
        "categoria": "postres",
        "imagen": "Imagenes/Comidas/Postres/cuatrolechesmediana.jpg",
        "descripcion": "Bizcocho esponjoso y suave, bañado en una deliciosa mezcla de cuatro leches que lo hacen extra jugoso y cremoso. Cubierto con una ligera capa de crema batida y un toque especial que lo vuelve irresistible."
        " A fluffy and soft sponge cake, soaked in a delicious four-milk mixture that makes it extra moist and creamy. Topped with a light layer of whipped cream and a special touch that makes it irresistible."
    },
    "produ_0052": {
        "nombre": "Cuatro Leches / Porcion",
        "precio": 8,
        "categoria": "postres",
        "imagen": "Imagenes/Comidas/Postres/cuatrolechesporcion.jpg",
        "descripcion": "Bizcocho esponjoso y suave, bañado en una deliciosa mezcla de cuatro leches que lo hacen extra jugoso y cremoso. Cubierto con una ligera capa de crema batida y un toque especial que lo vuelve irresistible."
        " A fluffy and soft sponge cake, soaked in a delicious four-milk mixture that makes it extra moist and creamy. Topped with a light layer of whipped cream and a special touch that makes it irresistible."
    },
    "produ_0053": {
        "nombre": "Cuatro Leches / Docena",
        "precio": 35,
        "categoria": "postres",
        "imagen": "Imagenes/Comidas/Postres/cuatrolechesdocena.jpg",
        "descripcion": "Pide tu docena de shots de 4 leches para tus momentos especiales."
        " Get your dozen 4 milk shots for your special moments."
    },
    "produ_0054": {
        "nombre": "Ponque Mediano",
        "precio": 30,
        "categoria": "postres",
        "imagen": "Imagenes/Comidas/Postres/ponquemediano.jpg",
        "descripcion": "Nuestro PONQUE de Vainilla es esponjoso, suave y lleno de un delicioso sabor casero que encanta en cada bocado, perfecto para acompañar con un cafecito."
        " Our Vanilla PONQUE is fluffy, soft, and full of a delicious homemade flavor that delights in every bite, perfect to accompany with a cup of coffee."
    },
    "produ_0055": {
        "nombre": "Ponque Especial",
        "precio": 35,
        "categoria": "postres",
        "imagen": "Imagenes/Comidas/Postres/ponqueespecial.jpg",
        "descripcion": "Nuestro PONQUE de Vainilla es esponjoso, suave y lleno de un delicioso sabor casero que encanta en cada bocado, perfecto para acompañar con un cafecito."
        " Our Vanilla PONQUE is fluffy, soft, and full of a delicious homemade flavor that delights in every bite, perfect to accompany with a cup of coffee."
    },
    "produ_0056": {
        "nombre": "Ponquecitos/ Docena",
        "precio": 39,
        "categoria": "postres",
        "imagen": "Imagenes/Comidas/Postres/ponquecitos.jpg",
        "descripcion": "Docena de Ponquesitos rellenos con el más delicioso Dulce de Leche! Dozen cupcakes filled with the most delicious Dulce de Leche!"
        " Dozen cupcakes filled with the most delicious Dulce de Leche!"
    },

    "produ_006": {
        "nombre": "Quesillo",
        "precio": 30,
        "categoria": "postres",
        "imagen": "Imagenes/Comidas/Postres/quesillo.jpg",
        "descripcion": "Postre venezolano hecho con leche condensada, huevos y azúcar, de textura suave."
        " Venezuelan dessert made with condensed milk, eggs, and sugar, with a smooth texture."        
    },
    "produ_0061": {
        "nombre": "Quesillo con Coco",
        "precio": 35,
        "categoria": "postres",
        "imagen": "Imagenes/Comidas/Postres/quesillococo.jpg",
        "descripcion": "Postre venezolano hecho con leche condensada, huevos y azúcar, de textura suave."
        " Venezuelan dessert made with condensed milk, eggs, and sugar, with a smooth texture."
    },
    "produ_008": {
        "nombre": "Agua",
        "precio": 3,
        "categoria": "otros",
        "imagen": "Imagenes/Comidas/Otros/agua.jpg",
        "descripcion": "Agua mineral embotellada."
    },

    "produ_0081": {
        "nombre": "Refresco",
        "precio": 3,
        "categoria": "otros",
        "imagen": "Imagenes/Comidas/Otros/refresco.jpg",
        "descripcion": "Bebida carbonatada dulce, ideal para acompañar comidas."
    },

    "produ_009": {
        "nombre": "Ponche Crema",
        "precio": 8,
        "categoria": "otros",
        "imagen": "Imagenes/Comidas/Otros/ponche.jpeg",
        "descripcion": "Bebida venezolana hecha con leche condensada, crema de leche y especias."
    },
    "produ_0010": {
        "nombre": "Pan de Jamón",
        "precio": 45,
        "categoria": "otros",
        "imagen": "Imagenes/Comidas/Otros/pandejamon.jpg",
        "descripcion": "Pan de jamón tradicional, suave y recién horneado, relleno con jamón, tocineta, aceitunas y pasas que crean el balance perfecto entre salado y dulce. ¡Disrútalo calientito, porque asi sabe mucho mejor!"
        " Traditional ham bread, soft and freshly baked, filled with ham, bacon, olives, and raisins that create the perfect balance between salty and sweet. Enjoy it warm, because that's how it tastes much better!"
    },
    "produ_0011": {
        "nombre": "Pan de Jamón Medio Kilo",
        "precio": 25,
        "categoria": "otros",
        "imagen": "Imagenes/Comidas/Otros/pandejamonmedio.jpg",
        "descripcion": "Pan de jamón especial, suave y recién horneado, relleno con jamón, tocineta, aceitunas y pasas que crean el balance perfecto entre salado y dulce. ¡Disrútalo calientito, porque asi sabe mucho mejor!"
        " Special ham bread, soft and freshly baked, filled with ham, bacon, olives, and raisins that create the perfect balance between salty and sweet. Enjoy it warm, because that's how it tastes much better!"
    },
    "produ_0012": {
        "nombre": "Pan de Jamón Porción - 12 Rollos",
        "precio": 12,
        "categoria": "otros",
        "imagen": "Imagenes/Comidas/Otros/pandejamonporcion.jpg",
        "descripcion": "Pan de jamón porción, suave y recién horneado, relleno con jamón, tocineta, aceitunas y pasas que crean el balance perfecto entre salado y dulce. ¡Disrútalo calientito, porque asi sabe mucho mejor!"
        " Ham bread portion, soft and freshly baked, filled with ham, bacon, olives, and raisins that create the perfect balance between salty and sweet. Enjoy it warm, because that's how it tastes much better!"
    },
    "produ_0013": {
        "nombre": "50 - Teqenos",
        "precio": 60,
        "categoria": "otros",
        "imagen": "Imagenes/Comidas/Otros/tequenos50.jpg",
        "descripcion": "Deliciosos tequeños recién hechos, doraditos y crujientes por fuera, con queso derretido y suave por dentro."
        " Delicious freshly made tequeños, golden and crispy on the outside, with melted and soft cheese on the inside."
    },
    "produ_0014": {
        "nombre": "25 - Teqenos",
        "precio": 35,
        "categoria": "otros",
        "imagen": "Imagenes/Comidas/Otros/tequenos25.jpg",
        "descripcion": "Teqenos porción, deliciosos y recién hechos, doraditos y crujientes por fuera, con queso derretido y suave por dentro."
        " Tequeños portion, delicious and freshly made, golden and crispy on the outside, with melted and soft cheese on the inside."
    },
    "produ_0015": {
        "nombre": "Salsa de Pimenton",
        "precio": 20,
        "categoria": "otros",
        "imagen": "Imagenes/Comidas/Otros/salsapimenton.jpg",
        "descripcion": "Salsa de pimentón, ideal para acompañar comidas."
        " Pimenton sauce, ideal for accompanying meals."
    },
    "produ_0016": {
        "nombre": "Salsa de Pina",
        "precio": 20,
        "categoria": "otros",
        "imagen": "Imagenes/Comidas/Otros/salsapina.jpg",
        "descripcion": "Salsa de pina, ideal para acompañar comidas."
        " Pineapple sauce, ideal for accompanying meals."
    },

}


def categoria_por_nombre(nombre: str) -> str | None:
    for _pid, p in PRODUCTOS.items():
        if p["nombre"] == nombre:
            return p["categoria"]
    return None


def es_comida_lunch_o_rapida_por_nombre(nombre: str) -> bool:
    c = categoria_por_nombre(nombre)
    return c in ("lunch", "comida_rapida")
