import pyglet
import random

# Create a window
window = pyglet.window.Window(width=1200, height=600, caption='Linear Search Visualization')
batch = pyglet.graphics.Batch()

#โหลดฟอนต์ ตัวหนา
impact_font = pyglet.font.load('Impact')

# Generate a list with random numbers ensuring 99 is included
# n = 6
# numbers = random.sample(range(1, 100), n)
# numbers.insert(random.sample(range(n//2, n), 1)[0],99) #ให้มันrandom 99 กว่ากว่า index ครึ่งหนึ่ง
# print(numbers)
target = 37
numbers = [81, 38, 23, 70, 92, 37, 22]
# Variables to control the animation and search
current_index = 0
found_index = -1
search_complete = False

def linear_search(dt):
    global current_index, found_index, search_complete
    if current_index < len(numbers):
        if numbers[current_index] == target:
            found_index = current_index
            search_complete = True
        current_index += 1
    else:
        search_complete = True


# Variable to control the blinking of "Succeed!" text
succeed_blinking = True

@window.event
def on_draw():
    window.clear()
    for i, number in enumerate(numbers):
        # Define the position and size of each 'box'
        x = i * 120 + 200
        y = window.height // 2
        width = 100
        height = 100

        # Draw the box
        if i == current_index and not search_complete:
            color = (255, 0, 0)  # Red for the current box being checked
            label = pyglet.text.Label(".",
                           x=x+50,
                           y=y-20,
                           anchor_x='center',
                           anchor_y='center',
                           batch=batch,
                           font_name='Impact',font_size=30,
                           color=(255,255, 255, 255))
            label.draw()
        elif i == found_index:
            color = (0, 255, 0)  # Green if 99 is found
            if succeed_blinking:
                label = pyglet.text.Label("Succeed!",
                               x=x+50,
                               y=y-30,
                               anchor_x='center',
                               anchor_y='center',
                               batch=batch,
                               font_name='Impact',font_size=35,
                               color=(255,255, 255, 255))
                label.draw()
        else:
            color = (0 , 0 , 0 , 255)  # White for unchecked or passed boxes
        
        pyglet.shapes.Rectangle(x, y, width, height, color=(255, 255, 255), batch=batch).draw()
        pyglet.shapes.Rectangle(x+3, y+3, width-6, height-6, color=color , batch=batch).draw()
        # Draw the number inside the box
        label = pyglet.text.Label(str(number),
                           x=x+width//2,
                           y=y+height//2,
                           anchor_x='center',
                           anchor_y='center',
                           batch=batch,
                           font_name='Impact',font_size=30,
                           color=(255,255, 255, 255))

        label.draw()

@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.R:
        reset_search()

def reset_search():
    global current_index, found_index, search_complete
    current_index = 0
    found_index = -1
    search_complete = False

    # Reset blinking of "Succeed!" text
    global succeed_blinking
    succeed_blinking = True

# Function to toggle blinking of "Succeed!" text
def toggle_blink(dt):
    global succeed_blinking
    succeed_blinking = not succeed_blinking

# Schedule the blinking of "Succeed!" text every 0.5 seconds
pyglet.clock.schedule_interval(toggle_blink, 1)
# Schedule the linear search to run every 0.2 seconds
pyglet.clock.schedule_interval(linear_search, 1)

pyglet.app.run()
