# -*- coding: utf-8 -*-
"""
Neural Network Models for Pet Adoption Recommendation System

This module implements the needed functions to set up and use the trained neural network models for the pet adoption
recommendation system. It includes functions to load the models, preprocess input data, and get pet recommendations.
"""

from pathlib import Path
import pickle

import pandas as pd
from pandas.core.dtypes.common import is_bool_dtype
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors
import torch

try:
    from src.encodings import (
        PET_GENDER_ENCODING,
        INV_PET_GENDER_ENCODING,
        PET_SIZE_ENCODING,
        INV_PET_SIZE_ENCODING,
    )
except ImportError:
    from encodings import (
        PET_GENDER_ENCODING,
        INV_PET_GENDER_ENCODING,
        PET_SIZE_ENCODING,
        INV_PET_SIZE_ENCODING,
    )


__knn_model = None
__scaler_model = None
__chars_means = None
__dogs_df = None
__dogs_train_df = None


def setup_nn_models(
    knn_model_path: Path = Path("./models/knn_dog_adoption-2025-07-01_18-10-09.pkl"),
    dogs_df_path: Path = Path("./data/kiwoko_dogs_data-2025-06-27_12-56-43.csv"),
):
    """Set up the neural network models for the application."""

    global __knn_model
    global __scaler_model
    global __chars_means
    global __dogs_df
    global __dogs_train_df

    # Load the pre-trained KNN model
    __knn_model = load_model(knn_model_path)
    assert isinstance(__knn_model, NearestNeighbors)

    # Load the dataset of pets currently available for adoption
    __dogs_df = load_dataset(dogs_df_path)
    assert isinstance(__dogs_df, pd.DataFrame)

    # Update knn model with the dataset of pets currently available for adoption
    __dogs_train_df, __scaler_model, __chars_means = retrain_knn_model(
        __knn_model, __dogs_df
    )


def load_model(model_path):
    with open(model_path, "rb") as model_file:
        model = pickle.load(model_file)

    if isinstance(model, NearestNeighbors):
        # If the model is a KNN model, ensure it is set to the correct parameters
        model_params = model.get_params()
        assert (
            model_params["n_neighbors"] == 2
        ), "KNN model must have n_neighbors set to 2"
        assert (
            model_params["algorithm"] == "auto"
        ), "KNN model must use the 'auto' algorithm"

    if isinstance(model, torch.nn.Module):
        # If the model is a PyTorch model, load it to the appropriate device
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model.to(device)

    return model


def load_dataset(file_path: Path) -> pd.DataFrame:
    """Load the dataset of pets currently available for adoption."""

    df = pd.read_csv(file_path, index_col=0)

    for feature in df.columns:
        if df[feature].dtype.name == "object":
            df[feature] = df[feature].astype("category")  # Convert boolean to int

    return df


def retrain_knn_model(
    knn_model: NearestNeighbors = None,
    dogs_df: pd.DataFrame = None,
) -> tuple[pd.DataFrame, MinMaxScaler, pd.Series]:
    """
    Retrain the KNN model with the provided dataset of pets currently available for
    adoption.

    Warning: This function will overwrite the weights of the existing KNN model with the
    new ones.
    """

    if knn_model is None:
        global __knn_model
        assert isinstance(__knn_model, NearestNeighbors)
        knn_model = __knn_model

    if dogs_df is None:
        global __dogs_df
        assert isinstance(__dogs_df, pd.DataFrame)
        dogs_df = __dogs_df

    # Preprocess the training data
    dogs_train_df, scaler_model, chars_means = preprocess_train_data(dogs_df)

    # Fit the KNN model with the preprocessed data
    knn_model.fit(dogs_train_df)

    return dogs_train_df, scaler_model, chars_means


def preprocess_train_data(
    dogs_df: pd.DataFrame = None,
) -> tuple[pd.DataFrame, MinMaxScaler, pd.Series]:
    """
    Preprocess the training data for the KNN model.

    Warning: This function will overwrite the existing scaler model with the new one.
    """

    if dogs_df is None:
        global __dogs_df
        assert isinstance(__dogs_df, pd.DataFrame)
        dogs_df = __dogs_df

    # Set categorical columns to 'category' dtype
    for feature in dogs_df.columns:
        if dogs_df[feature].dtype.name == "object":
            dogs_df[feature] = dogs_df[feature].astype("category")

    # Drop nan values, unnecessary columns from the dataset and some outliers
    dogs_filtered_df = (
        dogs_df.drop(
            columns=[
                "name",
                "breed",
                "province",  # Temporarily dropped, may be useful but needs some preprocessing
                "is_dewormed",  # Highly correlated with is_vaccinated
                "is_identified",  # Highly correlated with is_vaccinated
                "has_microchip",  # Highly correlated with is_vaccinated
                "is_affectionate",  # Highly correlated with is_sociable
                "is_sedentary",
                "description_1",
                "description_2",
                "img_url",
                "info_url",
            ]
        )
        .dropna(
            subset=[
                "size",
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

    # Encode categorical and boolean features, leave numerical features as is
    dogs_encoded_df = dogs_filtered_df.select_dtypes(include="number")

    dogs_encoded_df["is_male"] = (
        dogs_filtered_df["gender"].map(PET_GENDER_ENCODING).astype(int)
    )
    dogs_encoded_df["size"] = (
        dogs_filtered_df["size"].map(PET_SIZE_ENCODING).astype(int)
    )

    for feature in dogs_filtered_df.select_dtypes(include="boolean").columns:
        dogs_encoded_df[feature] = dogs_filtered_df[feature].astype(int)

    # Scale the numerical features
    scaler_model = MinMaxScaler(
        feature_range=(0, 1),
    )

    dogs_scaled_df = dogs_encoded_df.copy()
    dogs_scaled_df[["age", "size"]] = scaler_model.fit_transform(
        dogs_scaled_df[["age", "size"]]
    )

    # Calculate the means of the features for later use
    chars_means = dogs_scaled_df.mean()

    return dogs_scaled_df, scaler_model, chars_means


def get_pet_recommendations(
    client_answers: list[float],
    number_of_recommendations: int = 2,
    knn_model: NearestNeighbors = None,
    dogs_df: pd.DataFrame = None,
    dogs_train_df: pd.DataFrame = None,
) -> list[pd.Series]:
    """Get pet recommendations based on the given input data using a KNN model."""

    if knn_model is None:
        global __knn_model
        assert isinstance(__knn_model, NearestNeighbors)
        knn_model = __knn_model

    if dogs_df is None:
        global __dogs_df
        assert isinstance(__dogs_df, pd.DataFrame)
        dogs_df = __dogs_df

    if dogs_train_df is None:
        global __dogs_train_df
        assert isinstance(__dogs_train_df, pd.DataFrame)
        dogs_train_df = __dogs_train_df

    # Convert the client answers into the desired pet features
    pet_desired_features = client_answers_to_pet_features(client_answers)

    # Prepare the input data for the models
    preprocessed_input_data = preprocess_input_data(pet_desired_features)

    # Get recommendations using the KNN model
    pet_recommendations = [
        dogs_df.loc[dogs_train_df.iloc[recommendation_id].name]
        for recommendation_id in knn_model.kneighbors(
            preprocessed_input_data,
            n_neighbors=number_of_recommendations,
            return_distance=False,
        )[0]
    ]

    return pet_recommendations


def client_answers_to_pet_features(client_answers: list[float]) -> pd.Series:
    """
    Convert the client answers into the desired pet features for the recommendation
    system.
    """

    # Map the client input data to the pet features
    pet_features = pd.Series(
        {
            "age": ((client_answers[3] * 0.6) + (client_answers[4] * 0.4)),
            "is_male": client_answers[1],
            "size": (
                (client_answers[2] * 0.3)
                + (client_answers[3] * 0.3)
                + (client_answers[4] * 0.3)
                + (client_answers[9] * 0.1)
            ),
            "can_travel": client_answers[0],
            "urgent_adoption": client_answers[0],
            "needs_vet_care": ((client_answers[4] * 0.7) + (client_answers[9] * 0.3)),
            "is_vaccinated": client_answers[5],
            "is_healthy": ((client_answers[4] * 0.7) + (client_answers[9] * 0.3)),
            "is_sterilized": client_answers[5],
            "has_passport": client_answers[5],
            "good_with_children": client_answers[8],
            "good_with_cats": client_answers[7],
            "good_with_dogs": client_answers[6],
            "is_hyperactive": ((client_answers[3] * 0.4) + (client_answers[9] * 0.6)),
            "is_fearful": (
                (client_answers[6] * 0.3)
                + (client_answers[7] * 0.3)
                + (client_answers[8] * 0.3)
                + (client_answers[10] * 0.1)
            ),
            "is_sociable": (
                (client_answers[6] * 0.1)
                + (client_answers[8] * 0.15)
                + (client_answers[9] * 0.4)
                + (client_answers[10] * 0.35)
            ),
            "is_calm": ((client_answers[3] * 0.5) + (client_answers[9] * 0.5)),
        }
    )

    return pet_features


def preprocess_input_data(input_data: pd.Series) -> pd.DataFrame:
    """Preprocess the input data for the machine learning models."""

    # Reshape the input to match the expected format for the KNN model
    preprocessed_input_data = pd.DataFrame(
        input_data.values.reshape(1, -1),
        columns=input_data.index,
    )

    return preprocessed_input_data


def encode_non_numeric_features(
    input_data: pd.Series,
    dogs_df: pd.DataFrame = None,
) -> pd.Series:
    """Encode the client input data for the machine learning models."""

    if dogs_df is None:
        global __dogs_df
        assert isinstance(__dogs_df, pd.DataFrame)
        dogs_df = __dogs_df

    encoded_input = pd.Series(dtype=float)
    for feature in input_data.index:

        # Encode categorical features to numerical values
        if feature == "gender":
            encoded_input["is_male"] = PET_GENDER_ENCODING[input_data[feature]]

        elif feature == "size":
            encoded_input[feature] = PET_SIZE_ENCODING[input_data[feature]]

        # Convert boolean values to integers (0 or 1)
        elif is_bool_dtype(dogs_df[feature].dtype):
            encoded_input[feature] = int(bool(input_data[feature]))

        # For numerical features, we can leave them the same
        else:
            encoded_input[feature] = input_data[feature]

    return encoded_input


def decode_non_numeric_features(
    input_data: pd.Series,
    dogs_df: pd.DataFrame = None,
) -> pd.Series:
    """Decode the client input data back to its original categorical values."""

    if dogs_df is None:
        global __dogs_df
        assert isinstance(__dogs_df, pd.DataFrame)
        dogs_df = __dogs_df

    decoded_input = pd.Series(dtype=object)
    for feature in input_data.index:

        # Decode categorical features back to their original values
        if feature == "is_male":
            decoded_input["gender"] = INV_PET_GENDER_ENCODING[input_data[feature]]

        elif feature == "size":
            decoded_input[feature] = INV_PET_SIZE_ENCODING[input_data[feature]]

        # Decode boolean values back to their original boolean representation
        elif is_bool_dtype(dogs_df[feature].dtype):
            decoded_input[feature] = bool(round(input_data[feature]))

        # For numerical features, we can leave them as is
        else:
            decoded_input[feature] = input_data[feature]

    return decoded_input


def fill_features_with_means(
    input_data: pd.Series,
    chars_means: pd.Series = None,
) -> pd.Series:
    """Fill missing values in the client input data with the mean of each feature."""

    if chars_means is None:
        global __chars_means
        assert isinstance(__chars_means, pd.Series)
        chars_means = __chars_means

    mean_filled_input = chars_means.copy()

    for feature in input_data.index:
        mean_filled_input[feature] = input_data[feature]

    return mean_filled_input


def scale_numerical_features(
    input_data: pd.Series,
    scaler_model: MinMaxScaler = None,
) -> pd.Series:
    """Scale the numerical features of the client input data using a pre-trained scaler model."""

    if scaler_model is None:
        global __scaler_model
        assert isinstance(__scaler_model, MinMaxScaler)
        scaler_model = __scaler_model

    scaled_input = input_data.copy()

    input_data_df = pd.DataFrame(
        scaled_input.values.reshape(1, -1),
        columns=input_data.index,
    )

    scaled_input[scaler_model.get_feature_names_out()] = scaler_model.transform(
        input_data_df[scaler_model.get_feature_names_out()]
    )[0]

    return scaled_input


def unscale_numerical_features(
    input_data: pd.Series,
    scaler_model: MinMaxScaler = None,
) -> pd.Series:
    """Unscale the numerical features of the client input data using a pre-trained scaler model."""

    if scaler_model is None:
        global __scaler_model
        assert isinstance(__scaler_model, MinMaxScaler)
        scaler_model = __scaler_model

    unscaled_input = input_data.copy()

    input_data_df = pd.DataFrame(
        unscaled_input.values.reshape(1, -1),
        columns=input_data.index,
    )

    unscaled_input[scaler_model.get_feature_names_out()] = (
        scaler_model.inverse_transform(
            input_data_df[scaler_model.get_feature_names_out()]
        )[0]
    )

    return unscaled_input
