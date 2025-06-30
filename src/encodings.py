# -*- coding: utf-8 -*-
"""
Mappings for Pet Adoption Recommendation System

This module defines the mappings for pet attributes such as the pet gender, age, and size.
"""

import numpy as np


def invert_dict(d):
    """Inverts a dictionary."""
    inverted_dict = {v: (k if v is not None else "Desconocido") for k, v in d.items()}

    # Handle the case where the key is nan
    inverted_dict[np.nan] = "Desconocido"

    return inverted_dict


# Pet gender

PET_GENDER_ENCODING = {
    "Hembra": 0,
    "Macho": 1,
}
INV_PET_GENDER_ENCODING = invert_dict(PET_GENDER_ENCODING)


# Pet size

PET_SIZE_ENCODING = {
    "Enano": 0,
    "Pequeño": 1,
    "Mediano": 2,
    "Grande": 3,
    "Gigante": 4,
}
INV_PET_SIZE_ENCODING = invert_dict(PET_SIZE_ENCODING)
