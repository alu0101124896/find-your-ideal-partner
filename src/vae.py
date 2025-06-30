# -*- coding: utf-8 -*-
"""
Variational Autoencoder (VAE) for Pet Adoption Recommendation System

This module implements a Variational Autoencoder (VAE) to learn a latent representation of pet features and fill out
missing values in the user input data for pet adoption recommendations in a coherent manner.
"""

import torch
import torch.nn as nn


class VAE(nn.Module):
    """
    Variational Autoencoder (VAE) for reconstructing input data and learning a latent representation.
    This model consists of an encoder that maps input data to a latent space and a decoder that reconstructs
    the input from the latent representation. The model uses the reparameterization trick to allow backpropagation
    through the stochastic sampling process.

    Attributes:
        input_dim (int): Dimension of the input data.
        latent_dim (int): Dimension of the latent space.
        hidden_dim (int): Dimension of the hidden layers in the encoder and decoder.
    """

    def __init__(self, input_dim: int, latent_dim: int = 10, hidden_dim: int = 64):
        super(VAE, self).__init__()

        # Set the device to GPU if available, otherwise use CPU
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Save the dimensions
        self.input_dim = input_dim
        self.latent_dim = latent_dim
        self.hidden_dim = hidden_dim

        # Encoder layers
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc_mu = nn.Linear(hidden_dim, latent_dim)  # mean of latent
        self.fc_log_var = nn.Linear(hidden_dim, latent_dim)  # log variance of latent

        # Decoder layers
        self.fc2 = nn.Linear(latent_dim, hidden_dim)
        self.fc3 = nn.Linear(hidden_dim, input_dim)

    def encode(self, input_data):
        """Encode the input into a latent representation"""

        h = nn.functional.relu(self.fc1(input_data))
        mu = self.fc_mu(h)
        log_var = self.fc_log_var(h)

        return mu, log_var

    @staticmethod
    def reparameterize(mu, log_var):
        """Reparameterization trick to sample from the latent space"""

        std = torch.exp(0.5 * log_var)
        eps = torch.randn_like(std)

        return mu + eps * std

    def decode(self, z):
        """Decode the latent representation to reconstruct the input"""

        h = nn.functional.relu(self.fc2(z))

        return self.fc3(h)  # For continuous data, output raw values

    def forward(self, input_data):
        """Forward pass through the VAE"""

        mu, log_var = self.encode(input_data)
        z = self.reparameterize(mu, log_var)
        x_recon = self.decode(z)

        return x_recon, mu, log_var

    @staticmethod
    def vae_loss(recon_x, x, mu, log_var):
        """Loss function combining reconstruction loss and KL divergence"""

        recon_loss = nn.functional.mse_loss(
            recon_x, x, reduction="sum"
        )  # reconstruction loss (MSE)
        # KL divergence loss
        kld = -0.5 * torch.sum(1 + log_var - mu.pow(2) - log_var.exp())

        return recon_loss + kld

    def train_vae(self, data_loader, num_epochs=10, learning_rate=1e-3, verbose=True):
        """Function to train the VAE model"""

        # Define the optimizer parameters
        optimizer = torch.optim.Adam(
            self.parameters(), lr=learning_rate, weight_decay=1e-5
        )

        # Ensure the model is in training mode
        self.train()

        history = {}
        for epoch in range(num_epochs):
            current_epoch_total_loss = 0

            for batch in data_loader:
                batch = batch[0]  # Get the data from the DataLoader
                optimizer.zero_grad()
                recon_batch, mu, log_var = self(batch)
                loss = self.vae_loss(recon_batch, batch, mu, log_var)
                loss.backward()
                optimizer.step()
                current_epoch_total_loss += loss.item()

            # Store the loss for the current epoch
            history[epoch] = current_epoch_total_loss / len(data_loader.dataset)

            if verbose:
                print(f"Epoch {epoch + 1}, Loss: {history[epoch]:.4f}")

        return history

    def impute_missing_values(self, input_data):
        """
        Evaluate the VAE model on the given input tensor data to get the reconstructed
        output.
        Args:
            input_data (torch.Tensor): Input tensor data to be evaluated.
        Returns:
            torch.Tensor: Reconstructed output tensor from the VAE.
        """

        self.eval()

        # Ensure the input data is on the correct device
        input_data = input_data.to(self.device)

        # Generate latent representation for the client input
        with torch.no_grad():
            mu, log_var = self.encode(input_data)
            z = self.reparameterize(mu, log_var)

        # Decode the latent representation to get the reconstructed dog features
        with torch.no_grad():
            reconstructed_dog = self.decode(z)

        return reconstructed_dog
