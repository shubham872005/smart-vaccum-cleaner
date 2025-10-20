import tkinter as tk
import time
import random
from vacuum_agent import Environment, VacuumAgent
from PIL import Image, ImageTk

class VacuumGUI:
    def __init__(self, root, rows=5, cols=5):
        self.root = root
        self.rows = rows
        self.cols = cols
        self.env = Environment(rows, cols)
        self.agent = VacuumAgent(self.env)
        self.running = False
        self.speed = 500  # milliseconds per step
        self.start_time = None

        # Load images
        self.images = {}
        self.load_images()  # Make sure images exist in the same folder

        # Canvas
        self.canvas = tk.Canvas(root, width=cols*80, height=rows*80, bg="white")
        self.canvas.grid(row=0, column=0, rowspan=10)

        # Control frame
        self.control_frame = tk.Frame(root)
        self.control_frame.grid(row=0, column=1, sticky="n")

        self.status_label = tk.Label(self.control_frame, text="Status: Idle", font=("Arial", 12))
        self.status_label.pack(pady=5)

        self.moves_label = tk.Label(self.control_frame, text="Moves: 0", font=("Arial", 12))
        self.moves_label.pack(pady=5)

        self.progress_label = tk.Label(self.control_frame, text="Progress: 0%", font=("Arial", 12))
        self.progress_label.pack(pady=5)

        tk.Button(self.control_frame, text="Start", command=self.start).pack(pady=5)
        tk.Button(self.control_frame, text="Pause", command=self.pause).pack(pady=5)
        tk.Button(self.control_frame, text="Reset", command=self.reset).pack(pady=5)

        self.speed_slider = tk.Scale(self.control_frame, from_=100, to=1000,
                                     orient="horizontal", label="Speed (ms)",
                                     command=self.update_speed)
        self.speed_slider.set(self.speed)
        self.speed_slider.pack(pady=5)

        # Place obstacles and draw initial grid
        self.place_obstacles()
        self.update_gui()

    def load_images(self):
        """Load actual images for the simulation. Images must be in the same folder."""
        self.images["vacuum"] = ImageTk.PhotoImage(
            Image.open("vacuum_image.png").resize((80, 80)), master=self.root)
        self.images["clean"] = ImageTk.PhotoImage(
            Image.open("cleaned_tile_image.png").resize((80, 80)), master=self.root)
        self.images["dirty"] = ImageTk.PhotoImage(
            Image.open("dirty_tile_image.png").resize((80, 80)), master=self.root)
        self.images["obstacle"] = ImageTk.PhotoImage(
            Image.open("obstacle_image.png").resize((80, 80)), master=self.root)

    def place_obstacles(self, count=5):
        """Randomly place obstacles."""
        self.obstacles = set()
        while len(self.obstacles) < count:
            x, y = random.randint(0, self.rows-1), random.randint(0, self.cols-1)
            if (x, y) != (self.agent.x, self.agent.y):
                self.obstacles.add((x, y))

    def update_gui(self):
        """Draw the grid and vacuum."""
        self.canvas.delete("all")
        for i in range(self.rows):
            for j in range(self.cols):
                if (i,j) in self.obstacles:
                    self.canvas.create_image(j*80, i*80, image=self.images["obstacle"], anchor="nw")
                elif self.env.grid[i][j] == "clean":
                    self.canvas.create_image(j*80, i*80, image=self.images["clean"], anchor="nw")
                else:
                    self.canvas.create_image(j*80, i*80, image=self.images["dirty"], anchor="nw")

        # Draw vacuum
        self.canvas.create_image(self.agent.y*80, self.agent.x*80, image=self.images["vacuum"], anchor="nw")

        # Update labels
        self.moves_label.config(text=f"Moves: {self.agent.moves}")
        cleaned_cells = sum(1 for row in self.env.grid for cell in row if cell == "clean")
        total_cells = self.rows * self.cols - len(self.obstacles)
        progress = int((cleaned_cells / total_cells) * 100)
        self.progress_label.config(text=f"Progress: {progress}%")

    def start(self):
        self.running = True
        self.status_label.config(text="Status: Running")
        if self.start_time is None:
            self.start_time = time.time()
        self.simulate()

    def pause(self):
        self.running = False
        self.status_label.config(text="Status: Paused")

    def reset(self):
        self.running = False
        self.env = Environment(self.rows, self.cols)
        self.agent = VacuumAgent(self.env)
        self.agent.moves = 0
        self.start_time = None
        self.place_obstacles()
        self.status_label.config(text="Status: Idle")
        self.update_gui()

    def update_speed(self, val):
        self.speed = int(val)

    def simulate(self):
        if self.running and not self.env.is_cleaned():
            self.agent.perceive_and_act()
            self.update_gui()
            self.root.after(self.speed, self.simulate)
        elif self.env.is_cleaned():
            self.running = False
            elapsed_time = round(time.time() - self.start_time, 2) if self.start_time else 0
            self.status_label.config(text=f"Finished in {elapsed_time}s")
            print(f"Finished in {self.agent.moves} moves")


# --- Main Execution ---
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Realistic Smart Vacuum Cleaner Simulation")
    app = VacuumGUI(root, rows=6, cols=6)
    root.mainloop()
