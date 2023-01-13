import turtle

class GameWindow():
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.title("Pong")
        self.screen.setup(width=858, height=525)
    
    def player_action(self, player):
        self.screen.listen()
        self.screen.onkeypress(player.up, player.upkey)
        self.screen.onkeypress(player.down, player.downkey)
        
    def gameloop(self, ball):
        pass

screen = turtle.Screen()
screen.title("Pong")
screen.setup(width=858, height=525)

class Ball:
    def __init__(self, x_pos, y_pos):
        self.ball = turtle.Turtle()
        self.box.speed(1)
        self.box.up()
        self.box.shape("circle")


class Player:
    def __init__(self, starting_pos, up="Up", down="Down"):
        self.box = turtle.Turtle()
        self.box.speed(9)
        self.box.ht()
        self.box.up()
        self.box.shape("square")
        self.box.shapesize(1, 10)
        self.box.setpos(starting_pos, self.box.ycor())
        self.box.left(90)
        self.box.st()
        self.upkey = up
        self.downkey = down
    
    def _move(self, option):
        if option == "up":
            if self.box.ycor() >= 200:
                print("No move done")
            else:
                self.box.forward(50)
        elif option == "down":
            if self.box.ycor() <= -200:
                print("No move done")
            else:
                self.box.backward(50)
        else :
            print("Invalid option")
        print(self.box.pos())
    def up(self):
        self._move("up")

    def down(self):
        self._move("down")

players = [Player(-428), Player(428, up='w', down='s')]

screen.listen()

for player in players: 
    screen.onkeypress(player.up, player.upkey)
    screen.onkeypress(player.down, player.downkey)

screen.mainloop()
