# -*- coding: utf-8 -*-
"""
Interactive Pet Adoption Recommendation Web Application

This file implements the catalog page of a Streamlit web application to display all
currently available dogs for adoption with a resume of each dog's information, an image
and a link to the dog's original page on the Kiwoko website.
"""

from itertools import batched
from pathlib import Path

import streamlit as st

try:
    from src.ml_models import load_dataset
except ImportError:
    from ..src.ml_models import load_dataset


def main():
    """Main function to run the pet adoption catalog page of the web application."""

    set_streamlit_page_config()
    init_session_state_variables()

    show_title_and_description()
    show_catalog()


def set_streamlit_page_config():
    """Set up the Streamlit page configuration for this page only."""

    st.set_page_config(
        layout="wide",
    )


def init_session_state_variables():
    """Initialize session state variables for the catalog page."""

    # Load the dogs dataset
    if "dogs_df" not in st.session_state:
        st.session_state.dogs_df = load_dataset(
            Path("./data/kiwoko_dogs_data-2025-06-27_12-56-43.csv")
        )

    # Create an iterator for the dataset to ease the display of dogs in batches
    if "dataset_iterator" not in st.session_state:
        st.session_state.dataset_iterator = iter(
            batched(st.session_state.dogs_df.index, 3)
        )


def show_title_and_description():
    """Display the title and description of the catalog page."""

    st.title("Catalogo de Perros en Adopción")
    st.write(
        "Aquí puedes ver todos los perros disponibles para adopción. Puedes navegar por"
        + " el catálogo y ver la información destacada de cada perro."
    )


def show_catalog():
    """Display the catalog of dogs available for adoption in batches of three."""

    for current_batch in st.session_state.dataset_iterator:
        col1, col2, col3 = st.columns(3, border=True)

        with col1:
            display_dog_info(st.session_state.dogs_df.loc[current_batch[0]])

        if len(current_batch) > 1:
            with col2:
                display_dog_info(st.session_state.dogs_df.loc[current_batch[1]])

        if len(current_batch) > 2:
            with col3:
                display_dog_info(st.session_state.dogs_df.loc[current_batch[2]])


def display_dog_info(dog):
    """Display information about a dog in the catalog."""

    left_col, right_col = st.columns(2)

    with left_col:
        st.image(
            dog["img_url"],
            use_container_width=True,
            caption="Unavailable image" if dog["img_url"] is None else "",
        )

    with right_col:
        st.link_button(
            label=f"**{dog["name"]}**",
            url=dog["info_url"],
        )

        st.write(f"**Edad:** {dog["age"]} años")
        st.write(f"**Tamaño:** {dog["size"]}")
        st.write(f"**Provincia:** {dog["province"]}")
        st.write(f"**Puede viajar:** {"Sí" if dog["can_travel"] else "No"}")

        emojis = []
        if dog["good_with_children"]:
            emojis.append("👶")
        if dog["good_with_dogs"]:
            emojis.append("🐶")
        if dog["good_with_cats"]:
            emojis.append("🐱")

        if len(emojis) > 0:
            st.write(" ".join(emojis))

        st.write(" 🔴 ¡Urge adopción! 🔴" if dog["urgent_adoption"] else "")


if __name__ == "__main__":
    main()
