# -*- coding: utf-8 -*-
"""
Interactive Pet Adoption Recommendation Web Application

This module implements a Streamlit web application for pet adoption recommendations based on user characteristics and
preferences using a Nearest-Neighbors search algorithm. It provides a user-friendly interface for clients to fill out an
adoption form and receive personalized pet recommendations.
"""

import streamlit as st


def main():
    # Set up the Streamlit page configuration
    pg = st.navigation(
        pages=[
            st.Page(
                "./pages/home.py",
                title="Inicio",
                icon="🏠",
            ),
            st.Page(
                "./pages/recommendation-form.py",
                title="Formulario de recomendación",
                icon="🐶",
            ),
            st.Page(
                "./pages/catalog.py",
                title="Catálogo de adopción",
                icon="🐾",
                url_path="catalog",
            ),
            st.Page(
                "./pages/eda.py",
                title="Análisis exploratorio de datos",
                icon="📊",
            ),
            st.Page(
                "./pages/feedback-form.py",
                title="Danos tu opinión!",
                icon="✍️",
            ),
        ],
        expanded=True,
    )
    pg.run()


if __name__ == "__main__":
    main()
