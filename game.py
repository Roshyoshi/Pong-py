import turtle
from random import *
from time import sleep

def direction():
    n = 0
    while n == 0:
        n = randint(-1, 1)
    return n
    screen.update()


x_move = direction() * 2 
y_move = direction() * 2 


class GameWindow():
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.title("pong")
        self.screen.setup(width=858, height=525)
        self.screen.tracer(0)
        self.width = 858
        self.height = 525
        self.players = [Player(-399), Player(399, up='w', down='s')]
        self.ball = Ball()

        for player in self.players:
            player_action(player)

    def player_action(self, player):
        self.screen.listen()
        self.screen.onkeypress(player.up, player.upkey)
        self.screen.onkeypress(player.down, player.downkey)
        
    def gameloop(self):
        
        ball = self.ball
        players = self.players
        top_score = 0
        x_move = direction() * 2
        y_move = direction() * 2

    def move_ball():

            self.screen.update()
            top_score = max(*[player.score for player in players])
            ball.move(x_move, y_move)
            for player in players:
                if ball.abs_x_pos() > player.abs_pos:
                    for i in range(len(players)):
                        if players[i] != player:
                            players[i].score += 1
                ball.reset()
                x_move *= direction()
                y_move *= direction()

            if ball.abs_y_pos() >= 261:
                x_move *= 1
            y_move *= -1

            for player in players:
                if abs(ball.y_pos() - player.y_pos()) <= 40:
                    if abs(ball.x_pos() - player.x_pos()) <= 20:
                        x_move *= -1
                        ball.increase_speed()

screen = turtle.Screen()
screen.title("pong")
screen.setup(width=858, height=525)
screen.tracer(n=2, delay=128)

class Ball:
    def __init__(self, x_pos=0, y_pos=0):
        self.ball = turtle.Turtle()
        self.ball.ht()
        self.ball.shape("square")
        self.ball.up()
        self.ball.goto(x_pos, y_pos)
        self.ball.speed(0)
        self.ball.st()
        self.starting_x = x_pos
        self.starting_y = y_pos

    def increase_speed(self):
        current = self.ball.speed()
        if current < 10:
            self.ball.speed(current + 1)
    
    def move(self, x_move, y_move):
            self.ball.setx(self.ball.xcor() + x_move)
            self.ball.sety(self.ball.ycor() + y_move)

    def abs_x_pos(self):
        return abs(self.ball.xcor())
    
    def abs_y_pos(self):
        return abs(self.ball.ycor())

    def x_pos(self):
        return self.ball.xcor()

    def y_pos(self):
        return self.ball.ycor()

    def reset(self):
        self.ball.speed(0)
        self.ball.goto(self.starting_x, self.starting_y)
        self.ball.speed(9)

class Player:
    def __init__(self, starting_pos, up="Up", down="Down"):
        self.box = turtle.Turtle()
        self.box.speed(0)
        self.box.ht()
        self.box.up()
        self.box.shape("square")
        self.box.shapesize(stretch_len=5) 
        self.box.setpos(starting_pos, self.box.ycor())
        self.box.left(90)
        self.box.st()
        self.upkey = up
        self.downkey = down
        self.score = 0
        self.abs_pos = abs(starting_pos)
    def _move(self, option):
        if option == "Up":
            if self.box.ycor() >= 212:
                print("no move done")
            else:
                self.box.forward(20)
        elif option == "Down":
            if self.box.ycor() <= -212:
                print("no move done")
            else:
                self.box.backward(20)
        else :
            print("invalid option")
        print(self.box.pos())
    def up(self):
        self._move("Up")

    def down(self):
        self._move("Down")

    def x_pos(self):
        return self.box.xcor()

    def y_pos(self):
        return self.box.ycor()

def move_ball():
    global x_move, y_move
    screen.update()
    top_score = max(*[player.score for player in players])
    ball.move(x_move, y_move)
    for player in players:
        if ball.abs_x_pos() > player.abs_pos:
            for i in range(len(players)):
                if players[i] != player:
                    players[i].score += 1
            ball.reset()
            x_move *= direction()
            y_move *= direction()

    if ball.abs_y_pos() >= 261:
        x_move *= 1
        y_move *= -1

    for player in players:
        if abs(ball.y_pos() - player.y_pos()) <= 40:
            if abs(ball.x_pos() - player.x_pos()) <= 20:
                x_move *= -1
                ball.increase_speed()
    turtle.ontimer(move_ball, t=2)

players = [Player(-399), Player(399, up='w', down='s')]

screen.listen()

for player in players: 
    screen.onkeypress(player.up, player.upkey)
    screen.onkeypress(player.down, player.downkey)

top_score = 0
ball = Ball()
move_ball()
turtle.mainloop()



