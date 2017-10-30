from microbit import *
import random

PADDLE_LEFT = 0
PADDLE_CENTER = 1
PADDLE_RIGHT = 2
GAME_RUNNING = 0
GAME_WON = 1
GAME_LOST = 2
message = ""


# Placeholder for testing without radio
def send(msg):
    global message
    message = msg


# Placeholder for testing without radio
def receive():
    global message
    msg = message
    message = ""
    return msg


class Ball:
    def __init__(self):
        self.x = 1
        self.y = 1
        self.update_last_pos()
        self.vx = 1
        self.vy = 1
        self.passed = False

    def update(self):
        self.update_last_pos()
        self.x += self.vx
        self.y += self.vy

    def update_last_pos(self):
        self.last_x = self.x
        self.last_y = self.y


class Paddle:
    def __init__(self):
        self.state = PADDLE_RIGHT

    def get_pixels(self):
        if self.state == PADDLE_LEFT:
            return [[0, 4], [1, 4], [2, 4]]
        elif self.state == PADDLE_CENTER:
            return [[1, 4], [2, 4], [3, 4]]
        elif self.state == PADDLE_RIGHT:
            return [[2, 4], [3, 4], [4, 4]]
        else:
            return []


class Game:
    def __init__(self):
        self.ball = Ball()
        self.paddle = Paddle()
        self.state = GAME_RUNNING


def update_game(game):
    # Update the paddle
    if button_a.was_pressed() and game.paddle.state != PADDLE_LEFT:
        game.paddle.state -= 1
    if button_b.was_pressed() and game.paddle.state != PADDLE_RIGHT:
        game.paddle.state += 1
    # Check collisions
    future_x = game.ball.x + game.ball.vx
    future_y = game.ball.y + game.ball.vy
    if future_x < 0 or future_x > 4:
        game.ball.vx *= -1
    if future_y > 4:
        game.ball.passed = True
        game.state = GAME_LOST
        send("ponglost")
    if future_y < 0:
        game.ball.passed = True
        x = 4 - game.ball.x
        y = game.ball.y
        vx = -game.ball.vx
        vy = -game.ball.vy
        send("pongball {:d} {:d} {:d} {:d}".format(x, y, vx, vy))
    for coord in game.paddle.get_pixels():
        if coord[0] == int(future_x) and coord[1] == int(future_y):
            if random.randint(1, 2) == 1:
                game.ball.vx = random.randint(0, 1) * 2 - 1
            game.ball.vy *= -1
            break
    # Move ball
    if not game.ball.passed:
        game.ball.update()


def draw_game(game):
    # Clear the display for drawing
    display.clear()
    # If the ball is in our court (!passed), draw the ball (and a trail)
    if not game.ball.passed:
        display.set_pixel(game.ball.last_x, game.ball.last_y, 1)
        display.set_pixel(game.ball.x, game.ball.y, 5)
    # Draw the paddle
    for coord in game.paddle.get_pixels():
        display.set_pixel(coord[0], coord[1], 7)


def main():
    game = Game()
    while True:
        # Get radio messages
        message = receive().split(" ")
        if message[0] == "pongball":
            game.ball.x = int(message[1])
            game.ball.y = int(message[2])
            game.ball.vx = int(message[3])
            game.ball.vy = int(message[4])
            game.ball.passed = False
        if message[0] == "ponglost":
            game.state = GAME_WON
        # Update the game
        if game.state == GAME_RUNNING:
            update_game(game)
            draw_game(game)
        elif game.state == GAME_WON:
            display.show(Image.HAPPY)
        elif game.state == GAME_LOST:
            display.show(Image.SAD)
        sleep(100)


main()
