# modules/productos.py
import json
import os
import importlib
from uuid import uuid4

import streamlit as st
from modules.i18n import get_lang

# Base de productos unificada para ElaFood
# Compatible con el Panel del Chef y con el sistema actual

PRODUCTOS = {
    "produ_0010": {
        "nombre": "Pabellón",
        "precio": 15,
        "categoria": "lunch",
        "imagen": "Imagenes/Comidas/Lunch/pabellon.jpg",
        "descripcion": "El pabellón criollo es un plato tradicional venezolano que consiste en arroz blanco, carne mechada (carne de res deshebrada), caraotas negras (frijoles) y tajadas de plátano maduro frito.",
        
        "nombre_es": "Pabellón",
        "nombre_en": "Pabellón",
        "descripcion_es": "El pabellón criollo es un plato tradicional venezolano que consiste en arroz blanco, carne mechada (carne de res deshebrada), caraotas negras (frijoles) y tajadas de plátano maduro frito.",
        "descripcion_en": "Pabellón criollo is a traditional Venezuelan dish that consists of white rice, shredded beef (carne mechada), black beans (caraotas negras), and fried ripe plantain slices (tajadas)."
    },
    "produ_0020": {
        "nombre": "Milanesa de Pollo",
        "precio": 15,
        "categoria": "lunch",
        "imagen": "Imagenes/Comidas/Lunch/milanesapollo.jpg",
        "descripcion": "La milanesa de pollo es un plato popular que consiste en pechugas de pollo empanizadas y fritas hasta obtener una textura crujiente por fuera y jugosa por dentro.",
        
        "nombre_es": "Milanesa de Pollo",
        "nombre_en": "Chicken Cutlet",
        "descripcion_es": "La milanesa de pollo es un plato popular que consiste en pechugas de pollo empanizadas y fritas hasta obtener una textura crujiente por fuera y jugosa por dentro.",
        "descripcion_en": "Chicken cutlet is a popular dish consisting of breaded and fried chicken breasts."
    },
    "produ_0030": {
        "nombre": "Hervido de Res y Pollo",
        "precio": 15,
        "categoria": "lunch",
        "imagen": "Imagenes/Comidas/Lunch/hervidoderesypollo.jpg",
        "descripcion": "El hervido de res y pollo es un plato tradicional que consiste en carne de res y pollo cocinadas en una sopa cremosa.",
        
        "nombre_es": "Hervido de Res y Pollo",
        "nombre_en": "Beef and Chicken Stew",
        "descripcion_es": "El hervido de res y pollo es un plato tradicional que consiste en carne de res y pollo cocinadas en una sopa cremosa.",
        "descripcion_en": "Beef and chicken stew is a traditional dish consisting of beef and chicken cooked in a creamy soup."

    },

    "produ_0040": {
        "nombre": "Gordon Bleu",
        "precio": 15,
        "categoria": "lunch",
        "imagen": "Imagenes/Comidas/Lunch/gordonbleu.jpg",
        "descripcion": "El Gordon Bleu es un plato francés que consiste en pechugas de pollo rellenas de queso y empanizadas.",
        
        "nombre_es": "Gordon Bleu",
        "nombre_en": "Gordon Bleu",
        "descripcion_es": "El Gordon Bleu es un plato francés que consiste en pechugas de pollo rellenas de queso y empanizadas.",
        "descripcion_en": "Gordon Bleu is a French dish consisting of breaded chicken breasts filled with cheese."

    },
    "produ_0050": {
        "nombre": "Fajitas",
        "precio": 15,
        "categoria": "lunch",
        "imagen": "Imagenes/Comidas/Lunch/fajitas.jpg",
        "descripcion": "Las fajitas son un plato mexicano que consiste en carne (generalmente pollo o res) servida con vegetales, granos y salsas.",
        
        "nombre_es": "Fajitas",
        "nombre_en": "Fajitas",
        "descripcion_es": "Las fajitas son un plato mexicano que consiste en carne (generalmente pollo o res) servida con vegetales, granos y salsas.",
        "descripcion_en": "Fajitas are a Mexican dish consisting of meat (usually chicken or beef) served with vegetables, grains, and salsas."

    },
    "produ_0060": {
        "nombre": "Chuleta de Cerdo",
        "precio": 15,
        "categoria": "lunch",
        "imagen": "Imagenes/Comidas/Lunch/chuletadecerdo.jpg",
        "descripcion": "La chuleta de cerdo es un plato delicioso que consiste en costillas de cerdo cocinadas a la parrilla o en el horno.",
        
        "nombre_es": "Chuleta de Cerdo",
        "nombre_en": "Pork Chop",
        "descripcion_es": "La chuleta de cerdo es un plato delicioso que consiste en costillas de cerdo cocinadas a la parrilla o en el horno.",
        "descripcion_en": "Pork chop is a delicious dish consisting of pork ribs grilled or baked."

    },
    "produ_0070": {
        "nombre": "Ceviche Mixto",
        "precio": 15,
        "categoria": "lunch",
        "imagen": "Imagenes/Comidas/Lunch/cevichemixto.jpg",
        "descripcion": "El ceviche mixto es un plato peruano que consiste en pescado y camaron crudo marinado en jugo de limón y acompañado con vegetales y salsas.",
        
        "nombre_es": "Ceviche Mixto",
        "nombre_en": "Mixed Ceviche",
        "descripcion_es": "El ceviche mixto es un plato peruano que consiste en pescado y camaron crudo marinado en jugo de limón y acompañado con vegetales y salsas.",
        "descripcion_en": "Mixed ceviche is a Peruvian dish consisting of raw fish and shrimp marinated in lime juice and served with vegetables and salsas."

    },

    "produ_0080": {
        "nombre": "Pollo al Horno",
        "precio": 15,
        "categoria": "lunch",
        "imagen": "Imagenes/Comidas/Lunch/polloalhorno.jpg",
        "descripcion": "El pollo al horno es un plato sencillo y saludable que consiste en pechugas de pollo cocinadas en el horno.",
        
        "nombre_es": "Pollo al Horno",
        "nombre_en": "Baked Chicken",
        "descripcion_es": "El pollo al horno es un plato sencillo y saludable que consiste en pechugas de pollo cocinadas en el horno.",
        "descripcion_en": "Baked chicken is a simple and healthy dish consisting of chicken breasts baked in the oven."

    },
    "produ_0090": {
        "nombre": "Pollo Guisado",
        "precio": 15,
        "categoria": "lunch",
        "imagen": "Imagenes/Comidas/Lunch/polloguisado.jpg",
        "descripcion": "El pollo guisado es un plato rico y sabroso que consiste en pechugas de pollo cocinadas en una salsa cremosa.",
        
        "nombre_es": "Pollo Guisado",
        "nombre_en": "Stewed Chicken",
        "descripcion_es": "El pollo guisado es un plato rico y sabroso que consiste en pechugas de pollo cocinadas en una salsa cremosa.",
        "descripcion_en": "Stewed chicken is a rich and tasty dish consisting of chicken breasts cooked in a creamy sauce."

    },
    "produ_0100": {
        "nombre": "Pasticho",
        "precio": 15,
        "categoria": "lunch",
        "imagen": "Imagenes/Comidas/Lunch/pasticho.jpg",
        "descripcion": "El pasticho es un plato tradicional venezolano que consiste en carne molida cocinada con ingredientes especiados.",
        
        "nombre_es": "Pasticho",
        "nombre_en": "Pasticho",
        "descripcion_es": "El pasticho es un plato tradicional venezolano que consiste en carne molida cocinada con ingredientes especiados.",
        "descripcion_en": "Pasticho is a traditional Venezuelan dish consisting of ground meat cooked with seasoned ingredients."

    },

    "produ_3010": {
        "nombre": "Hamburguesa",
        "precio": 15,
        "categoria": "comida_rapida",
        "imagen": "Imagenes/Comidas/Rapidas/hamburguesa.jpg",
        "descripcion": "La hamburguesa es un plato de comida rápida que consiste en carne molida servida dentro de un pan redondo con ingredientes adicionales.",

        "nombre_es": "Hamburguesa",
        "nombre_en": "Hamburger",
        "descripcion_es": "La hamburguesa es un plato de comida rápida que consiste en carne molida servida dentro de un pan redondo con ingredientes adicionales.",
        "descripcion_en": "The hamburger is a fast food dish consisting of ground meat served inside a round bun with additional ingredients."
    },
    "produ_3020": {
        "nombre": "Arepas de Carne Mechada-Pollo",
        "precio": 15,
        "categoria": "comida_rapida",
        "imagen": "Imagenes/Comidas/Rapidas/arepas.jpg",
        "descripcion": "Combo de Tres Arepas de Carne Mechada o Pollo",
        
        "nombre_es": "Arepas de Carne Mechada-Pollo",
        "nombre_en": "Shredded Beef-Chicken Arepas",
        "descripcion_es": "Combo de Tres Arepas de Carne Mechada o Pollo",
        "descripcion_en": "Combo of Three Shredded Beef-Chicken Arepas"

    },
    "produ_3030": {
        "nombre": "Empanadas de Carne Mechada-Pollo-Queso",
        "precio": 15,
        "categoria": "comida_rapida",
        "imagen": "Imagenes/Comidas/Rapidas/empanadas.jpg",
        "descripcion": "Combo de Tres Empanadas de Carne Mechada-Pollo-Queso",
        
        "nombre_es": "Empanadas de Carne Mechada-Pollo-Queso",
        "nombre_en": "Shredded Beef-Chicken-Cheese Empanadas",
        "descripcion_es": "Combo de Tres Empanadas de Carne Mechada-Pollo-Queso",
        "descripcion_en": "Combo of Three Shredded Beef-Chicken-Cheese Empanadas"

    },

    "produ_3040": {
        "nombre": "Enrrollado de Pollo-Carne",
        "precio": 15,
        "categoria": "comida_rapida",
        "imagen": "Imagenes/Comidas/Rapidas/enrrollado.jpg",
        "descripcion": "Un delicioso enrrollado de pollo y carne, relleno con ingredientes frescos y sazonados.",
        
        "nombre_es": "Enrrollado de Pollo-Carne",
        "nombre_en": "Chicken-Beef Roll",
        "descripcion_es": "Un delicioso enrrollado de pollo y carne, relleno con ingredientes frescos y sazonados.",
        "descripcion_en": "A delicious roll filled with chicken and beef, stuffed with fresh and seasoned ingredients."

    },
    "produ_6010": {
        "nombre": "Cuatro Leches Familiar",
        "precio": 50,
        "categoria": "postres",
        "imagen": "Imagenes/Comidas/Postres/cuatroleches.jpg",
        "descripcion": "Bizcocho esponjoso y suave, bañado en una deliciosa mezcla de cuatro leches que lo hacen extra jugoso y cremoso. Cubierto con una ligera capa de crema batida y un toque especial que lo vuelve irresistible.",
        
        "nombre_es": "Cuatro Leches Familiar",
        "nombre_en": "Four Milks Family Size",
        "descripcion_es": "Bizcocho esponjoso y suave, bañado en una deliciosa mezcla de cuatro leches que lo hacen extra jugoso y cremoso. Cubierto con una ligera capa de crema batida y un toque especial que lo vuelve irresistible.",
        "descripcion_en": "Spongy and soft cake, bathed in a delicious mixture of four milks that make it extra juicy and creamy. Topped with a light layer of whipped cream and a special touch that makes it irresistible."


    },
    "produ_6020": {
        "nombre": "Cuatro Leches / Mediana",
        "precio": 35,
        "categoria": "postres",
        "imagen": "Imagenes/Comidas/Postres/cuatrolechesmediana.jpg",
        "descripcion": "Bizcocho esponjoso y suave, bañado en una deliciosa mezcla de cuatro leches que lo hacen extra jugoso y cremoso. Cubierto con una ligera capa de crema batida y un toque especial que lo vuelve irresistible.",
        
        "nombre_es": "Cuatro Leches / Mediana",
        "nombre_en": "Four Milks / Medium",
        "descripcion_es": "Bizcocho esponjoso y suave, bañado en una deliciosa mezcla de cuatro leches que lo hacen extra jugoso y cremoso. Cubierto con una ligera capa de crema batida y un toque especial que lo vuelve irresistible.",
        "descripcion_en": "Spongy and soft cake, bathed in a delicious mixture of four milks that make it extra juicy and creamy. Topped with a light layer of whipped cream and a special touch that makes it irresistible."
    },
    "produ_6030": {
        "nombre": "Cuatro Leches / Porcion 10 oz",
        "precio": 8,
        "categoria": "postres",
        "imagen": "Imagenes/Comidas/Postres/cuatrolechesporcion.jpg",
        "descripcion": "Bizcocho esponjoso y suave, bañado en una deliciosa mezcla de cuatro leches que lo hacen extra jugoso y cremoso. Cubierto con una ligera capa de crema batida y un toque especial que lo vuelve irresistible.",
        
        "nombre_es": "Cuatro Leches / Porcion 10 oz",
        "nombre_en": "Four Milks / 10 oz Portion",
        "descripcion_es": "Bizcocho esponjoso y suave, bañado en una deliciosa mezcla de cuatro leches que lo hacen extra jugoso y cremoso. Cubierto con una ligera capa de crema batida y un toque especial que lo vuelve irresistible.",
        "descripcion_en": "Spongy and soft cake, bathed in a delicious mixture of four milks that make it extra juicy and creamy. Topped with a light layer of whipped cream and a special touch that makes it irresistible."

    },
    "produ_6040": {
        "nombre": "Cuatro Leches / Docena",
        "precio": 39,
        "categoria": "postres",
        "imagen": "Imagenes/Comidas/Postres/cuatrolechesdocena.jpg",
        "descripcion": "Pide tu docena de shots de 4 leches para tus momentos especiales.",

        "nombre_es": "Cuatro Leches / Docena",
        "nombre_en": "Four Milks / Dozen",
        "descripcion_es": "Pide tu docena de shots de 4 leches para tus momentos especiales.",
        "descripcion_en": "Order your dozen of four milks shots for your special moments."
    },
    
    "produ_6050": {
        "nombre": "Ponque Mediano",
        "precio": 30,
        "categoria": "postres",
        "imagen": "Imagenes/Comidas/Postres/ponquemediano.jpg",
        "descripcion": "Nuestro PONQUE de Vainilla es esponjoso, suave y lleno de un delicioso sabor casero que encanta en cada bocado, perfecto para acompañar con un cafecito.",

        "nombre_es": "Ponque Mediano",
        "nombre_en": "Vanilla Cake / Medium",
        "descripcion_es": "Nuestro PONQUE de Vainilla es esponjoso, suave y lleno de un delicioso sabor casero que encanta en cada bocado, perfecto para acompañar con un cafecito.",
        "descripcion_en": "Our Vanilla Cake is spongy, soft, and filled with a delicious homemade flavor that delights in every bite, perfect to accompany with a cup of coffee."
    },

    "produ_6060": {
        "nombre": "Ponque Especial",
        "precio": 35,
        "categoria": "postres",
        "imagen": "Imagenes/Comidas/Postres/ponqueespecial.jpg",
        "descripcion": "Nuestro PONQUE de Vainilla es esponjoso, suave y lleno de un delicioso sabor casero que encanta en cada bocado, perfecto para acompañar con un cafecito.",

        "nombre_es": "Ponque Especial",
        "nombre_en": "Vanilla Cake / Special",
        "descripcion_es": "Nuestro PONQUE de Vainilla es esponjoso, suave y lleno de un delicioso sabor casero que encanta en cada bocado, perfecto para acompañar con un cafecito.",
        "descripcion_en": "Our Vanilla Cake is spongy, soft, and filled with a delicious homemade flavor that delights in every bite, perfect to accompany with a cup of coffee."   
    },

    "produ_6070": {
        "nombre": "Ponquecitos/ Docena",
        "precio": 39,
        "categoria": "postres",
        "imagen": "Imagenes/Comidas/Postres/ponquecitos.jpg",
        "descripcion": "Docena de Ponquesitos rellenos con el más delicioso Dulce de Leche! Dozen cupcakes filled with the most delicious Dulce de Leche!",

        "nombre_es": "Ponquecitos/ Docena",
        "nombre_en": "Cupcakes / Dozen",
        "descripcion_es": "Docena de Ponquesitos rellenos con el más delicioso Dulce de Leche!",
        "descripcion_en": "Dozen cupcakes filled with the most delicious Dulce de Leche!"
        
    },
    "produ_6080": {
        "nombre": "Cuatro Leches con Fresa y Crema 12 oz",
        "precio": 12,
        "categoria": "postres",
        "imagen": "Imagenes/Comidas/Postres/cuatrolechesfresacrema.jpg",
        "descripcion": "Bizcocho esponjoso y suave, bañado en una deliciosa mezcla de cuatro leches con fresa y crema que lo hacen extra jugoso y cremoso. Cubierto con una ligera capa de crema batida y un toque especial que lo vuelve irresistible.",

        "nombre_es": "Cuatro Leches con Fresa y Crema 12 oz",
        "nombre_en": "Four Milks with Strawberry and Cream 12 oz",
        "descripcion_es": "Bizcocho esponjoso y suave, bañado en una deliciosa mezcla de cuatro leches con fresa y crema que lo hacen extra jugoso y cremoso. Cubierto con una ligera capa de crema batida y un toque especial que lo vuelve irresistible.",
        "descripcion_en": "Spongy and soft cake, bathed in a delicious blend of four milks with strawberry and cream that makes it extra juicy and creamy. Topped with a light layer of whipped cream and a special touch that makes it irresistible."
    },
    "produ_6090": {
        "nombre": "Torticas de Chocolate / Docena",
        "precio": 40,
        "categoria": "postres",
        "imagen": "Imagenes/Comidas/Postres/torticaschocolate.jpg",
        "descripcion": "Docena de Torticas de Chocolate, deliciosas y fáciles de compartir!",

        "nombre_es": "Torticas de Chocolate / Docena",
        "nombre_en": "Chocolate Cakes / Dozen",
        "descripcion_es": "Docena de Torticas de Chocolate, deliciosas y fáciles de compartir!",
        "descripcion_en": "Dozen chocolate cakes, delicious and easy to share!"

    },
    "produ_6100": {
        "nombre": "Quesillo",
        "precio": 30,
        "categoria": "postres",
        "imagen": "Imagenes/Comidas/Postres/quesillo.jpg",
        "descripcion": "Postre venezolano hecho con leche condensada, huevos y azúcar, de textura suave.",

        "nombre_es": "Quesillo",
        "nombre_en": "Quesillo",
        "descripcion_es": "Postre venezolano hecho con leche condensada, huevos y azúcar, de textura suave.",
        "descripcion_en": "Venezuelan dessert made with condensed milk, eggs and sugar, with a soft texture."
    },
    "produ_6110": {
        "nombre": "Quesillo con Coco",
        "precio": 35,
        "categoria": "postres",
        "imagen": "Imagenes/Comidas/Postres/quesillococo.jpg",
        "descripcion": "Postre venezolano hecho con leche condensada, huevos y azúcar, de textura suave.",

        "nombre_es": "Quesillo con Coco",
        "nombre_en": "Quesillo with Coconut",
        "descripcion_es": "Postre venezolano hecho con leche condensada, huevos y azúcar, de textura suave.",
        "descripcion_en": "Venezuelan dessert made with condensed milk, eggs and sugar, with a soft texture."
    },
    "produ_6120": {
        "nombre": "Mini quesillos - unidad",
        "precio": 7,
        "categoria": "postres",
        "imagen": "Imagenes/Comidas/Postres/miniquesillos.jpg",
        "descripcion": "Deliciosos mini quesillos rellenos con el más delicioso Dulce de Leche!",

        "nombre_es": "Mini quesillos - unidad",
        "nombre_en": "Mini quesillos - unit",
        "descripcion_es": "Deliciosos mini quesillos rellenos con el más delicioso Dulce de Leche!",
        "descripcion_en": "Delicious mini quesillos filled with the most delicious dulce de leche!"
    },
    "produ_6130": {
        "nombre": "Choco Quesillo",
        "precio": 6,
        "categoria": "postres",
        "imagen": "Imagenes/Comidas/Postres/piedelimonporcion.jpg",
        "descripcion": "Postre venezolano hecho con leche condensada, huevos y azúcar, de textura suave.",
        "nombre_es": "Choco Quesillo",
        "nombre_en": "Choco Quesillo",
        "descripcion_es": "Postre venezolano hecho con leche condensada, huevos y azúcar, de textura suave.",
        "descripcion_en": "Venezuelan dessert made with condensed milk, eggs and sugar, with a soft texture."
    },
    
    "produ_6130": {
        "nombre": "Pie de Limón / Docena",
        "precio": 40,
        "categoria": "postres",
        "imagen": "Imagenes/Comidas/Postres/piedelimon.jpg",
        "descripcion": "Postre cremoso y delicioso, hecho con una base de galleta, relleno de queso crema y cubierto con una capa de mousse de limón.",
        "nombre_es": "Pie de Limón / Docena",
        "nombre_en": "Lemon Pie / Dozen",
        "descripcion_es": "Postre cremoso y delicioso, hecho con una base de galleta, relleno de queso crema y cubierto con una capa de mousse de limón.",
        "descripcion_en": "Creamy and delicious dessert, made with a cookie base, filled with cream cheese and covered with a layer of lemon mousse."
    },
    
    "produ_9010": {
        "nombre": "Agua",
        "precio": 3,
        "categoria": "otros",
        "imagen": "Imagenes/Comidas/Otros/agua.jpg",
        "descripcion": "Agua mineral embotellada.",

        "nombre_es": "Agua",
        "nombre_en": "Water",
        "descripcion_es": "Agua mineral embotellada.",
        "descripcion_en": "Bottled mineral water."

    },

    "produ_9020": {
        "nombre": "Refresco",
        "precio": 3,
        "categoria": "otros",
        "imagen": "Imagenes/Comidas/Otros/refresco.jpg",
        "descripcion": "Bebida carbonatada dulce, ideal para acompañar comidas.",
        "nombre_es": "Refresco",
        "nombre_en": "Soft Drink",
        "descripcion_es": "Bebida carbonatada dulce, ideal para acompañar comidas.",
        "descripcion_en": "Sweet carbonated drink, ideal for accompanying meals."
    },

    "produ_9030": {
        "nombre": "Ponche Crema",
        "precio": 8,
        "categoria": "otros",
        "imagen": "Imagenes/Comidas/Otros/ponche.jpeg",
        "descripcion": "Bebida venezolana hecha con leche condensada, crema de leche y especias.",
        "nombre_es": "Ponche Crema",
        "nombre_en": "Ponche Cream",
        "descripcion_es": "Bebida venezolana hecha con leche condensada, crema de leche y especias.",
        "descripcion_en": "Venezuelan drink made with condensed milk, cream of milk and spices."
    },
    "produ_9040": {
        "nombre": "Pan de Jamón",
        "precio": 45,
        "categoria": "otros",
        "imagen": "Imagenes/Comidas/Otros/pandejamon.jpg",
        "descripcion": "Pan de jamón tradicional, suave y recién horneado, relleno con jamón, tocineta, aceitunas y pasas que crean el balance perfecto entre salado y dulce. ¡Disrútalo calientito, porque asi sabe mucho mejor!",
        "nombre_es": "Pan de Jamón",
        "nombre_en": "Ham Bread",
        "descripcion_es": "Pan de jamón tradicional, suave y recién horneado, relleno con jamón, tocineta, aceitunas y pasas que crean el balance perfecto entre salado y dulce. ¡Disrútalo calientito, porque asi sabe mucho mejor!",
        "descripcion_en": "Traditional ham bread, soft and freshly baked, filled with ham, bacon, olives and raisins that create the perfect balance between savory and sweet. Enjoy it warm, because that's how it tastes much better!"
    },
    "produ_9050": {
        "nombre": "Pan de Jamón Medio Kilo",
        "precio": 25,
        "categoria": "otros",
        "imagen": "Imagenes/Comidas/Otros/pandejamonmedio.jpg",
        "descripcion": "Pan de jamón especial, suave y recién horneado, relleno con jamón, tocineta, aceitunas y pasas que crean el balance perfecto entre salado y dulce. ¡Disrútalo calientito, porque asi sabe mucho mejor!",
        
        "nombre_es": "Pan de Jamón Medio Kilo",
        "nombre_en": "Half Kilo Ham Bread",
        "descripcion_es": "Pan de jamón especial, suave y recién horneado, relleno con jamón, tocineta, aceitunas y pasas que crean el balance perfecto entre salado y dulce. ¡Disrútalo calientito, porque asi sabe mucho mejor!",
        "descripcion_en": "Special ham bread, soft and freshly baked, filled with ham, bacon, olives and raisins that create the perfect balance between savory and sweet. Enjoy it warm, because that's how it tastes much better!"

    },
    "produ_9060": {
        "nombre": "Pan de Jamón Porción - 12 Rollos",
        "precio": 12,
        "categoria": "otros",
        "imagen": "Imagenes/Comidas/Otros/pandejamonporcion.jpg",
        "descripcion": "Pan de jamón porción, suave y recién horneado, relleno con jamón, tocineta, aceitunas y pasas que crean el balance perfecto entre salado y dulce. ¡Disrútalo calientito, porque asi sabe mucho mejor!",
        
        "nombre_es": "Pan de Jamón Porción - 12 Rollos",
        "nombre_en": "Ham Bread Portion - 12 Rolls",
        "descripcion_es": "Pan de jamón porción, suave y recién horneado, relleno con jamón, tocineta, aceitunas y pasas que crean el balance perfecto entre salado y dulce. ¡Disrútalo calientito, porque asi sabe mucho mejor!",
        "descripcion_en": "Ham bread portion, soft and freshly baked, filled with ham, bacon, olives and raisins that create the perfect balance between savory and sweet. Enjoy it warm, because that's how it tastes much better!"
    },
    "produ_9070": {
        "nombre": "50 - Teqenos",
        "precio": 60,
        "categoria": "otros",
        "imagen": "Imagenes/Comidas/Otros/tequenos50.jpg",
        "descripcion": "Deliciosos tequeños recién hechos, doraditos y crujientes por fuera, con queso derretido y suave por dentro.",

        "nombre_es": "50 - Teqenos",
        "nombre_en": "50 - Teqenos",
        "descripcion_es": "Deliciosos tequeños recién hechos, doraditos y crujientes por fuera, con queso derretido y suave por dentro.",
        "descripcion_en": "Delicious tequenos, freshly made, golden and crispy on the outside, with melted cheese and soft on the inside."
    },
    "produ_9080": {
        "nombre": "25 - Teqenos",
        "precio": 35,
        "categoria": "otros",
        "imagen": "Imagenes/Comidas/Otros/tequenos25.jpg",
        "descripcion": "Teqenos porción, deliciosos y recién hechos, doraditos y crujientes por fuera, con queso derretido y suave por dentro.",

        "nombre_es": "25 - Teqenos",
        "nombre_en": "25 - Teqenos",
        "descripcion_es": "Teqenos porción, deliciosos y recién hechos, doraditos y crujientes por fuera, con queso derretido y suave por dentro.",
        "descripcion_en": "Tequeno portion, delicious and freshly made, golden and crispy on the outside, with melted cheese and soft on the inside."
    },
    "produ_9090": {
        "nombre": "Salsa de Pimenton",
        "precio": 20,
        "categoria": "otros",
        "imagen": "Imagenes/Comidas/Otros/salsapimenton.jpg",
        "descripcion": "Salsa de pimentón, ideal para acompañar comidas.",

        "nombre_es": "Salsa de Pimenton",
        "nombre_en": "Pepper Sauce",
        "descripcion_es": "Salsa de pimentón, ideal para acompañar comidas.",
        "descripcion_en": "Pepper sauce, ideal for accompanying meals."
    },
    "produ_9100": {
        "nombre": "Salsa de Pina",
        "precio": 20,
        "categoria": "otros",
        "imagen": "Imagenes/Comidas/Otros/salsapina.jpg",
        "descripcion": "Salsa de pina, ideal para acompañar comidas.",
        "nombre_es": "Salsa de Pina",
        "nombre_en": "Pineapple Sauce",
        "descripcion_es": "Salsa de pina, ideal para acompañar comidas.",
        "descripcion_en": "Pineapple sauce, ideal for accompanying meals."
    },
    

}

PRODUCTOS_CUSTOM_FILE = "data/productos_custom.json"
PRODUCTOS_CUSTOM_TABLE = "productos_catalogo"


def _ruta_productos_custom() -> str:
    try:
        os.makedirs(os.path.dirname(PRODUCTOS_CUSTOM_FILE), exist_ok=True)
        with open(PRODUCTOS_CUSTOM_FILE, "a", encoding="utf-8"):
            pass
        return PRODUCTOS_CUSTOM_FILE
    except OSError:
        return "/tmp/elafood_productos_custom.json"


def _cargar_productos_custom() -> dict:
    path = _ruta_productos_custom()
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError, ValueError):
        return {}


def _guardar_productos_custom(custom: dict) -> bool:
    path = _ruta_productos_custom()
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(custom or {}, f, ensure_ascii=False, indent=2)
        return True
    except OSError:
        return False


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


def _cargar_productos_custom_supabase() -> dict:
    sb = _supabase_client()
    if sb is None:
        return {}
    try:
        resp = sb.table(PRODUCTOS_CUSTOM_TABLE).select(
            "id,nombre_es,nombre_en,descripcion_es,descripcion_en,precio,categoria,imagen,activo"
        ).eq("activo", True).execute()
        out = {}
        for row in (resp.data or []):
            pid = str(row.get("id") or "").strip()
            if pid:
                data = {
                    "nombre": (row.get("nombre_es") or "").strip(),
                    "precio": float(row.get("precio") or 0),
                    "categoria": (row.get("categoria") or "").strip(),
                    "imagen": (row.get("imagen") or "").strip(),
                    "descripcion": (row.get("descripcion_es") or "").strip(),
                    "nombre_es": (row.get("nombre_es") or "").strip(),
                    "nombre_en": (row.get("nombre_en") or "").strip(),
                    "descripcion_es": (row.get("descripcion_es") or "").strip(),
                    "descripcion_en": (row.get("descripcion_en") or "").strip(),
                }
                out[pid] = data
        return out
    except Exception:
        # Tabla ausente o permisos: fallback local.
        return {}


def _guardar_producto_custom_supabase(pid: str, data: dict) -> bool:
    sb = _supabase_client()
    if sb is None:
        return False
    try:
        sb.table(PRODUCTOS_CUSTOM_TABLE).upsert(
            {
                "id": pid,
                "nombre_es": data.get("nombre_es", ""),
                "nombre_en": data.get("nombre_en", ""),
                "descripcion_es": data.get("descripcion_es", ""),
                "descripcion_en": data.get("descripcion_en", ""),
                "precio": data.get("precio", 0),
                "categoria": data.get("categoria", ""),
                "imagen": data.get("imagen", ""),
                "activo": True,
            },
            on_conflict="id",
        ).execute()
        return True
    except Exception:
        return False


def _upsert_producto_supabase_detallado(pid: str, payload: dict) -> tuple[bool, str]:
    sb = _supabase_client()
    if sb is None:
        return False, "cliente Supabase no disponible (revisa SUPABASE_URL/SUPABASE_SERVICE_KEY)"
    try:
        sb.table(PRODUCTOS_CUSTOM_TABLE).upsert(
            payload,
            on_conflict="id",
        ).execute()
        return True, ""
    except Exception as e:
        return False, str(e)[:500]


def _inyectar_productos_custom_en_memoria() -> None:
    # Prioriza Supabase cuando esté disponible; mantiene fallback local.
    custom = _cargar_productos_custom()
    custom_supabase = _cargar_productos_custom_supabase()
    merged = {**custom, **custom_supabase}
    for pid, p in (merged or {}).items():
        if pid and isinstance(p, dict):
            PRODUCTOS[pid] = p


def agregar_producto_custom(
    *,
    nombre_es: str,
    nombre_en: str,
    descripcion_es: str,
    descripcion_en: str,
    precio: float,
    categoria: str,
    imagen: str,
) -> tuple[bool, str, str]:
    categoria = (categoria or "").strip()
    if categoria not in {"lunch", "comida_rapida", "postres", "otros"}:
        return False, "", "categoría inválida"
    nombre_es = (nombre_es or "").strip()
    nombre_en = (nombre_en or "").strip()
    if not nombre_es:
        return False, "", "falta nombre_es"
    if not nombre_en:
        nombre_en = nombre_es
    descripcion_es = (descripcion_es or "").strip()
    descripcion_en = (descripcion_en or "").strip() or descripcion_es
    imagen = (imagen or "").strip()
    try:
        precio_val = float(precio)
    except Exception:
        return False, "", "precio inválido"
    if precio_val <= 0:
        return False, "", "precio inválido"

    pid = f"prd_{uuid4().hex[:10]}"
    while pid in PRODUCTOS:
        pid = f"prd_{uuid4().hex[:10]}"

    data = {
        "nombre": nombre_es,
        "precio": precio_val,
        "categoria": categoria,
        "imagen": imagen,
        "descripcion": descripcion_es,
        "nombre_es": nombre_es,
        "nombre_en": nombre_en,
        "descripcion_es": descripcion_es,
        "descripcion_en": descripcion_en,
    }

    custom = _cargar_productos_custom()
    custom[pid] = data
    if not _guardar_productos_custom(custom):
        return False, "", "no se pudo guardar productos custom"
    _guardar_producto_custom_supabase(pid, data)
    PRODUCTOS[pid] = data
    return True, pid, ""


def migrar_catalogo_a_supabase(base_only: bool = True) -> tuple[int, int, list[str]]:
    """
    Migra productos del catálogo local hacia Supabase.
    Retorna (ok_count, fail_count, errores_detallados).
    """
    ok = 0
    fail = 0
    errores: list[str] = []
    for pid, data in PRODUCTOS.items():
        if base_only and not str(pid).startswith("produ_"):
            continue
        if not isinstance(data, dict):
            fail += 1
            errores.append(f"{pid}: data inválida")
            continue
        payload = {
            "id": pid,
            "nombre_es": data.get("nombre_es") or data.get("nombre") or "",
            "nombre_en": data.get("nombre_en") or data.get("nombre_es") or data.get("nombre") or "",
            "descripcion_es": data.get("descripcion_es") or data.get("descripcion") or "",
            "descripcion_en": data.get("descripcion_en") or data.get("descripcion_es") or data.get("descripcion") or "",
            "precio": data.get("precio") or 0,
            "categoria": data.get("categoria") or "",
            "imagen": data.get("imagen") or "",
            "activo": True,
        }
        ok_row, err = _upsert_producto_supabase_detallado(pid, payload)
        if ok_row:
            ok += 1
        else:
            fail += 1
            errores.append(f"{pid}: {err or 'error desconocido'}")
    return ok, fail, errores


_inyectar_productos_custom_en_memoria()


def categoria_por_nombre(nombre: str) -> str | None:
    for _pid, p in PRODUCTOS.items():
        if nombre in {
            p.get("nombre", ""),
            p.get("nombre_es", ""),
            p.get("nombre_en", ""),
        }:
            return p["categoria"]
    return None


def es_comida_lunch_o_rapida_por_nombre(nombre: str) -> bool:
    c = categoria_por_nombre(nombre)
    return c in ("lunch", "comida_rapida")


def nombre_ui_producto(p: dict) -> str:
    lang = get_lang()
    if lang == "EN":
        return p.get("nombre_en") or p.get("nombre_es") or p.get("nombre") or ""
    return p.get("nombre_es") or p.get("nombre") or p.get("nombre_en") or ""


def descripcion_ui_producto(p: dict) -> str:
    lang = get_lang()
    if lang == "EN":
        return p.get("descripcion_en") or p.get("descripcion_es") or p.get("descripcion") or ""
    return p.get("descripcion_es") or p.get("descripcion") or p.get("descripcion_en") or ""
