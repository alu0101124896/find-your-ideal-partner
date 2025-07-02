# -*- coding: utf-8 -*-
"""
Questions for the Pet Adoption Recommendation System

This module defines the questions and available options for the form used in the Pet
Adoption Recommendation System.
"""


QUESTIONS = [
    {
        "question": "1. Preferencia de género del animal",
        "options": {
            "Exclusivamente hembra": 0,
            "Preferentemente hembra, pero flexible": 0.35,
            "Exclusivamente macho": 1,
            "Preferentemente macho, pero flexible": 0.65,
            "Sin preferencia de género": 0.5,
        },
    },
    {
        "question": "2. Tamaño preferido del perro",
        "options": {
            "Miniatura (ej: Chihuahua)": 0,
            "Pequeño (ej: Beagle)": 0.25,
            "Mediano (ej: Border Collie)": 0.5,
            "Grande (ej: Labrador)": 0.75,
            "Gigante (ej: Gran Danés)": 1,
        },
    },
    {
        "question": "3. Tipo de vivienda y espacio disponible",
        "options": {
            "Apartamento pequeño sin espacio exterior": 0,
            "Apartamento mediano con terraza/balcón": 0.3,
            "Apartamento grande o con patio/jardín pequeño": 0.7,
            "Casa con jardín amplio o terreno": 1,
        },
    },
    {
        "question": "4. Presupuesto mensual estimado para cuidados básicos (alimentación, accesorios)",
        "options": {
            "Menos de 50€": 0,
            "50-100€": 0.3,
            "100-200€": 0.7,
            "Más de 200€": 1,
        },
    },
    {
        "question": "5. Presupuesto disponible para gastos iniciales (adopción, esterilización, microchip)",
        "options": {
            "Menos de 50€": 0,
            "50-100€": 0.25,
            "100-150€": 0.5,
            "150-200€": 0.75,
            "Más de 200€": 1,
        },
    },
    {
        "question": "6. Situación actual con perros en el hogar",
        "options": {
            "Sin perros actualmente": 0.5,
            "Perro(s) sociable(s) con otros canes": 1,
            "Perro(s) con potencial reactividad, pero sociable(s)": 0.8,
            "Perro(s) con dificultad para socializar": 0,
            "Perro(s) PPP con dificultad para socializar": 0,
        },
    },
    {
        "question": "7. Situación actual con gatos en el hogar",
        "options": {
            "Sin gatos actualmente": 0.5,
            "Gato(s) sociable(s) con perros": 1,
            "Gato(s) con dificultad para convivir con perros": 0,
        },
    },
    {
        "question": "8. Presencia de menores en el hogar",
        "options": {
            "Menores de 10 años residiendo permanentemente": 1,
            "Visitas frecuentes de menores": 0.7,
            "Sin menores en el entorno habitual": 0.5,
        },
    },
    {
        "question": "9. Disponibilidad diaria para actividad física y compañía",
        "options": {
            "Muy limitada (paseos cortos <30 min/día)": 0,
            "Limitada pero con tiempo de calidad en casa": 0.2,
            "Moderada (2-3 paseos >30 min/día)": 0.5,
            "Amplia (paseos extensos >1h/día)": 0.8,
            "Muy amplia (actividades deportivas regulares)": 1,
        },
    },
    {
        "question": "10. Importancia del nivel de afecto y cercanía en el perro",
        "options": {
            "Característica esencial": 1,
            "Altamente deseable": 0.7,
            "Preferible pero no determinante": 0.3,
            "No prioritario en la selección": 0,
        },
    },
]
