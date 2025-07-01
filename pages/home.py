# -*- coding: utf-8 -*-
"""
Interactive Pet Adoption Recommendation Web Application

This file implements the home page of a Streamlit web application for pet adoption
recommendations. It serves as the landing page for users to learn about the application,
its features, the team behind it and the reasons and purpose of the project.
"""


import streamlit as st


def main():
    """Main function to run the home page of the pet adoption recommendation web application."""

    show_intro_section()
    show_how_it_works_section()
    show_why_choose_us_section()
    show_statistics_section()
    show_team_section()


def show_intro_section():
    """Display the introduction section of the home page."""

    st.title("🐾 Encuentra a tu compañero ideal")
    st.subheader("Tu nuevo mejor amigo te está esperando!")

    st.write("*Cada perro merece un hogar, cada familia merece el perro perfecto*")
    st.write("¿Estás listo para cambiar una vida y que cambien la tuya?")
    st.write(
        "Nuestro sistema de recomendación conecta familias con perros en busca de"
        + " hogar, utilizando inteligencia artificial para conectarte con el perro"
        + " perfecto según tu estilo de vida, preferencias y características del hogar."
        + " Todo ello para garantizar el match perfecto."
    )

    if st.button(
        "COMENZAR BÚSQUEDA INTELIGENTE",
        type="primary",
        use_container_width=True,
    ):
        st.switch_page("./pages/recommendation-form.py")


def show_how_it_works_section():
    """Display the 'How it works' section of the home page."""

    st.header("¿Cómo funciona?")

    st.subheader("📝 1. Completa tu Perfil")
    st.write("\t- Cuestionario inteligente de 3 minutos")
    st.write("\t- Analizamos tu estilo de vida y preferencias")

    st.subheader("🎯 2. Recibe Recomendaciones Personalizadas")
    st.write("\t- Algoritmo de IA analiza compatibilidad")
    st.write("\t- Ranking de los 10 perros más compatibles")

    st.subheader("❤️ 3. Encuentra tu Compañero Perfecto")
    st.write("\t- Explora perfiles detallados")
    st.write("\t- Contacta directamente con protectoras")


def show_why_choose_us_section():
    """Display the 'Why choose us' section of the home page."""

    st.header("¿Por qué elegir nuestro sistema?")

    st.write("...")


def show_statistics_section():
    """Display the statistics section of the home page."""

    st.header("Estadísticas de impacto")

    st.write("...")


def show_team_section():
    """Display the team section of the home page."""

    st.header("Sobre nosotros")

    st.write("...")


if __name__ == "__main__":
    main()
