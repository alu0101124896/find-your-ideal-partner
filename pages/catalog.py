# -*- coding: utf-8 -*-
"""
# ToDo: Add a brief description of the catalog page functionality and purpose.
"""

from itertools import batched
from pathlib import Path

import streamlit as st

try:
    from src.ml_models import load_dataset
except ImportError:
    from ..src.ml_models import load_dataset


def main():
    set_streamlit_page_config()

    if "dogs_df" not in st.session_state:
        # Load the dataset and store it in the session state
        st.session_state.dogs_df = load_dataset(
            Path("./data/kiwoko_dogs_data-2025-06-27_12-56-43.csv")
        )
    if "dataset_iterator" not in st.session_state:
        # Create an iterator for the dataset to allow loading dogs in batches
        st.session_state.dataset_iterator = iter(
            batched(st.session_state.dogs_df.index, 3)
        )

    st.title("Catalogo de Perros en Adopción")
    st.write(
        "Aquí puedes ver todos los perros disponibles para adopción. Puedes navegar por"
        + " el catálogo y ver la información destacada de cada perro."
    )

    st.write("---")  # Separator between rows

    for current_batch in st.session_state.dataset_iterator:
        col1, col2, col3 = st.columns(3)

        with col1:
            display_dog_info(st.session_state.dogs_df.loc[current_batch[0]])

        if len(current_batch) > 1:
            with col2:
                display_dog_info(st.session_state.dogs_df.loc[current_batch[1]])

        if len(current_batch) > 2:
            with col3:
                display_dog_info(st.session_state.dogs_df.loc[current_batch[2]])

        st.write("---")  # Separator between rows


def set_streamlit_page_config():
    """Set up the Streamlit page configuration and custom styles."""
    st.set_page_config(
        layout="wide",
    )

    max_width_str = f"max-width: {80}%;"
    st.markdown(
        f"""
        <style>
            .stApp {{
                primary-color: #4bf5ff;
                background-color: #ffffff;
                secondary-background-color: #f0f2f5;
                text-color: #333333;
            }}
            .reportview-container .main .block-container{{{max_width_str}}}
        </style>
        """,
        unsafe_allow_html=True,
    )


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

        st.write(f"**Edad:** {dog['age']} años")
        st.write(f"**Tamaño:** {dog['size']}")
        st.write(f"**Provincia:** {dog['province']}")
        st.write(f"**Puede viajar:** {'Sí' if dog['can_travel'] else 'No'}")

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
