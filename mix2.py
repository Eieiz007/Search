import pyglet
import random

# Create a window
window = pyglet.window.Window(width=1500, height=600, caption='Search Visualizations')
batch = pyglet.graphics.Batch()
impact_font = pyglet.font.load('Impact')

# Load sound effects
found_sound = pyglet.media.load('found.mp3', streaming=False)
search_complete_sound = pyglet.media.load('complete.mp3', streaming=False)

# Generate a sorted list with random numbers ensuring 37 is included
target = 99
binary_numbers = sorted(random.sample(range(1, 500), 200) + [target])

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
            found_sound.play()  # Play sound when target is found
        elif binary_numbers[binary_mid] < target:
            binary_left = binary_mid + 1
        else:
            binary_right = binary_mid - 1
    else:
        binary_search_complete = True
        search_complete_sound.play()  # Play sound when search is complete

def linear_search(dt):
    global linear_current_index, linear_found_index, linear_search_complete
    if linear_current_index < len(linear_numbers):
        if linear_numbers[linear_current_index] == target:
            linear_found_index = linear_current_index
            linear_search_complete = True
            found_sound.play()  # Play sound when target is found
        linear_current_index += 1
    else:
        linear_search_complete = True
        search_complete_sound.play()  # Play sound when search is complete

@window.event
def on_draw():
    window.clear()

    # Draw Linear Search on the top of the window
    bar_width = 7
    bar_spacing = 2
    bar_height_factor = window.height * 0.35 / max(linear_numbers)  # Adjusted to fit the window
    for i, number in enumerate(linear_numbers):
        x = i * (bar_width + bar_spacing) + 50
        y = window.height * 0.65
        width = bar_width
        height = number * bar_height_factor

        if i == linear_current_index and not linear_search_complete:
            color = (255, 0, 0)  # Red for the current bar being checked
        elif i == linear_found_index:
            color = (0, 255, 0)  # Green if 37 is found
        else:
            color = (255,255,255,255)  # Black for other bars
        
        pyglet.shapes.Rectangle(x, y, width, height, color=color, batch=batch).draw()

    # Draw Binary Search on the bottom of the window
    for i, number in enumerate(binary_numbers):
        x = i * (bar_width + bar_spacing) + 50
        y = window.height * 0.25
        width = bar_width
        height = number * bar_height_factor

        if binary_left <= i <= binary_right and not binary_search_complete:
            color = (255,255,255,255)  # Black for the current search interval
        elif i == binary_mid and not binary_search_complete:
            color = (255, 0, 0)  # Red for the middle bar
            
        elif binary_found and i == binary_mid:
            color = (0, 255, 0)  # Green if 37 is found
        else:
            color = (200, 200, 200)  # Grey for other bars

        pyglet.shapes.Rectangle(x, y, width, height, color=color, batch=batch).draw()

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

# Variable to control the visibility of succeed label for Binary Search
succeed_visible = True
# Schedule the text to toggle every 0.5 seconds
pyglet.clock.schedule_interval(toggle_succeed_label, 1)
# Schedule the binary search to run every 2 seconds
pyglet.clock.schedule_interval(binary_search, 0.5)
# Schedule the linear search to run every 1 second
pyglet.clock.schedule_interval(linear_search, 0.2)

pyglet.app.run()
