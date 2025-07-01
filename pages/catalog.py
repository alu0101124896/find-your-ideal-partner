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


# Define visualization constants
ELEMENTS_PER_ROW = 3
ELEMENTS_PER_PAGE = 6


def main():
    """Main function to run the pet adoption catalog page of the web application."""

    init_session_state_variables()

    show_title_and_description()
    show_catalog()


def init_session_state_variables():
    """Initialize session state variables for the catalog page."""

    # Load the dogs dataset
    if "dogs_df" not in st.session_state:
        st.session_state.dogs_df = (
            load_dataset(Path("./data/kiwoko_dogs_data-2025-06-27_12-56-43.csv"))
            .dropna(
                subset=[
                    "size",
                    "img_url",
                ]
            )
            .drop(
                index=[
                    2023,
                    8706,
                    11011,
                    11221,
                    11334,
                    12385,
                    12541,
                    12780,
                    13156,
                    13377,
                    13378,
                ],
                errors="ignore",
            )
        )

    # Create an iterator for the dataset to ease the display of dogs in batches
    if "dataset_shuffled_indexes" not in st.session_state:
        st.session_state.dataset_shuffled_indexes = st.session_state.dogs_df.sample(
            frac=1,
            random_state=42,
        ).index

    if "dataset_iterator_index" not in st.session_state:
        st.session_state.dataset_iterator_index = 0


def show_title_and_description():
    """Display the title and description of the catalog page."""

    st.title("Catalogo de Perros en Adopción")
    st.write(
        "Aquí puedes ver todos los perros disponibles para adopción. Puedes navegar por"
        + " el catálogo y ver la información destacada de cada perro."
    )


def show_catalog():
    """Display the catalog of dogs available for adoption in batches of three."""

    for current_dogs_ids_batch in batched(
        st.session_state.dataset_shuffled_indexes[
            st.session_state.dataset_iterator_index : (
                st.session_state.dataset_iterator_index + ELEMENTS_PER_PAGE
            )
        ],
        ELEMENTS_PER_ROW,
    ):
        for current_column, current_dog_id in zip(
            st.columns(ELEMENTS_PER_ROW, border=True),
            current_dogs_ids_batch,
        ):
            with current_column:
                display_dog_info(st.session_state.dogs_df.loc[current_dog_id])

    left_column, center_column, right_column = st.columns(3)
    with left_column:
        st.button(
            "Anterior",
            use_container_width=True,
            disabled=st.session_state.dataset_iterator_index <= 0,
            on_click=lambda: st.session_state.update(
                dataset_iterator_index=st.session_state.dataset_iterator_index
                - ELEMENTS_PER_PAGE
            ),
        )
    with center_column:
        st.markdown(
            '<div style="text-align: center;">Página '
            + str(st.session_state.dataset_iterator_index // ELEMENTS_PER_PAGE + 1)
            + " de "
            + str(
                (len(st.session_state.dataset_shuffled_indexes) + ELEMENTS_PER_PAGE - 1)
                // ELEMENTS_PER_PAGE
            )
            + "</div>",
            unsafe_allow_html=True,
        )
    with right_column:
        st.button(
            "Siguiente",
            use_container_width=True,
            disabled=(
                st.session_state.dataset_iterator_index + ELEMENTS_PER_PAGE
                >= len(st.session_state.dataset_shuffled_indexes)
            ),
            on_click=lambda: st.session_state.update(
                dataset_iterator_index=st.session_state.dataset_iterator_index
                + ELEMENTS_PER_PAGE
            ),
        )


def display_dog_info(dog):
    """Display information about a dog in the catalog."""

    left_column, right_column = st.columns(2)

    with left_column:
        st.image(
            dog["img_url"],
            use_container_width=True,
            caption="Unavailable image" if dog["img_url"] is None else "",
        )

    with right_column:
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
