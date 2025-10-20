import random

class Environment:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        # randomly initialize cells as clean or dirty
        self.grid = [[random.choice(["clean", "dirty"]) for _ in range(cols)] for _ in range(rows)]

    def is_cleaned(self):
        """Check if all cells are clean."""
        return all(cell == "clean" for row in self.grid for cell in row)


class VacuumAgent:
    def __init__(self, environment):
        self.env = environment
        self.x = random.randint(0, self.env.rows - 1)
        self.y = random.randint(0, self.env.cols - 1)
        self.moves = 0

    def perceive_and_act(self):
        """Perceive environment and clean or move."""
        if self.env.grid[self.x][self.y] == "dirty":
            # Clean current cell
            self.env.grid[self.x][self.y] = "clean"
        else:
            # Move to a random direction
            self.move_randomly()
        self.moves += 1

    def move_randomly(self):
        """Move in one of four directions randomly."""
        direction = random.choice(["up", "down", "left", "right"])
        if direction == "up" and self.x > 0:
            self.x -= 1
        elif direction == "down" and self.x < self.env.rows - 1:
            self.x += 1
        elif direction == "left" and self.y > 0:
            self.y -= 1
        elif direction == "right" and self.y < self.env.cols - 1:
            self.y += 1
