import pyglet
import random

# Create a window
window = pyglet.window.Window(width=1500, height=600, caption='Search Visualizations')
batch = pyglet.graphics.Batch()
impact_font = pyglet.font.load('Impact')

# Generate a sorted list with random numbers ensuring 37 is included
target = 37
binary_numbers = sorted(random.sample(range(1, 100), 18) + [target])
binary_numbers.insert(0, 1)
binary_numbers.insert(len(binary_numbers), 100)
binary_numbers = [1, 3, 4, 5, 6, 9, 13, 15, 17, 21, 22, 23, 30, 33, 34, 35, 37, 74, 80, 84, 100]
# Generate a list for Linear Search
linear_numbers = binary_numbers

# Variables to control the animation and search for Binary Search
binary_left, binary_right = 0, len(binary_numbers) - 1
binary_mid = (binary_left + binary_right) // 2
binary_found = False
binary_search_complete = False

# Variables to control the animation and search for Linear Search
linear_current_index = 0
linear_found_index = -1
linear_search_complete = False

# Function to toggle the visibility of succeed label for Binary Search
def toggle_succeed_label(dt):
    global succeed_visible
    succeed_visible = not succeed_visible

def binary_search(dt):
    global binary_left, binary_right, binary_mid, binary_found, binary_search_complete
    if binary_left <= binary_right and not binary_found:
        binary_mid = (binary_left + binary_right) // 2
        if binary_numbers[binary_mid] == target:
            binary_found = True
        elif binary_numbers[binary_mid] < target:
            binary_left = binary_mid + 1
        else:
            binary_right = binary_mid - 1
    else:
        binary_search_complete = True

def linear_search(dt):
    global linear_current_index, linear_found_index, linear_search_complete
    if linear_current_index < len(linear_numbers):
        if linear_numbers[linear_current_index] == target:
            linear_found_index = linear_current_index
            linear_search_complete = True
        linear_current_index += 1
    else:
        linear_search_complete = True

@window.event
def on_draw():
    window.clear()

    # Draw Linear Search on the top of the window
    for i, number in enumerate(linear_numbers):
        x = i * 60 + 50
        y = window.height * 0.65
        width = 50
        height = 50

        if i == linear_current_index and not linear_search_complete:
            color = (255, 0, 0)  # Red for the current box being checked
            label = pyglet.text.Label(".",
                           x=x+width//2,
                           y=y+height//2-50,
                           anchor_x='center',
                           anchor_y='center',
                           batch=batch,
                           font_name='Impact',font_size=30,
                           color=(255,255, 255, 255))
            label.draw()
        elif i == linear_found_index:
            color = (0, 255, 0)  # Green if 37 is found
            if succeed_visible:
                label77 = pyglet.text.Label("Succeed!",
                                x=x+30,
                                y=y-25,
                                anchor_x='center',
                                anchor_y='center',
                                batch=batch,
                                font_name='Impact',font_size=25,
                                color=(255,255, 255, 255))
                label77.draw()
        else:
            color = (0 , 0 , 0 , 255)  # White for unchecked or passed boxes
        
        pyglet.shapes.Rectangle(x, y, width, height, color=(255, 255, 255), batch=batch).draw()
        pyglet.shapes.Rectangle(x+3, y+3, width-6, height-6, color=color , batch=batch).draw()
        label = pyglet.text.Label(str(number), x=x+width//2, y=y+height//2, anchor_x='center', anchor_y='center',font_name='Impact', batch=batch,color=(255,255,255,255),font_size=15)
        label.draw()

    # Draw Binary Search on the bottom of the window
    for i, number in enumerate(binary_numbers):
        x = i * 60 + 50
        y = window.height * 0.25
        width = 50
        height = 50

        if binary_left <= i <= binary_right and not binary_search_complete:
            color = (0, 0, 0, 255)  # white for the current search interval
        elif i == binary_mid and not binary_search_complete:
            if number >= target and not binary_search_complete:
                label = pyglet.text.Label("more than", x=x+width//2, y=(y+height//2)-50,anchor_x='center', anchor_y='center',batch=batch,color=(255,255,255,255),font_name='Impact',font_size=25)
                label.draw()
            else:
                label = pyglet.text.Label("less than", x=x+width//2, y=(y+height//2)-50,anchor_x='center', anchor_y='center',batch=batch,color=(255,255,255,255),font_name='Impact',font_size=25)
                label.draw()
            color = (255, 0, 0)  # Red for the middle element
        elif binary_found and i == binary_mid:
            color = (0, 255, 0)  # Green if 37 is found
            if succeed_visible:
                label = pyglet.text.Label("Succeed!", x=x+width//2, y=(y+height//2)-50,anchor_x='center', anchor_y='center',batch=batch,color=(255,255,255,255),font_name='Impact',font_size=25)
                label.draw()
        else:
            color = (200, 200, 200)  # Grey for eliminated elements

        pyglet.shapes.Rectangle(x, y, width, height, color=(255, 255, 255), batch=batch).draw()
        pyglet.shapes.Rectangle(x+3, y+3, width-6, height-6, color=color , batch=batch).draw()
        # Draw the number inside the box
        label = pyglet.text.Label(str(number), x=x+width//2, y=y+height//2, anchor_x='center', anchor_y='center',font_name='Impact', batch=batch,color=(255,255,255,255),font_size=15)
        label.draw()

@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.R:
        reset_search()


def reset_search():
    global binary_left, binary_right, binary_mid, binary_found, binary_search_complete
    binary_left, binary_right = 0, len(binary_numbers) - 1
    binary_mid = (binary_left + binary_right) // 2
    binary_found = False
    binary_search_complete = False

    global linear_current_index, linear_found_index, linear_search_complete
    linear_current_index = 0
    linear_found_index = -1
    linear_search_complete = False

    # Reset blinking of "Succeed!" text
    global succeed_blinking
    succeed_blinking = True

# Variable to control the visibility of succeed label for Binary Search
succeed_visible = True
# Schedule the text to toggle every 0.5 seconds
pyglet.clock.schedule_interval(toggle_succeed_label, 1)
# Schedule the binary search to run every 2 seconds
pyglet.clock.schedule_interval(binary_search, 0.5)
# Schedule the linear search to run every 1 second
pyglet.clock.schedule_interval(linear_search, 0.3)

pyglet.app.run()
