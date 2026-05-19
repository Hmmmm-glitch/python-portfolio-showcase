import tkinter as tk
import random

# --- GAME CONFIGURATION ---
GAME_WIDTH = 300
GAME_HEIGHT = 300
SPEED = 150  # Lower number = faster game
SPACE_SIZE = 15
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"  # Bright green
FOOD_COLOR = "#FF0000"   # Bright red
BACKGROUND_COLOR = "#000000" # Black

class Snake:
    def __init__(self, canvas):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self, canvas):
        # Pick a random grid position for food
        x = random.randint(0, int((GAME_WIDTH / SPACE_SIZE)) - 1) * SPACE_SIZE
        y = random.randint(0, int((GAME_HEIGHT / SPACE_SIZE)) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

# --- GAME LOGIC ---
def next_turn(snake, food):
    global direction, score

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    # Insert new head position
    snake.coordinates.insert(0, [x, y])
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    # Check if snake ate the food
    if x == food.coordinates[0] and y == food.coordinates[1]:
        score += 1
        score_label.config(text=f"Score: {score}")
        canvas.delete("food")
        food = Food(canvas)
    else:
        # Remove the tail if it didn't eat food
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    # Check for collisions
    if check_collisions(snake):
        game_over()
    else:
        # Keep the game loop moving automatically
        window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
    global direction
    # Prevent the snake from turning instantly into itself
    if new_direction == 'left' and direction != 'right':
        direction = new_direction
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction
    elif new_direction == 'up' and direction != 'down':
        direction = new_direction
    elif new_direction == 'down' and direction != 'up':
        direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]

    # Check if hits walls
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True

    # Check if hits its own body
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False

def game_over():
    canvas.delete(tk.ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=('sans-serif', 24, 'bold'), text="GAME OVER", fill="red", tag="gameover")

# --- GUI SETUP ---
window = tk.Tk()
window.title("Mobile Snake Game")
window.resizable(False, False)

score = 0
direction = 'down'

# Score Display
score_label = tk.Label(window, text=f"Score: {score}", font=('sans-serif', 16))
score_label.pack()

# Game Canvas Screen
canvas = tk.Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

# --- MOBILE TOUCH CONTROLS PANEL ---
# A simple grid of buttons so you can play by tapping your screen
control_frame = tk.Frame(window)
control_frame.pack(pady=10)

btn_up = tk.Button(control_frame, text="▲ UP", width=6, height=2, command=lambda: change_direction('up'))
btn_left = tk.Button(control_frame, text="◀ LEFT", width=6, height=2, command=lambda: change_direction('left'))
btn_right = tk.Button(control_frame, text="RIGHT ▶", width=6, height=2, command=lambda: change_direction('right'))
btn_down = tk.Button(control_frame, text="▼ DOWN", width=6, height=2, command=lambda: change_direction('down'))

# Grid positioning for the controller layout
btn_up.grid(row=0, column=1)
btn_left.grid(row=1, column=0)
btn_right.grid(row=1, column=2)
btn_down.grid(row=2, column=1)

# Initialize Objects
snake = Snake(canvas)
food = Food(canvas)

# Start Game
next_turn(snake, food)
window.mainloop()
