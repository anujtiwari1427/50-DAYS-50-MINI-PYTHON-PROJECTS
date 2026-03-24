# Ball Catching Game using Python Tkinter

from tkinter import Tk, Button, Label, Canvas
from random import randint

# Initialize main window
base = Tk()
base.title("BALL CATCHING GAME")
base.resizable(False, False)
canvas = Canvas(base, width=590, height=610, bg="lightblue")
canvas.pack()

# Game variables
ball_y_position = 0
paddle_x_position = 5
score = 0

class Ball:
    def __init__(self, canvas, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.canvas = canvas
        self.ball = canvas.create_oval(self.x1, self.y1, self.x2, self.y2, 
                                      fill="blue", tags='ball')
    
    def move_ball(self):
        collision_offset = 5
        global ball_y_position, score
        
        # Check if ball reached bottom
        if ball_y_position >= 510:
            global paddle_x_position, paddle
            # Check collision with paddle
            if (paddle_x_position - collision_offset <= self.x1 and
                paddle_x_position + 40 + collision_offset >= self.x2):
                score += 5
                canvas.delete('ball')
                start_new_ball()
            else:
                canvas.delete('ball')
                paddle.remove_paddle()
                show_game_over()
            return
        
        ball_y_position += 1
        self.canvas.move(self.ball, 0, 1)
        self.canvas.after(10, self.move_ball)

class Paddle:
    def __init__(self, canvas, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.canvas = canvas
        self.paddle = canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2,
                                            fill="green", tags='paddle')
    
    def move_paddle(self, direction):
        global paddle_x_position
        if direction == 1:  # Move right
            self.canvas.move(self.paddle, 20, 0)
            paddle_x_position += 20
        else:  # Move left
            self.canvas.move(self.paddle, -20, 0)
            paddle_x_position -= 20
    
    def remove_paddle(self):
        canvas.delete('paddle')

def start_new_ball():
    global ball_y_position
    ball_y_position = 0
    x_position = randint(0, 560)
    ball = Ball(canvas, x_position, 20, x_position + 30, 50)
    ball.move_ball()

def show_game_over():
    game_over_window = Tk()
    game_over_window.title("GAME OVER")
    game_over_window.resizable(False, False)
    game_canvas = Canvas(game_over_window, width=300, height=300, bg="white")
    game_canvas.pack()
    
    result_label = Label(game_canvas, text=f"\nGame Over!\n\nFinal Score: {score}\n\n",
                        font=("Arial", 12))
    result_label.pack()
    
    play_again_btn = Button(game_canvas, text="Play Again", bg="lightgreen",
                           command=lambda: restart_game(game_over_window))
    play_again_btn.pack(pady=5)
    
    quit_btn = Button(game_canvas, text="Quit", bg="lightcoral",
                     command=lambda: quit_game(game_over_window))
    quit_btn.pack(pady=5)

def restart_game(game_over_window):
    game_over_window.destroy()
    start_game()

def quit_game(game_over_window):
    game_over_window.destroy()
    base.destroy()

def start_game():
    global score, paddle_x_position, paddle
    score = 0
    paddle_x_position = 5
    
    # Clear canvas
    canvas.delete("all")
    
    # Create paddle
    paddle = Paddle(canvas, 5, 560, 45, 575)
    
    # Create control buttons
    right_btn = Button(canvas, text="Move Right ?", bg="lightpink",
                      command=lambda: paddle.move_paddle(1))
    right_btn.place(x=350, y=580)
    
    left_btn = Button(canvas, text="? Move Left", bg="lightpink",
                     command=lambda: paddle.move_paddle(0))
    left_btn.place(x=250, y=580)
    
    # Start first ball
    start_new_ball()
    
    # Start game loop
    base.mainloop()

# Start the game
if __name__ == "__main__":
    start_game()
