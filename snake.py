import tkinter as tk
import random

# -------------------------
# Game settings
# -------------------------

WIDTH = 600
HEIGHT = 400
SIZE = 20
SPEED = 100

# -------------------------
# Window
# -------------------------

window = tk.Tk()
window.title("Snake Game")
window.resizable(False, False)

canvas = tk.Canvas(
    window,
    width=WIDTH,
    height=HEIGHT,
    bg="black"
)

canvas.pack()

score_label = tk.Label(
    window,
    text="Score: 0",
    font=("Arial", 16)
)

score_label.pack()

# Restart button
restart_button = tk.Button(
    window,
    text="Restart Game",
    font=("Arial", 14),
    command=lambda: restart_game()
)

# -------------------------
# Game variables
# -------------------------

snake = []
direction = "Right"
next_direction = "Right"

score = 0
food = None
game_running = False


# -------------------------
# Create food
# -------------------------

def create_food():

    while True:

        x = random.randrange(0, WIDTH, SIZE)
        y = random.randrange(0, HEIGHT, SIZE)

        if (x, y) not in snake:
            return (x, y)


# -------------------------
# Start / Restart game
# -------------------------

def restart_game():

    global snake
    global direction
    global next_direction
    global score
    global food
    global game_running

    # Reset snake
    snake = [
        (300, 200),
        (280, 200),
        (260, 200)
    ]

    # Reset direction
    direction = "Right"
    next_direction = "Right"

    # Reset score
    score = 0

    score_label.config(text="Score: 0")

    # Create new food
    food = create_food()

    # Start game
    game_running = True

    # Remove game-over text
    canvas.delete("all")

    # Hide restart button
    restart_button.pack_forget()

    # Draw game
    draw_game()

    # Start movement
    move_snake()


# -------------------------
# Keyboard controls
# -------------------------

def change_direction(event):

    global next_direction

    if not game_running:
        return

    if event.keysym == "Up" and direction != "Down":
        next_direction = "Up"

    elif event.keysym == "Down" and direction != "Up":
        next_direction = "Down"

    elif event.keysym == "Left" and direction != "Right":
        next_direction = "Left"

    elif event.keysym == "Right" and direction != "Left":
        next_direction = "Right"


window.bind("<Up>", change_direction)
window.bind("<Down>", change_direction)
window.bind("<Left>", change_direction)
window.bind("<Right>", change_direction)


# -------------------------
# Move snake
# -------------------------

def move_snake():

    global direction
    global food
    global score
    global game_running

    if not game_running:
        return

    direction = next_direction

    head_x, head_y = snake[0]

    # Calculate new head position

    if direction == "Right":
        head_x += SIZE

    elif direction == "Left":
        head_x -= SIZE

    elif direction == "Up":
        head_y -= SIZE

    elif direction == "Down":
        head_y += SIZE

    new_head = (head_x, head_y)

    # -------------------------
    # Wall collision
    # -------------------------

    if (
        head_x < 0
        or head_x >= WIDTH
        or head_y < 0
        or head_y >= HEIGHT
    ):
        game_over()
        return

    # -------------------------
    # Self collision
    # -------------------------

    if new_head in snake:
        game_over()
        return

    # Add new head
    snake.insert(0, new_head)

    # -------------------------
    # Food collision
    # -------------------------

    if new_head == food:

        score += 1

        score_label.config(
            text=f"Score: {score}"
        )

        food = create_food()

    else:

        # Remove tail
        snake.pop()

    draw_game()

    window.after(SPEED, move_snake)


# -------------------------
# Draw game
# -------------------------

def draw_game():

    canvas.delete("all")

    # Draw snake
    for index, (x, y) in enumerate(snake):

        if index == 0:

            # Head
            canvas.create_rectangle(
                x,
                y,
                x + SIZE,
                y + SIZE,
                fill="lime"
            )

        else:

            # Body
            canvas.create_rectangle(
                x,
                y,
                x + SIZE,
                y + SIZE,
                fill="green"
            )

    # Draw food
    x, y = food

    canvas.create_oval(
        x,
        y,
        x + SIZE,
        y + SIZE,
        fill="red"
    )


# -------------------------
# Game Over
# -------------------------

def game_over():

    global game_running

    game_running = False

    canvas.create_text(
        WIDTH // 2,
        HEIGHT // 2 - 30,
        text="GAME OVER",
        fill="white",
        font=("Arial", 30, "bold")
    )

    canvas.create_text(
        WIDTH // 2,
        HEIGHT // 2 + 10,
        text=f"Score: {score}",
        fill="white",
        font=("Arial", 18)
    )

    # Show restart button
    restart_button.pack(pady=10)


# -------------------------
# Start the first game
# -------------------------

restart_game()

window.mainloop()