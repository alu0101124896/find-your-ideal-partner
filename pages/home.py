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

    set_streamlit_page_config()

    show_intro_section()
    st.markdown("---")
    show_how_it_works_section()
    st.markdown("---")
    show_why_choose_us_section()
    st.markdown("---")
    show_fast_navigation_section()
    st.markdown("---")
    show_statistics_section()
    st.markdown("---")
    show_team_section()


def set_streamlit_page_config():
    """Set up the Streamlit page configuration for this page only."""

    st.set_page_config(
        layout="centered",
    )


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

    st.write(
        "✅ Matching Científico: Basado en características comportamentales y de"
        + " compatibilidad"
    )
    st.write("✅ Datos Reales: Información actualizada de protectoras verificadas")
    st.write("✅ Proceso Rápido: Encuentra tu match en menos de 5 minutos")
    st.write("✅ Completamente Gratuito: Sin costes ocultos ni suscripciones")


def show_fast_navigation_section():
    """Display the fast navigation section of the home page."""

    st.header("Navegación rápida")

    left_column_1, right_column_1 = st.columns(2, border=True)

    with left_column_1:
        st.subheader("🔍 Sistema de Recomendación")
        st.write("Obtén tu match perfecto")
        if st.button(
            "Empezar Ahora",
            use_container_width=True,
        ):
            st.switch_page("./pages/recommendation-form.py")

    with right_column_1:
        st.subheader("📚 Catálogo de Adopción")
        st.write("Explora todos los perros disponibles")
        if st.button(
            "Ver Perros Disponibles",
            use_container_width=True,
        ):
            st.switch_page("./pages/catalog.py")

    left_column_2, right_column_2 = st.columns(2, border=True)

    with left_column_2:
        st.subheader("📊 Análisis de Datos")
        st.write("Descubre insights sobre los perros y sus características")
        if st.button(
            "Ver Análisis",
            use_container_width=True,
        ):
            st.switch_page("./pages/eda.py")

    with right_column_2:
        st.subheader("💭 Comparte tu Opinión")
        st.write("Ayúdanos a mejorar el sistema")
        if st.button(
            "Dar Feedback",
            use_container_width=True,
        ):
            st.switch_page("./pages/feedback-form.py")


def show_statistics_section():
    """Display the statistics section of the home page."""

    st.header("Estadísticas de impacto")

    st.subheader("🎯 Nuestro Compromiso con la Adopción Responsable")
    st.write(
        "En España, más de **292,000 perros** llegan cada año a protectoras. Solo el"
        + " **45%** encuentra un hogar. Nosotros trabajamos para cambiar estas"
        + " estadísticas mediante tecnología que optimiza el proceso de adopción."
    )
    st.write(
        "**Nuestra misión:** Reducir el tiempo de estancia en refugios y aumentar las"
        + " adopciones exitosas a través del matching inteligente."
    )


def show_team_section():
    """Display the team section of the home page."""

    st.header("Sobre nosotros")

    st.write(
        "Somos un pequeño grupo de estudiantes de la Escuela de Organización Industrial"
        + " (EOI) de Madrid, apasionados por la tecnología y el bienestar animal."
    )
    st.write(
        "Hemos creado esta aplicación como parte de nuestro proyecto final del Curso de"
        + " Inteligencia Artificial, con el objetivo de ayudar a las protectoras de"
        + " animales a encontrar hogares para los perros que cuidan."
    )

    st.subheader("Nuestro equipo está formado por:")
    st.write(" - **Carla San Miguel Fernández**")
    st.write(" - **Juan Antolín Jiménez**")
    st.write(" - **Sergio Tabares Hernández**")


if __name__ == "__main__":
    main()
