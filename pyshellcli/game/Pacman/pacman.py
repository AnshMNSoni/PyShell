import time

class PacMan:
    def __init__(self, x, y, canvas, cell_size, offset_x, offset_y):
        self.x = x
        self.y = y
        self.canvas = canvas
        self.cell_size = cell_size
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.direction = "right"
        self.next_direction = "right"
        self.speed = 2
        self.mouth_open = True
        self.mouth_angle = 60
        self.powered = False
        self.power_time = 0
        self.lives = 3
        self.id = None
        self.draw()
        
    def draw(self):
        if self.id:
            self.canvas.delete(self.id)
        
        x = self.offset_x + self.x * self.cell_size + self.cell_size // 2
        y = self.offset_y + self.y * self.cell_size + self.cell_size // 2
        radius = self.cell_size // 2 - 2
        
        start_angle = 0
        if self.direction == "right":
            start_angle = self.mouth_angle // 2
        elif self.direction == "left":
            start_angle = 180 + self.mouth_angle // 2
        elif self.direction == "up":
            start_angle = 270 + self.mouth_angle // 2
        elif self.direction == "down":
            start_angle = 90 + self.mouth_angle // 2
        
        if self.mouth_open:
            self.id = self.canvas.create_arc(
                x - radius, y - radius, 
                x + radius, y + radius, 
                start=start_angle, 
                extent=360 - self.mouth_angle, 
                fill="yellow", outline="yellow"
            )
        else:
            self.id = self.canvas.create_oval(
                x - radius, y - radius, 
                x + radius, y + radius, 
                fill="yellow", outline="yellow"
            )
    
    def animate_mouth(self):
        self.mouth_open = not self.mouth_open
        self.draw()
    
    def move(self, grid):
        # Check if we can change to the requested direction
        new_x, new_y = self.x, self.y
        if self.next_direction == "right":
            new_x += 1
        elif self.next_direction == "left":
            new_x -= 1
        elif self.next_direction == "up":
            new_y -= 1
        elif self.next_direction == "down":
            new_y += 1
        
        # If the new direction is valid, change direction
        if 0 <= new_x < len(grid[0]) and 0 <= new_y < len(grid) and grid[new_y][new_x] != 1:
            self.direction = self.next_direction
        
        # Move in the current direction
        new_x, new_y = self.x, self.y
        if self.direction == "right":
            new_x += 1
        elif self.direction == "left":
            new_x -= 1
        elif self.direction == "up":
            new_y -= 1
        elif self.direction == "down":
            new_y += 1
        
        # Check if the move is valid
        if 0 <= new_x < len(grid[0]) and 0 <= new_y < len(grid) and grid[new_y][new_x] != 1:
            self.x, self.y = new_x, new_y
            self.draw()
            return True
        return False
    
    def set_direction(self, direction):
        self.next_direction = direction
    
    def activate_power(self):
        self.powered = True
        self.power_time = time.time()
    
    def update_power_status(self):
        if self.powered and time.time() - self.power_time > 10:  # 10 seconds of power
            self.powered = False