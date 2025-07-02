# Find Your Ideal Partner

This project consists of the development of an AI-powered pet recommendation system, which guides users in selecting a pet that best fits their lifestyle and preferences, making the process of pet adoption more informed and personalized, and ultimately enhancing the well-being of both pets and their owners, while also reducing the number of abandoned animals and promoting responsible pet ownership.

The resulting tool is deployed as a web application using Streamlit and it's available at the next link: https://find-your-ideal-partner.streamlit.app/

## Project Structure
```sh
.
├── README.md                                               # Project documentation
├── requirements.txt                                        # List of required Python packages
├── pet_recommender_system.ipynb                            # Jupyter notebook with the dataset and AI models preparation
├── app.py                                                  # Streamlit app entry point
├── src
│   ├── encodings.py                                        # Module with the encodings for the categorical features in the dataset
│   ├── questions.py                                        # Module with the questions and answers for the recommendation form
│   ├── ml_models.py                                        # Module with auxiliary functions for machine learning models
│   └── vae.py                                              # Module with the class definition for the Variational Autoencoder (VAE) model
├── data
│   ├── kiwoko_web_scraping.ipynb                           # Jupyter notebook with the web scraping code to create the pets dataset
│   └── kiwoko_dogs_data-2025-06-27_12-56-43.csv            # CSV file with the dataset of dogs available for adoption
├── models
│   ├── knn_dog_adoption-2025-07-01_18-10-09.pkl            # Pickle file with the trained Nearest Neighbors search model for the pet recommendation system
│   └── vae_dog_adoption-2025-07-01_18-10-08.pkl            # Pickle file with the trained Variational Autoencoder (VAE) model for the NaN values imputation
├── img
│   ├── choropleth_map.png                                  # Choropleth map of Spain showing the number of dogs available for adoption by province
│   ├── health_and_care_features_distribution.png           # Distribution of health and care features in the dogs dataset
│   ├── personality_and_behavior_features_distribution.png  # Distribution of personality and behavior features in the dogs dataset
│   ├── dogs_correlation_matrix.png                         # Correlation matrix heatmap of the dogs dataset
│   └── vae_training_loss_history.png                       # Training loss history of the Variational Autoencoder (VAE) model
└── pages
    ├── home.py                                             # Streamlit page for the home screen, introducing the tool, its purpose, and some background information
    ├── recommendation-form.py                              # Streamlit page for the recommendation form, where users answer questions about their lifestyle and preferences, and receive the pet recommendations
    ├── catalog.py                                          # Streamlit page for the pet catalog, displaying all available pets for adoption
    ├── eda.py                                              # Streamlit page for the exploratory data analysis (EDA) of the pets dataset
    └── feedback-form.py                                    # Streamlit page for the feedback form, allowing users to provide feedback on the recommendations

```


## Requirements
- Python: 3.12

- NumPy: 1.26.4
- Pandas: 2.2.3
- GeoPandas: 1.1.1

- Scikit-learn: 1.6.1
- SciPy: 1.13.1
- Torch: 2.7.1

- Matplotlib: 3.10.3
- Seaborn: 0.13.2

- Streamlit: 1.46.0


Note: The provided versions are the only ones tested. Other versions may work but are not guaranteed.


### Python installation

To run this project, you need to have Python installed on your machine. You can download it from [python.org](https://www.python.org/downloads/).

Make sure to download the version 3.12 or later, as this project has been tested with Python 3.12. After downloading, follow the installation instructions for your operating system.

### Virtual Environment setup (optional but recommended)

After installing Python, it is highly recommended to create a virtual environment to manage dependencies. You can do this using the following commands:

```bash
# Create a virtual environment (optional but recommended)
python -m venv venv
```

Then, activate the virtual environment:


#### On Windows
```bash
venv\Scripts\activate
```

#### On macOS/Linux
```bash
source venv/bin/activate
```

### Python dependencies installation

Finally, install the required packages using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## Local usage

To run the Streamlit app locally, use the following command in your terminal at the root of this project directory:

```bash
streamlit run app.py
```

A new web browser tab should open with the app running. If it doesn't, you can manually open your web browser and go to `http://localhost:8501`.

The app will prompt you to answer a series of questions about your lifestyle and preferences. Based on your answers, it will recommend a pet that best suits you.
