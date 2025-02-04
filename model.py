import torch
import torch.nn as nn
import torch.optim as optim
from board import Board

class BoardGeneratorModel(nn.Module):
    def __init__(self, board_size: int, num_regions: int, latent_dim: int = 32):
        super().__init__()
        self.board_size = board_size
        self.num_regions = num_regions
        self.latent_dim = latent_dim
        self.fc = nn.Sequential(
            nn.Linear(latent_dim, 128),
            nn.ReLU(),
            nn.Linear(128, board_size * board_size * num_regions)
        )

    def forward(self, z):
        logits = self.fc(z)
        logits = logits.view(-1, self.board_size, self.board_size, self.num_regions)
        board_out = torch.argmax(logits, dim=-1) + 1
        return board_out

class GenerativeBoardGenerator:
    def __init__(self, board_size: int, num_regions: int, latent_dim: int = 32):
        self.board_size = board_size
        self.latent_dim = latent_dim
        self.model = BoardGeneratorModel(board_size, num_regions, latent_dim)
        self.optimizer = optim.Adam(self.model.parameters(), lr=1e-3)

    def generate_board(self, latent_vector: torch.Tensor = None) -> Board:
        if latent_vector is None:
            latent_vector = torch.randn(1, self.latent_dim)
        with torch.no_grad():
            board_tensor = self.model(latent_vector)
        board_np = board_tensor.squeeze(0).cpu().numpy()
        board = Board(self.board_size)
        board.grid = board_np
        return board

    def train(self, objective_function, num_epochs: int = 10000):
        for epoch in range(num_epochs):
            self.optimizer.zero_grad()
            latent_vector = torch.randn(1, self.latent_dim)
            board_tensor = self.model(latent_vector)
            board_np = board_tensor.squeeze(0).cpu().numpy()
            board = Board(self.board_size)
            board.grid = board_np

            reward = objective_function(board)
            loss = -torch.tensor(reward, dtype=torch.float32)
            loss.backward()
            self.optimizer.step()

            if epoch % 1000 == 0:
                print(f"Epoch {epoch}: Loss = {loss.item():.4f}, Reward = {reward:.4f}")
