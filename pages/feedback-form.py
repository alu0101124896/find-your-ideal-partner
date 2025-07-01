# -*- coding: utf-8 -*-
"""
# ToDo: Add a brief description of the feedback form page functionality and purpose.
"""


import streamlit as st
import streamlit.components.v1 as components

st.title("Formulario de opinón")

<iframe src="https://docs.google.com/forms/d/e/1FAIpQLSfO3vW8yXCm57oNMjySB5NsGf6bLTG3an3J2OXtJppwMVWT8A/viewform?embedded=true" width="700" height="520" frameborder="0" marginheight="0" marginwidth="0">Cargando…</iframe>
google_form_embed_code = """
<iframe src="https://docs.google.com/forms/d/e/TU_ID_DE_FORMULARIO/viewform?embedded=true" width="640" height="800" frameborder="0" marginheight="0" marginwidth="0">Cargando…</iframe>
"""

components.html(google_form_embed_code, height=800) # El 'height' aquí se refiere a la altura del componente en Streamlit

def main():
    # ToDo: Implement the feedback form page functionality
    pass


if __name__ == "__main__":
    main()
