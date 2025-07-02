# -*- coding: utf-8 -*-
"""
Interactive Pet Adoption Recommendation Web Application

This file implements the feedback form page of a Streamlit web application to collect
user feedback and opinions about the application and its features.
"""


import streamlit as st
import streamlit.components.v1 as components


def main():
    """Main function to run the feedback form page of the web application."""

    set_streamlit_page_config()

    show_feedback_form_section()


def set_streamlit_page_config():
    """Set up the Streamlit page configuration for this page only."""

    st.set_page_config(
        layout="centered",
    )


def show_feedback_form_section():
    """Display the feedback form section of the page."""

    st.title("Cuestionario de retroalimentación")

    components.html(
        """
            <iframe 
                    src="https://docs.google.com/forms/d/e/1FAIpQLSfO3vW8yXCm57oNMjySB5NsGf6bLTG3an3J2OXtJppwMVWT8A/viewform?embedded=true"
                    width="700"
                    height="600"
                    scrolling="yes"
                    frameborder="0"
                    marginheight="0"
                    marginwidth="0"
            >
                Cargando…
            </iframe>
        """,
        height=600,  # El 'height' aquí se refiere a la altura del componente en Streamlit
    )


if __name__ == "__main__":
    main()
