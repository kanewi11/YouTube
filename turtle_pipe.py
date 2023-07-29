import turtle
import colorsys


# Create a screen for drawing
screen = turtle.Screen()
screen.bgcolor('black')

# Create a turtle
circle_turtle = turtle.Turtle()
circle_turtle.speed(0)

hue = 0  # Set the initial color (hue) value
width = 1  # Set the initial color (hue) value

# Draw circles with changing radius, colors, and line width
for i in range(144):
    hue += 0.02  # Change the hue for the next circle
    width += 0.2  # Change the line width for the next circle
    circle_turtle.right(10)
    circle_turtle.pensize(width)
    circle_turtle.pencolor(colorsys.hsv_to_rgb(hue, 1.0, 1.0))
    circle_turtle.circle(100)

# Exit the program on click
screen.exitonclick()
