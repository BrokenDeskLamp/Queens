import torch
import torch.nn as nn
import torch.optim as optim
from objective import objective_function


class BoardGeneratorModel(nn.Module):
    """
    This model takes a latent vector and produces logits for an 8x8 board,
    where for each of the 64 cells it outputs 'num_regions' logits.
    The final board is obtained by sampling (or taking argmax) from a categorical
    distribution for each cell.
    """

    def __init__(self, latent_dim=32, board_size=8, num_regions=8):
        super(BoardGeneratorModel, self).__init__()
        self.board_size = board_size
        self.num_regions = num_regions
        self.latent_dim = latent_dim

        # A simple feed-forward network that maps latent vector to a flat output
        self.fc1 = nn.Sequential(nn.Linear(latent_dim, 128), nn.ReLU())
        # The final layer outputs board_size * board_size * num_regions logits.
        self.fc2 = nn.Linear(128, board_size * board_size * num_regions)

    def forward(self, z):
        x = self.fc1(z)
        x = self.fc2(x)
        # Reshape flat vector to shape: (batch_size, board_size, board_size, num_regions)
        logits = x.view(-1, self.board_size, self.board_size, self.num_regions)
        return logits


def sample_board(model, latent_vector):
    logits = model(latent_vector)  # shape: [batch, board_size, board_size, num_regions]
    batch_size = logits.size(0)
    logits_flat = logits.view(batch_size, -1, model.num_regions)  # shape: [batch, 64, num_regions]
    distribution = torch.distributions.Categorical(logits=logits_flat)
    # Sample raw values in range 0...7
    raw_samples = distribution.sample()  # shape: [batch, 64]

    # Save the raw samples for computing log_prob
    # Optionally, for display or other purposes, shift to 1...8:
    board = raw_samples.view(batch_size, model.board_size, model.board_size) + 1
    return board, raw_samples, distribution


def train_model(model, objective_function, num_epochs=10000, latent_dim=32, lr=1e-3):
    optimizer = optim.Adam(model.parameters(), lr=lr)

    for epoch in range(num_epochs):
        optimizer.zero_grad()
        z = torch.randn(1, latent_dim)
        board, raw_samples, distribution = sample_board(model, z)

        # Convert board (the displayed version is not used for log_prob) to numpy for the objective.
        board_np = board.squeeze(0).detach().cpu().numpy()
        reward = objective_function(board_np)

        # Use raw_samples (which are in 0...7) for log_prob computation.
        log_probs = distribution.log_prob(raw_samples.view(1, -1))
        log_prob_sum = log_probs.sum()

        loss = -log_prob_sum * reward
        loss.backward()
        optimizer.step()

        if epoch % 10 == 0:
            print(f"Epoch {epoch}: Loss = {loss.item():.4f}, Reward = {reward:.4f}")


# Example usage:
if __name__ == "__main__":
    latent_dim = 32
    board_size = 8
    num_regions = 8
    model = BoardGeneratorModel(latent_dim=latent_dim, board_size=board_size, num_regions=num_regions)

    # Train the model to maximize the objective.
    train_model(model, objective_function, num_epochs=1000, latent_dim=latent_dim)

    # Once trained, generate a board.
    z = torch.randn(1, latent_dim)
    board, _ = sample_board(model, z)
    board_np = board.squeeze(0).detach().cpu().numpy()
    print("Generated board:")
    print(board_np)
    print("Done!")
