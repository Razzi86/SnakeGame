import turtle
import random

# define program constants
WIDTH = 600
HEIGHT = 600
FOOD_SIZE = 10

# dictionary for controlling player movement
offsets = {
#           x   y
    "up": (0, 20),
    "down": (0, -20),
    "left": (-20, 0),
    "right": (20, 0)
}

# Lambs makes a function that simplifies changing 
# direction editing what it does depending on the user inpit
def bind_direction_keys():
    #                      command (direction) v  -  v in response to this key
    screen.onkey(lambda: set_snake_direction("up"), "Up")
    screen.onkey(lambda: set_snake_direction("down"), "Down")
    screen.onkey(lambda: set_snake_direction("left"), "Left")
    screen.onkey(lambda: set_snake_direction("right"), "Right")
    # replaces screen.onkey(go_up, "Up")

# lambda is EXTREMELY useful for minimizing code repitiion in any projects
def set_snake_direction(direction):
    global snake_direction
    if direction == "up": # user input for direction change
        if snake_direction != "down": # no self-collision by pressing the wrong key
            snake_direction = "up" # if tests pass, snake goes up

    elif direction == "down": 
        if snake_direction != "up": 
            snake_direction = "down"

    elif direction == "left": 
        if snake_direction != "right": 
            snake_direction = "left"

    elif direction == "right": 
        if snake_direction != "left": 
            snake_direction = "right"

# def move_snake
def game_loop():
    #game loop processes user input without blocking the current game state
    stamper.clear() #clear all previous stamps, aka removes snake

    new_head = snake[-1].copy() #make a copy of the head of the snake
    # new_head = [60, x]
    # offset of particular snake direction, 0th one

    # newhead value is being incremented by the offset value labeled in the dictionary
    # changed for the direction the snake is heading in
    new_head[0] += offsets[snake_direction][0] # changes x
    new_head[1] += offsets[snake_direction][1] # changes y

    # check collisions
    if new_head in snake or new_head[0] < - WIDTH / 2 or new_head[0]  > WIDTH / 2 \
        or new_head[1] < - HEIGHT / 2 or new_head[1] > HEIGHT / 2:
        reset()

    else:
        global delay
        # add to the snake
        snake.append(new_head)

        # check if there is an immediate food collision
        if not food_collision():
            snake.pop(0) # keep the snake the same length unless fed

        # ^ basically: the snake always appends when a game loop is triggered
        # if food isn't immediately hit, it pops and cancels out the growth
        # if food is hit, the append happens and pop() isn't called

        # draw snake
        for coordinates in snake:
            stamper.goto(coordinates[0], coordinates[1])
            stamper.stamp()

        # refresh screen
        screen.title(f"Snake Game. Score: {score}")
        screen.update()

        # recursion
        turtle.ontimer(game_loop, delay) #creating a timer

# detects whether the snake has touched the food
def food_collision():
    global food_pos, score, delay
    if get_distance(snake[-1], food_pos) < 20:
        score += 1 # must be made global to add to the scope of this function
        if delay < 10:
            delay = 10
        else:
            delay -= 4
        food_pos = get_random_food_pos()
        food.goto(food_pos)
        return True
    return False

# generates random position for food within borders
def get_random_food_pos():
    x = random.randint(- WIDTH / 2 + FOOD_SIZE, WIDTH / 2 - FOOD_SIZE)
    y = random.randint(- HEIGHT / 2 + FOOD_SIZE, HEIGHT / 2 - FOOD_SIZE)
    return (x, y)

# returns distance through pythagoras theorem
def get_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    distance = ((y2-y1) ** 2 + (x2-x1) ** 2 ) ** 0.5 #pythagoras theorem
    return distance

# resets all global variables then calls game loop
# now its the code run to start the game AND reset
def reset():
    global delay, score, snake, snake_direction, food_pos
    score = 0
    delay = 100
    snake = [[0,0], [20, 0], [40, 0], [60, 0]]
    snake_direction = "up"
    food_pos = get_random_food_pos()
    food.goto(food_pos)
    game_loop()

# create a window where we'll do our drawing
screen = turtle.Screen()
screen.setup(WIDTH, HEIGHT)
screen.title("Snake")
screen.bgcolor("cyan")
screen.tracer() #disables automatic animation

# create a turtle
stamper = turtle.Turtle()
stamper.shape("square")
stamper.penup() #doesn't leave a trace as it moves
turtle.tracer(0) # DISABLES REFRESHING, REALLY IMPORTANT

# event handlers / callbacks (listens for key inputs)
screen.listen()
bind_direction_keys()

# create snake as coordinates and default score/delay
snake = [[0,0], [20, 0], [40, 0], [60, 0]]
snake_direction = "up"
delay = 100
score = 0

# draw snake
# for coordinates in snake:
    # stamper.goto(coordinates[0],coordinates[1])
    # stamper.stamp()

# Food turtle
food = turtle.Turtle()
food.shape("circle")
food.color("red")
food.shapesize(FOOD_SIZE / 20) # devide by 20 for pixel control
food.penup() # food doesnt leave a trail
food_pos = get_random_food_pos()
food.goto(food_pos)

# initial call to move snake and start game
# game_loop()
reset()

# end commands
turtle.done()

#STAMPER IS USEFUL FOR BOARD GAMES, SNAKE, MAZES, PIXEL ART
