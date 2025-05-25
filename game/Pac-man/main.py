import tkinter as tk
import random
import time

from ghost import Ghost
from pacman import PacMan

class GameBoard:
    def __init__(self, canvas, width, height):
        self.canvas = canvas
        self.width = width
        self.height = height
        
        # Calculate the best cell size to fit the maze properly
        self.grid = self.create_grid()
        grid_width = len(self.grid[0])
        grid_height = len(self.grid)
        
        # Calculate cell size to fit the screen with some padding
        self.cell_size = min(
            (width - 40) // grid_width,  # 20px padding on each side
            (height - 100) // grid_height  # 50px padding on top and bottom for score
        )
        
        # Calculate the offset to center the board
        self.offset_x = (width - (grid_width * self.cell_size)) // 2
        self.offset_y = (height - (grid_height * self.cell_size)) // 2 + 20  # Extra space for score at top
        
        self.dots = []
        self.power_pellets = []
        self.draw_board()
    
    def create_grid(self):
        # 0 = empty, 1 = wall, 2 = dot, 3 = power pellet
        # This is a simplified version of the Pac-Man maze
        grid = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 3, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 3, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1],
            [1, 2, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 2, 1],
            [1, 1, 1, 1, 2, 1, 1, 1, 0, 1, 0, 1, 1, 1, 2, 1, 1, 1, 1],
            [0, 0, 0, 1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 0, 0, 0],
            [1, 1, 1, 1, 2, 1, 0, 1, 1, 0, 1, 1, 0, 1, 2, 1, 1, 1, 1],
            [0, 0, 0, 0, 2, 0, 0, 1, 0, 0, 0, 1, 0, 0, 2, 0, 0, 0, 0],
            [1, 1, 1, 1, 2, 1, 0, 1, 1, 1, 1, 1, 0, 1, 2, 1, 1, 1, 1],
            [0, 0, 0, 1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 0, 0, 0],
            [1, 1, 1, 1, 2, 1, 0, 1, 1, 1, 1, 1, 0, 1, 2, 1, 1, 1, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1],
            [1, 3, 2, 1, 2, 2, 2, 2, 2, 0, 2, 2, 2, 2, 2, 1, 2, 3, 1],
            [1, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1],
            [1, 2, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 2, 1],
            [1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
        return grid
    
    def draw_board(self):
        # Draw background for the entire game area
        self.canvas.create_rectangle(
            self.offset_x - 10, self.offset_y - 10,
            self.offset_x + len(self.grid[0]) * self.cell_size + 10,
            self.offset_y + len(self.grid) * self.cell_size + 10,
            fill="#000033", outline="#000033"
        )
        
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                x1 = self.offset_x + x * self.cell_size
                y1 = self.offset_y + y * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                if self.grid[y][x] == 1:  # Wall
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2, 
                        fill="#0000FF", outline="#0000FF"
                    )
                elif self.grid[y][x] == 2:  # Dot
                    dot_size = self.cell_size // 8
                    dot_x = x1 + self.cell_size // 2
                    dot_y = y1 + self.cell_size // 2
                    dot_id = self.canvas.create_oval(
                        dot_x - dot_size, dot_y - dot_size,
                        dot_x + dot_size, dot_y + dot_size,
                        fill="white", outline="white"
                    )
                    self.dots.append((x, y, dot_id))
                elif self.grid[y][x] == 3:  # Power pellet
                    pellet_size = self.cell_size // 4
                    pellet_x = x1 + self.cell_size // 2
                    pellet_y = y1 + self.cell_size // 2
                    pellet_id = self.canvas.create_oval(
                        pellet_x - pellet_size, pellet_y - pellet_size,
                        pellet_x + pellet_size, pellet_y + pellet_size,
                        fill="white", outline="white"
                    )
                    self.power_pellets.append((x, y, pellet_id))
    
    def get_screen_position(self, x, y):
        """Convert grid coordinates to screen coordinates"""
        return (self.offset_x + x * self.cell_size, 
                self.offset_y + y * self.cell_size)
    
    def eat_dot(self, x, y):
        for i, (dot_x, dot_y, dot_id) in enumerate(self.dots):
            if dot_x == x and dot_y == y:
                self.canvas.delete(dot_id)
                self.dots.pop(i)
                self.grid[y][x] = 0
                return 10  # Score for eating a dot
        return 0
    
    def eat_power_pellet(self, x, y):
        for i, (pellet_x, pellet_y, pellet_id) in enumerate(self.power_pellets):
            if pellet_x == x and pellet_y == y:
                self.canvas.delete(pellet_id)
                self.power_pellets.pop(i)
                self.grid[y][x] = 0
                return 50  # Score for eating a power pellet
        return 0
    
    def get_remaining_dots(self):
        return len(self.dots) + len(self.power_pellets)

class GameController:
    def __init__(self, root):
        self.root = root
        self.root.title("Pac-Man")
        self.root.resizable(False, False)
        
        # Set a fixed window size that works well for most screens
        self.width = 600
        self.height = 700
        
        # Configure the window
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.configure(bg="black")
        
        # Create a frame for the game
        self.game_frame = tk.Frame(root, bg="black")
        self.game_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create a canvas for the game
        self.canvas = tk.Canvas(self.game_frame, width=self.width, height=self.height, bg="black", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Create the game title
        self.canvas.create_text(
            self.width // 2, 20, 
            text="PAC-MAN", 
            fill="#FFFF00", 
            font=("Arial", 24, "bold")
        )
        
        # Initialize the game board
        self.board = GameBoard(self.canvas, self.width, self.height)
        
        # Find a valid starting position for Pac-Man
        pacman_start_x, pacman_start_y = self.find_valid_position()
        self.pacman = PacMan(
            pacman_start_x, pacman_start_y, 
            self.canvas, self.board.cell_size,
            self.board.offset_x, self.board.offset_y
        )
        
        # Create ghosts
        self.ghosts = []
        ghost_colors = ["#FF0000", "#FFB8FF", "#00FFFF", "#FFB852"]  # Red, Pink, Cyan, Orange
        ghost_names = ["Blinky", "Pinky", "Inky", "Clyde"]
        
        # Find valid starting positions for ghosts
        for i in range(4):
            ghost_x, ghost_y = self.find_valid_position()
            self.ghosts.append(
                Ghost(
                    ghost_x, ghost_y, 
                    self.canvas, self.board.cell_size, 
                    ghost_colors[i], ghost_names[i],
                    self.board.offset_x, self.board.offset_y
                )
            )
        
        self.score = 0
        self.score_text = self.canvas.create_text(
            self.width // 4, 50, 
            text="SCORE: 0", 
            fill="white", 
            font=("Arial", 16, "bold")
        )
        
        # Create a visual representation of lives
        self.lives_text = self.canvas.create_text(
            3 * self.width // 4, 50, 
            text="LIVES:", 
            fill="white", 
            font=("Arial", 16, "bold")
        )
        
        self.life_icons = []
        self.update_lives_display()
        
        self.game_over = False
        self.game_won = False
        self.paused = False
        self.update_id = None
        
        # Create pause button
        self.pause_button = tk.Button(
            self.game_frame, 
            text="PAUSE", 
            font=("Arial", 12), 
            bg="#333333", 
            fg="white",
            activebackground="#555555",
            activeforeground="white",
            command=self.toggle_pause
        )
        self.pause_button.place(x=self.width - 80, y=10, width=70, height=30)
        
        # Bind arrow keys
        self.root.bind("<Left>", lambda event: self.pacman.set_direction("left"))
        self.root.bind("<Right>", lambda event: self.pacman.set_direction("right"))
        self.root.bind("<Up>", lambda event: self.pacman.set_direction("up"))
        self.root.bind("<Down>", lambda event: self.pacman.set_direction("down"))
        self.root.bind("<space>", lambda event: self.toggle_pause())
        
        # Start the game loop
        self.last_time = time.time()
        self.update()
    
    def update_lives_display(self):
        # Clear existing life icons
        for icon in self.life_icons:
            self.canvas.delete(icon)
        self.life_icons = []
        
        # Draw new life icons
        for i in range(self.pacman.lives):
            x = 3 * self.width // 4 + 60 + i * 30
            y = 50
            icon = self.canvas.create_arc(
                x - 10, y - 10, x + 10, y + 10,
                start=30, extent=300, fill="yellow"
            )
            self.life_icons.append(icon)
    
    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            self.pause_button.config(text="RESUME")
            # Show pause message
            self.pause_text = self.canvas.create_text(
                self.width // 2, self.height // 2,
                text="GAME PAUSED",
                fill="yellow",
                font=("Arial", 24, "bold")
            )
        else:
            self.pause_button.config(text="PAUSE")
            # Remove pause message
            if hasattr(self, 'pause_text'):
                self.canvas.delete(self.pause_text)
            self.last_time = time.time()  # Reset time to avoid big jumps
    
    def find_valid_position(self):
        while True:
            x = random.randint(1, len(self.board.grid[0]) - 2)
            y = random.randint(1, len(self.board.grid) - 2)
            if self.board.grid[y][x] != 1:  # Not a wall
                return x, y
    
    def update(self):
        if self.game_over or self.game_won:
            return
        
        if self.paused:
            self.update_id = self.root.after(100, self.update)
            return
        
        current_time = time.time()
        dt = current_time - self.last_time
        self.last_time = current_time
        
        # Update Pac-Man
        self.pacman.update_power_status()
        self.pacman.animate_mouth()
        self.pacman.move(self.board.grid)
        
        # Check for dots and power pellets
        dot_score = self.board.eat_dot(self.pacman.x, self.pacman.y)
        pellet_score = self.board.eat_power_pellet(self.pacman.x, self.pacman.y)
        
        if pellet_score > 0:
            self.pacman.activate_power()
            for ghost in self.ghosts:
                ghost.get_scared()
        
        self.score += dot_score + pellet_score
        self.canvas.itemconfig(self.score_text, text=f"SCORE: {self.score}")
        
        # Update ghosts
        for ghost in self.ghosts:
            ghost.move(self.board.grid, self.pacman)
            
            # Check for collision with Pac-Man
            if ghost.x == self.pacman.x and ghost.y == self.pacman.y:
                if self.pacman.powered and not ghost.returning:
                    ghost.return_to_base()
                    self.score += 200  # Score for eating a ghost
                    self.canvas.itemconfig(self.score_text, text=f"SCORE: {self.score}")
                elif not ghost.returning:
                    self.pacman.lives -= 1
                    self.update_lives_display()
                    
                    if self.pacman.lives <= 0:
                        self.game_over = True
                        self.show_game_over()
                    else:
                        # Reset positions
                        pacman_x, pacman_y = self.find_valid_position()
                        self.pacman.x, self.pacman.y = pacman_x, pacman_y
                        self.pacman.draw()
                        
                        # Show "Ready!" message
                        ready_text = self.canvas.create_text(
                            self.width // 2, self.height // 2,
                            text="READY!",
                            fill="yellow",
                            font=("Arial", 24, "bold")
                        )
                        self.root.update()
                        time.sleep(2)
                        self.canvas.delete(ready_text)
        
        # Check if all dots and power pellets are eaten
        if self.board.get_remaining_dots() == 0:
            self.game_won = True
            self.show_victory()
        
        # Schedule the next update
        self.update_id = self.root.after(100, self.update)
    
    def show_game_over(self):
        # Cancel any pending after callbacks
        if self.update_id:
            self.root.after_cancel(self.update_id)
            self.update_id = None
            
        # Create a semi-transparent overlay
        overlay = self.canvas.create_rectangle(
            0, 0, self.width, self.height,
            fill="black", stipple="gray50"
        )
        
        # Create a game over panel
        panel = self.canvas.create_rectangle(
            self.width // 4, self.height // 3 - 20,
            3 * self.width // 4, 2 * self.height // 3 + 20,
            fill="#000033", outline="#FF0000", width=3
        )
        
        # Game over text
        self.canvas.create_text(
            self.width // 2, self.height // 3,
            text="GAME OVER",
            fill="#FF0000", font=("Arial", 28, "bold")
        )
        
        self.canvas.create_text(
            self.width // 2, self.height // 2,
            text=f"FINAL SCORE: {self.score}",
            fill="white", font=("Arial", 20)
        )
        
        # Create restart button
        restart_button = tk.Button(
            self.canvas, 
            text="PLAY AGAIN", 
            font=("Arial", 16), 
            bg="#FF0000", 
            fg="white",
            activebackground="#FF3333",
            activeforeground="white",
            command=self.restart_game
        )
        restart_button_window = self.canvas.create_window(
            self.width // 2, 2 * self.height // 3 - 20,
            window=restart_button
        )
        
        # Create quit button
        quit_button = tk.Button(
            self.canvas, 
            text="QUIT", 
            font=("Arial", 16), 
            bg="#333333", 
            fg="white",
            activebackground="#555555",
            activeforeground="white",
            command=self.quit_game
        )
        quit_button_window = self.canvas.create_window(
            self.width // 2, 2 * self.height // 3 + 30,
            window=quit_button
        )
    
    def show_victory(self):
        # Cancel any pending after callbacks
        if self.update_id:
            self.root.after_cancel(self.update_id)
            self.update_id = None
            
        # Create a semi-transparent overlay
        overlay = self.canvas.create_rectangle(
            0, 0, self.width, self.height,
            fill="black", stipple="gray50"
        )
        
        # Create a victory panel
        panel = self.canvas.create_rectangle(
            self.width // 4, self.height // 3 - 20,
            3 * self.width // 4, 2 * self.height // 3 + 20,
            fill="#000033", outline="#FFFF00", width=3
        )
        
        # Victory text
        self.canvas.create_text(
            self.width // 2, self.height // 3,
            text="VICTORY!",
            fill="#FFFF00", font=("Arial", 28, "bold")
        )
        
        self.canvas.create_text(
            self.width // 2, self.height // 2,
            text=f"FINAL SCORE: {self.score}",
            fill="white", font=("Arial", 20)
        )
        
        # Create restart button
        restart_button = tk.Button(
            self.canvas, 
            text="PLAY AGAIN", 
            font=("Arial", 16), 
            bg="#FFFF00", 
            fg="black",
            activebackground="#FFFF33",
            activeforeground="black",
            command=self.restart_game
        )
        restart_button_window = self.canvas.create_window(
            self.width // 2, 2 * self.height // 3 - 20,
            window=restart_button
        )
        
        # Create quit button
        quit_button = tk.Button(
            self.canvas, 
            text="QUIT", 
            font=("Arial", 16), 
            bg="#333333", 
            fg="white",
            activebackground="#555555",
            activeforeground="white",
            command=self.quit_game
        )
        quit_button_window = self.canvas.create_window(
            self.width // 2, 2 * self.height // 3 + 30,
            window=quit_button
        )
    
    def restart_game(self):
        # Cancel any pending after callbacks
        if self.update_id:
            self.root.after_cancel(self.update_id)
            self.update_id = None
            
        # Clean up and restart
        self.root.destroy()
        new_root = tk.Tk()
        new_game = GameController(new_root)
        new_root.mainloop()
    
    def quit_game(self):
        # Cancel any pending after callbacks
        if self.update_id:
            self.root.after_cancel(self.update_id)
            self.update_id = None
        self.root.destroy()

class StartScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Pac-Man")
        self.root.resizable(False, False)
        
        # Set a fixed window size
        self.width = 600
        self.height = 700
        
        # Configure the window
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.configure(bg="black")
        
        # Create a canvas for the start screen
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg="black", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Draw the Pac-Man logo
        self.canvas.create_text(
            self.width // 2, self.height // 4,
            text="PAC-MAN",
            fill="#FFFF00",
            font=("Arial", 48, "bold")
        )
        
        # Draw Pac-Man character
        self.canvas.create_arc(
            self.width // 2 - 50, self.height // 2 - 50,
            self.width // 2 + 50, self.height // 2 + 50,
            start=30, extent=300, fill="yellow"
        )
        
        # Draw ghosts
        ghost_colors = ["#FF0000", "#FFB8FF", "#00FFFF", "#FFB852"]
        for i, color in enumerate(ghost_colors):
            x_offset = (i - 1.5) * 80
            self.canvas.create_oval(
                self.width // 2 - 30 + x_offset, self.height // 2 + 80,
                self.width // 2 + 30 + x_offset, self.height // 2 + 140,
                fill=color, outline=color
            )
            # Eyes
            self.canvas.create_oval(
                self.width // 2 - 20 + x_offset, self.height // 2 + 90,
                self.width // 2 - 10 + x_offset, self.height // 2 + 100,
                fill="white", outline="white"
            )
            self.canvas.create_oval(
                self.width // 2 + 10 + x_offset, self.height // 2 + 90,
                self.width // 2 + 20 + x_offset, self.height // 2 + 100,
                fill="white", outline="white"
            )
            # Pupils
            self.canvas.create_oval(
                self.width // 2 - 18 + x_offset, self.height // 2 + 92,
                self.width // 2 - 12 + x_offset, self.height // 2 + 98,
                fill="black", outline="black"
            )
            self.canvas.create_oval(
                self.width // 2 + 12 + x_offset, self.height // 2 + 92,
                self.width // 2 + 18 + x_offset, self.height // 2 + 98,
                fill="black", outline="black"
            )
        
        # Create start button
        start_button = tk.Button(
            self.canvas, 
            text="START GAME", 
            font=("Arial", 20), 
            bg="#FFFF00", 
            fg="black",
            activebackground="#FFFF33",
            activeforeground="black",
            command=self.start_game
        )
        start_button_window = self.canvas.create_window(
            self.width // 2, 3 * self.height // 4,
            window=start_button
        )
        
        # Create quit button
        quit_button = tk.Button(
            self.canvas, 
            text="QUIT", 
            font=("Arial", 16), 
            bg="#333333", 
            fg="white",
            activebackground="#555555",
            activeforeground="white",
            command=self.root.destroy
        )
        quit_button_window = self.canvas.create_window(
            self.width // 2, 3 * self.height // 4 + 60,
            window=quit_button
        )
        
        # Instructions
        self.canvas.create_text(
            self.width // 2, self.height - 80,
            text="Use arrow keys to move\nPress SPACE to pause",
            fill="white",
            font=("Arial", 14),
            justify="center"
        )
        
        # Copyright
        self.canvas.create_text(
            self.width // 2, self.height - 20,
            text="© 2025 Pac-Man Game",
            fill="#888888",
            font=("Arial", 10)
        )
    
    def start_game(self):
        self.root.destroy()
        new_root = tk.Tk()
        game = GameController(new_root)
        new_root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    start_screen = StartScreen(root)
    root.mainloop()