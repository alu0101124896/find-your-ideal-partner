# -*- coding: utf-8 -*-
"""
Interactive Pet Adoption Recommendation Web Application

This module implements a Streamlit web application for pet adoption recommendations based on user characteristics and
preferences using pre-trained neural network models. It provides a user-friendly interface for clients to fill out an
adoption form and receive personalized pet recommendations.
"""

import streamlit as st


def main():
    # Set up the Streamlit page configuration
    pg = st.navigation(
        [
            st.Page(
                "./pages/home.py",
                title="Home",
                icon="🏠",
            ),
            st.Page(
                "./pages/catalog.py",
                title="Pet Catalog",
                icon="🐾",
                url_path="catalog",
            ),
            st.Page(
                "./pages/eda.py",
                title="Exploratory Data Analysis",
                icon="📊",
            ),
            st.Page(
                "./pages/recommendation-form.py",
                title="Pet Recommendation Form",
                icon="🐶",
            ),
            st.Page(
                "./pages/feedback-form.py",
                title="Feedback Form",
                icon="✍️",
            ),
        ]
    )
    pg.run()


if __name__ == "__main__":
    main()
