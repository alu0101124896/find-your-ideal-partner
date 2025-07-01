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

    st.title("Bienvenido a la Aplicación de Recomendación de Adopción de Mascotas")
    st.write(
        "Esta aplicación te ayuda a encontrar la mascota perfecta para ti. "
        "Completa el formulario de recomendación y obtén sugerencias personalizadas."
    )

    st.header("¿Cómo funciona?")
    st.write(
        "1. Completa el formulario de recomendación con tus preferencias y características.\n"
        "2. Recibe una lista de mascotas recomendadas que se ajustan a tus necesidades.\n"
        "3. Explora el catálogo de mascotas disponibles para adopción."
    )

    st.header("Equipo del Proyecto")
    st.write(
        "Este proyecto es desarrollado por un equipo apasionado por el bienestar animal y la tecnología."
    )

    st.header("Propósito del Proyecto")
    st.write(
        "Nuestro objetivo es facilitar la adopción responsable de mascotas, "
        "conectando a personas con animales que necesitan un hogar."
    )


if __name__ == "__main__":
    main()
