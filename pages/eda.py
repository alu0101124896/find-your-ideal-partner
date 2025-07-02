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
    set_seaborn_style()
    init_session_state_variables()

    show_title_and_description()
    st.write("---")
    show_eda_visualizations()


def set_streamlit_page_config():
    """Set up the Streamlit page configuration for this page only."""

    st.set_page_config(
        layout="centered",
    )


def set_seaborn_style():
    """Set the Seaborn style for visualizations."""

    sns.set_theme(
        context="paper",
        style="white",
        font_scale=1.2,
        rc={
            "axes.labelsize": 14,
            "axes.titlesize": 16,
            "xtick.labelsize": 12,
            "ytick.labelsize": 12,
        },
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
    show_health_and_care_histograms()
    st.write("---")
    show_personality_and_behavior_histograms()
    st.write("---")
    show_correlation_heatmap()


def show_age_size_gender_boxplot():
    """Display a boxplot of pet ages by size and gender."""

    st.subheader("Distribución de edades según el tamaño y el género")

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.boxplot(
        x="size",
        y="age",
        hue="gender",
        palette=sns.color_palette("Pastel1", n_colors=2),
        data=st.session_state.dogs_df.loc[(st.session_state.dogs_df["age"] < 50)],
        ax=ax,
    )

    plt.legend(title="Género", loc="upper right")
    ax.set_xlabel("Tamaño")
    ax.set_ylabel("Edad")

    plt.tight_layout()
    st.pyplot(fig)


def show_choropleth_map():
    """Display a choropleth map of available dogs by province"""

    st.subheader("Mapa de disponibilidad por provincia")

    fig, ax = plt.subplots(figsize=(10, 10))

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


def show_health_and_care_histograms():
    """Display histograms of health and care features in the dataset"""

    st.subheader("Distribución de características de salud y cuidado")

    health_and_care_features = [
        "is_healthy",
        "is_vaccinated",
        "is_dewormed",
        "is_sterilized",
        "is_identified",
        "has_microchip",
        "has_passport",
    ]
    health_and_care_stats = get_stats(health_and_care_features)

    fig, ax = plt.subplots(figsize=(8, 6))

    # Create a bar plot to visualize the distribution of health and care features
    sns.barplot(
        ax=ax,
        data=health_and_care_stats,
        x="value",
        y="count",
        hue="variable",
        palette="pastel",
        order=["True", "False"],  # Ensure the order of the bars is consistent
    )

    ax.legend(title="Características", loc="upper right")
    ax.set_xlabel("Características de salud y cuidado")
    ax.set_ylabel("Número de perros")

    plt.tight_layout()
    st.pyplot(fig)


def show_personality_and_behavior_histograms():
    """Display histograms of personality and behavior features in the dataset"""

    st.subheader("Distribución de características de personalidad y comportamiento")

    personality_and_behavior_features = [
        "is_affectionate",
        "is_hyperactive",
        "is_fearful",
        "is_sociable",
        "is_calm",
        "is_sedentary",
    ]
    personality_and_behavior_stats = get_stats(personality_and_behavior_features)

    fig, ax = plt.subplots(figsize=(8, 6))

    # Create a bar plot to visualize the distribution of health and care features
    sns.barplot(
        ax=ax,
        data=personality_and_behavior_stats,
        x="value",
        y="count",
        hue="variable",
        palette="pastel",
        order=["True", "False"],  # Ensure the order of the bars is consistent
    )

    ax.legend(title="Características", loc="upper left")
    ax.set_xlabel("Características de personalidad y comportamiento")
    ax.set_ylabel("Número de perros")

    plt.tight_layout()
    st.pyplot(fig)


def get_stats(features):
    """Get statistics for the specified features in the dataset."""

    return (
        st.session_state.dogs_df[features]
        .melt(
            value_vars=features,
        )
        .groupby(
            ["value", "variable"],
            group_keys=True,
            observed=True,
        )
        .size()
        .reset_index(name="count")
        .sort_values(
            by=["value", "variable"],
            ascending=[False, False],
        )
    )


def show_correlation_heatmap():
    """Display a correlation heatmap of numerical features in the dataset"""

    st.subheader("Mapa de correlación entre algunas de las características")

    features_correlations = st.session_state.visualization_df.corr()

    fig, ax = plt.subplots(figsize=(10, 10))

    sns.heatmap(
        features_correlations,
        ax=ax,
        mask=np.triu(np.ones_like(features_correlations, dtype=bool)),
        annot=False,
        fmt=".2f",
        cmap="coolwarm",
        square=True,
        cbar_kws={"shrink": 0.8},
        vmin=-1,
        vmax=1,
        linewidths=0.5,
    )

    plt.tight_layout()
    st.pyplot(fig)


if __name__ == "__main__":
    main()
