# -*- coding: utf-8 -*-
"""
Interactive Pet Adoption Recommendation Web Application

This file implements the exploratory data analysis (EDA) page of a Streamlit web
application to display various visualizations and insights about the available pets
for adoption.
"""

from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import streamlit as st


try:
    from src.ml_models import load_dataset
    from src.encodings import (
        PET_GENDER_ENCODING,
        PET_SIZE_ENCODING,
    )
except ImportError:
    from ..src.ml_models import load_dataset
    from ..src.encodings import (
        PET_GENDER_ENCODING,
        PET_SIZE_ENCODING,
    )


def main():
    """Main function to run the EDA page of the web application."""

    set_streamlit_page_config()
    init_session_state_variables()

    show_title_and_description()
    st.write("---")
    show_eda_visualizations()


def set_streamlit_page_config():
    """Set up the Streamlit page configuration for this page only."""

    st.set_page_config(
        layout="centered",
    )


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

    # Prepare the dataset for visualization
    if "visualization_df" not in st.session_state:
        st.session_state.visualization_df = encode_dataset(st.session_state.dogs_df)

    if "gdf" not in st.session_state:
        # Load the world map for visualization
        st.session_state.gdf = gpd.read_file(
            "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/spain-provinces.geojson"
        )


def encode_dataset(dogs_df):
    """Encode categorical variables in the dataset for visualization purposes."""

    dogs_encoded_df = dogs_df.drop(
        columns=[
            "name",
            "breed",
            "description_1",
            "description_2",
            "img_url",
            "info_url",
        ]
    ).select_dtypes(include="number")

    dogs_encoded_df["is_male"] = dogs_df["gender"].map(PET_GENDER_ENCODING).astype(int)
    dogs_encoded_df["size"] = dogs_df["size"].map(PET_SIZE_ENCODING).astype(int)

    for feature in dogs_df.select_dtypes(include="boolean").columns:
        dogs_encoded_df[feature] = dogs_df[feature].astype(int)

    return dogs_encoded_df


def show_title_and_description():
    """Display the title and description of the EDA page."""

    st.title("Análisis Exploratorio de Datos (EDA)")
    st.write(
        "En esta sección, exploraremos los datos sobre las mascotas disponibles para "
        "adopción y así comprender mejor las características y tendencias del dataset."
    )


def show_eda_visualizations():
    """Display various visualizations and insights about the available pets for adoption."""

    show_age_size_gender_boxplot()
    st.write("---")
    show_choropleth_map()
    st.write("---")
    show_correlation_heatmap()


def show_age_size_gender_boxplot():
    """Display a boxplot of pet ages by size and gender."""

    st.subheader("Distribución de edades según el tamaño y el género")

    fig, ax = plt.subplots()
    sns.boxplot(
        x="size",
        y="age",
        hue="gender",
        palette=sns.color_palette("Pastel1", n_colors=2),
        data=st.session_state.dogs_df.loc[(st.session_state.dogs_df["age"] < 50)],
        ax=ax,
    )
    plt.legend(title="Género")
    ax.set_xlabel("Tamaño")
    ax.set_ylabel("Edad")
    st.pyplot(fig)


def show_choropleth_map():
    """Display a choropleth map of available dogs by province"""

    st.subheader("Mapa de disponibilidad por provincia")

    fig, ax = plt.subplots()

    dogs_per_province = (
        st.session_state.dogs_df.groupby("province", observed=True)
        .size()
        .reset_index(name="num_dogs_available")
    )
    gdf = st.session_state.gdf.merge(
        dogs_per_province,
        left_on="name",
        right_on="province",
        how="left",
    )
    gdf["num_dogs_available"] = gdf["num_dogs_available"].fillna(0)

    gdf.plot(
        column="num_dogs_available",
        ax=ax,
        legend=True,
        cmap="OrRd",
        edgecolor="black",
        linewidth=0.3,
        legend_kwds={
            "shrink": 0.8,
        },
    )
    plt.axis("off")
    st.pyplot(fig)


def show_correlation_heatmap():
    """Display a correlation heatmap of numerical features in the dataset"""

    st.subheader("Mapa de correlación entre algunas de las características")

    fig, ax = plt.subplots(figsize=(14, 14))
    corr = st.session_state.visualization_df.corr()
    sns.heatmap(
        corr,
        mask=np.triu(np.ones_like(corr, dtype=bool)),
        ax=ax,
        annot=False,
        fmt=".2f",
        cmap="coolwarm",
        square=True,
        cbar_kws={"shrink": 0.8},
        vmin=-1,
        vmax=1,
        linewidths=0.5,
    )
    st.pyplot(fig)


if __name__ == "__main__":
    main()
