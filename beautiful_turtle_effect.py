import turtle
import colorsys


# Window settings
window = turtle.Screen()
window.bgcolor('black')
window.title('Beautiful Turtle Effect')

# Creating a turtle
t = turtle.Turtle()
t.speed(0)
t.width(2)

# Loop for drawing the spiral
for i in range(500):
    hue = i / 360.0
    color = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
    t.color(color)
    t.forward(i)
    t.left(59)

# Exiting the program on click
window.exitonclick()
