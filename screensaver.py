import os,sys
sys.path.append(os.getcwd())

import turtle
from random import random, randrange


MIN_COLOR_STEP = 30
MAX_COLOR_STEP = 100


class MyTurtle(turtle.Turtle):
    """ Helper turtle class to handle mouse clicks and keep state"""

    def __init__(self, **args):
        turtle.Turtle.__init__(self, **args)
        self._alive = True
        self._change_increment = False

    def kill_turtle(self, x, y):
        self._alive = False

    def is_alive(self):
        return self._alive

    def wants_to_change_direction(self):
        if self._change_increment:
            self._change_increment = False
            return True

        return False

    def change_increment(self, x, y):
        # print "change increment"
        self._change_increment = True


def draw_turtle(turtle, x1, y1, x2, y2, red, green, blue):
    """Change color of turtle, and draw a new line"""
    turtle.color(red, green, blue)

    turtle.up()
    turtle.goto(x1, y1)
    turtle.down()
    turtle.goto(x2, y2)


def random_increment():
    """ Return an increment to be used in x or y direction.

    To avoid no movement in any coordinate make sure that this
    never returns 0. That is that MIN_INCR + n*INCR_STEP != 0 for
    all n's
    """

    MIN_INCR = -22
    MAX_INCR = 23
    INCR_STEP = 5

    return randrange(MIN_INCR, MAX_INCR, INCR_STEP)


def draw_turtle_screensaver():
    """ Draw random lines on the screen that bounce around

    If left mouse button is clicked, bob the turtle changes
    direction. If right mouse button is clicked, bob the turtle
    is killed.
    """

    # Define or hard working turtle
    turtle_screen = turtle.Screen()
    turtle_screen.screensize()
    turtle_screen.setup(width=1.0, height=1.0)

    canvas = turtle_screen.getcanvas()
    root = canvas.winfo_toplevel()
    root.overrideredirect(1)

    bob_the_turtle = MyTurtle()
    bob_the_turtle.shape('blank')
    bob_the_turtle.speed(0)

    turtle_screen.bgcolor('black')
    turtle_screen.onclick(bob_the_turtle.kill_turtle, btn=2)
    turtle_screen.onclick(bob_the_turtle.change_increment, btn=1)

    # Get the limits for the turtle movement
    MAX_WIDTH = turtle_screen.window_width() // 2
    MAX_HEIGHT = turtle_screen.window_height() // 2

    # Set initial coordinates to the middle of the screen
    x1, y1 = 0, 0
    x2, y2 = 0, 0

    # Find random increments for change of every coordinate
    x1_incr = random_increment()
    y1_incr = random_increment()
    x2_incr = random_increment()
    y2_incr = random_increment()

    # Setup initial colors, new colors and steps between changes
    steps_before_change = randrange(MIN_COLOR_STEP, MAX_COLOR_STEP)
    red, green, blue = random(), random(), random()
    new_red, new_green, new_blue = random(), random(), random()

    red_incr = (new_red - red) / steps_before_change
    green_incr = (new_green - green) / steps_before_change
    blue_incr = (new_blue - blue) / steps_before_change

    color_steps = 0

    while (bob_the_turtle.is_alive()):

        # Change color toward new color in incremental steps
        red += red_incr
        green += green_incr
        blue += blue_incr

        color_steps += 1

        # If we've reached the new color, find a new color to go towards
        if color_steps >= steps_before_change:
            color_steps = 0

            # Switch color, find new color and new color increments
            red, green, blue = new_red, new_green, new_blue
            new_red, new_green, new_blue = random(), random(), random()

            steps_before_change = randrange(MIN_COLOR_STEP, MAX_COLOR_STEP)
            red_incr = (new_red - red) / steps_before_change
            green_incr = (new_green - green) / steps_before_change
            blue_incr = (new_blue - blue) / steps_before_change

        if bob_the_turtle.wants_to_change_direction():
            # Find new random increments for change of every coordinate
            x1_incr = random_increment()
            y1_incr = random_increment()
            x2_incr = random_increment()
            y2_incr = random_increment()

        # Increment all coordinates
        x1 += x1_incr
        y1 += y1_incr
        x2 += x2_incr
        y2 += y2_incr

        # If any of the coordinates is off-screen, revert increment
        if abs(x1) > MAX_WIDTH:
            x1_incr *= -1

        if abs(y1) > MAX_HEIGHT:
            y1_incr *= -1

        if abs(x2) > MAX_WIDTH:
            x2_incr *= -1

        if abs(y2) > MAX_HEIGHT:
            y2_incr *= -1

        # Draw the new line, in the current color
        draw_turtle(bob_the_turtle, x1, y1, x2, y2, red, green, blue)


def main():
    draw_turtle_screensaver()


if __name__ == '__main__':
    main()
