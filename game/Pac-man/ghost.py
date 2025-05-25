import random
import math

class Ghost:
    def __init__(self, x, y, canvas, cell_size, color, name, offset_x, offset_y):
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y
        self.canvas = canvas
        self.cell_size = cell_size
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.color = color
        self.name = name
        self.direction = random.choice(["right", "left", "up", "down"])
        self.speed = 1
        self.id = None
        self.eye_ids = []
        self.scared = False
        self.returning = False
        self.draw()
    
    def draw(self):
        if self.id:
            self.canvas.delete(self.id)
            for eye_id in self.eye_ids:
                self.canvas.delete(eye_id)
            self.eye_ids = []
        
        x = self.offset_x + self.x * self.cell_size + self.cell_size // 2
        y = self.offset_y + self.y * self.cell_size + self.cell_size // 2
        radius = self.cell_size // 2 - 2
        
        if self.scared:
            color = "blue"
        elif self.returning:
            color = "white"
        else:
            color = self.color
        
        # Draw ghost body
        self.id = self.canvas.create_oval(
            x - radius, y - radius, 
            x + radius, y + radius, 
            fill=color, outline=color
        )
        
        # Draw eyes
        eye_radius = radius // 4
        if self.direction == "right":
            eye_x_offset = radius // 3
            eye_y_offset = -radius // 3
        elif self.direction == "left":
            eye_x_offset = -radius // 3
            eye_y_offset = -radius // 3
        elif self.direction == "up":
            eye_x_offset = 0
            eye_y_offset = -radius // 2
        else:  # down
            eye_x_offset = 0
            eye_y_offset = 0
        
        # Left eye
        left_eye = self.canvas.create_oval(
            x - eye_radius - eye_x_offset, y - eye_radius - eye_y_offset,
            x + eye_radius - eye_x_offset, y + eye_radius - eye_y_offset,
            fill="white", outline="white"
        )
        self.eye_ids.append(left_eye)
        
        # Right eye
        right_eye = self.canvas.create_oval(
            x - eye_radius + eye_x_offset, y - eye_radius - eye_y_offset,
            x + eye_radius + eye_x_offset, y + eye_radius - eye_y_offset,
            fill="white", outline="white"
        )
        self.eye_ids.append(right_eye)
        
        # Pupils
        pupil_radius = eye_radius // 2
        pupil_offset = eye_radius // 2
        
        if self.direction == "right":
            pupil_x_offset = pupil_offset
            pupil_y_offset = 0
        elif self.direction == "left":
            pupil_x_offset = -pupil_offset
            pupil_y_offset = 0
        elif self.direction == "up":
            pupil_x_offset = 0
            pupil_y_offset = -pupil_offset
        else:  # down
            pupil_x_offset = 0
            pupil_y_offset = pupil_offset
        
        # Left pupil
        left_pupil = self.canvas.create_oval(
            x - pupil_radius - eye_x_offset + pupil_x_offset, 
            y - pupil_radius - eye_y_offset + pupil_y_offset,
            x + pupil_radius - eye_x_offset + pupil_x_offset, 
            y + pupil_radius - eye_y_offset + pupil_y_offset,
            fill="black", outline="black"
        )
        self.eye_ids.append(left_pupil)
        
        # Right pupil
        right_pupil = self.canvas.create_oval(
            x - pupil_radius + eye_x_offset + pupil_x_offset, 
            y - pupil_radius - eye_y_offset + pupil_y_offset,
            x + pupil_radius + eye_x_offset + pupil_x_offset, 
            y + pupil_radius - eye_y_offset + pupil_y_offset,
            fill="black", outline="black"
        )
        self.eye_ids.append(right_pupil)
    
    def move(self, grid, pacman):
        if self.returning and self.x == self.start_x and self.y == self.start_y:
            self.returning = False
            self.scared = False
        
        possible_directions = []
        
        # Check all four directions
        directions = ["right", "left", "up", "down"]
        dx = [1, -1, 0, 0]
        dy = [0, 0, -1, 1]
        
        for i in range(4):
            new_x = self.x + dx[i]
            new_y = self.y + dy[i]
            
            # Check if the move is valid
            if (0 <= new_x < len(grid[0]) and 0 <= new_y < len(grid) and 
                grid[new_y][new_x] != 1):
                # Don't go back unless it's the only option
                if (directions[i] == "right" and self.direction == "left" or
                    directions[i] == "left" and self.direction == "right" or
                    directions[i] == "up" and self.direction == "down" or
                    directions[i] == "down" and self.direction == "up"):
                    continue
                possible_directions.append((directions[i], new_x, new_y))
        
        if not possible_directions:
            # If no valid moves, try all directions including going back
            for i in range(4):
                new_x = self.x + dx[i]
                new_y = self.y + dy[i]
                if (0 <= new_x < len(grid[0]) and 0 <= new_y < len(grid) and 
                    grid[new_y][new_x] != 1):
                    possible_directions.append((directions[i], new_x, new_y))
        
        if possible_directions:
            if self.returning:
                # When returning to base, use A* pathfinding to get back
                best_direction = self.find_path_to_base(possible_directions)
            elif self.scared:
                # When scared, move randomly
                best_direction = random.choice(possible_directions)
            else:
                # Normal behavior: chase Pac-Man or move randomly
                if random.random() < 0.7:  # 70% chance to chase
                    best_direction = self.chase_pacman(possible_directions, pacman)
                else:
                    best_direction = random.choice(possible_directions)
            
            self.direction = best_direction[0]
            self.x, self.y = best_direction[1], best_direction[2]
            self.draw()
    
    def chase_pacman(self, possible_directions, pacman):
        min_distance = float('inf')
        best_direction = None
        
        for direction, new_x, new_y in possible_directions:
            distance = math.sqrt((new_x - pacman.x) ** 2 + (new_y - pacman.y) ** 2)
            if distance < min_distance:
                min_distance = distance
                best_direction = (direction, new_x, new_y)
        
        return best_direction
    
    def find_path_to_base(self, possible_directions):
        min_distance = float('inf')
        best_direction = None
        
        for direction, new_x, new_y in possible_directions:
            distance = math.sqrt((new_x - self.start_x) ** 2 + (new_y - self.start_y) ** 2)
            if distance < min_distance:
                min_distance = distance
                best_direction = (direction, new_x, new_y)
        
        return best_direction
    
    def get_scared(self):
        self.scared = True
    
    def return_to_base(self):
        self.returning = True