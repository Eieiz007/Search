import pyglet
import random

# Create a window
window = pyglet.window.Window(width=1200, height=600, caption='Binary Search Visualization')
batch = pyglet.graphics.Batch()
impact_font = pyglet.font.load('Impact')

# Generate a sorted list with random numbers ensuring 37 is included
target = 37
numbers = sorted(random.sample(range(1, 100), 6) + [target])
numbers.insert(0, 1)
numbers.insert(len(numbers), 100)

# Variables to control the animation and search
left, right = 0, len(numbers) - 1
mid = (left + right) // 2
found = False
search_complete = False

# Function to toggle the visibility of succeed label
def toggle_succeed_label(dt):
    global succeed_visible
    succeed_visible = not succeed_visible


def binary_search(dt):
    global left, right, mid, found, search_complete
    if left <= right and not found:
        mid = (left + right) // 2
        if numbers[mid] == target:
            found = True
        elif numbers[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    else:
        search_complete = True


@window.event
def on_draw():
    window.clear()
    for i, number in enumerate(numbers):
        # Define the position and size of each 'box'
        x = i * 120 + 80
        y = window.height // 2
        width = 100
        height = 100
        
        # Draw the box
        if left <= i <= right and not search_complete:
            color = (0, 0, 0, 255)  # white for the current search interval
        elif i == mid and not search_complete:
            color = (255, 0, 0)  # Red for the middle element
            if number >= target and not search_complete:
                label = pyglet.text.Label("more than", x=x+width//2, y=(y+height//2)-75,anchor_x='center', anchor_y='center',batch=batch,color=(255,255,255,255),font_name='Impact',font_size=35)
                label.draw()
            else:
                label = pyglet.text.Label("less than", x=x+width//2, y=(y+height//2)-75,anchor_x='center', anchor_y='center',batch=batch,color=(255,255,255,255),font_name='Impact',font_size=35)
                label.draw()
        elif found and i == mid:
            color = (0, 255, 0)  # Green if 37 is found
            if succeed_visible:
                labelsucceedd = pyglet.text.Label("Succeed!", x=x+width//2, y=(y+height//2)-75,anchor_x='center', anchor_y='center',batch=batch,color=(255,255,255,255),font_name='Impact',font_size=35)
                labelsucceedd.draw()
        else:
            color = (200, 200, 200)  # Grey for eliminated elements

        
        pyglet.shapes.Rectangle(x, y, width, height, color=(255, 255, 255), batch=batch).draw()
        pyglet.shapes.Rectangle(x+3, y+3, width-6, height-6, color=color , batch=batch).draw()
        # Draw the number inside the box
        label = pyglet.text.Label(str(number), x=x+width//2, y=y+height//2, anchor_x='center', anchor_y='center',font_name='Impact', batch=batch,color=(255,255,255,255),font_size=25)
        label.draw()

@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.R:
        reset_search()

def reset_search():
    global left, right, mid, found, search_complete
    left, right = 0, len(numbers) - 1
    mid = (left + right) // 2
    found = False
    search_complete = False

# Variable to control the visibility of succeed label
succeed_visible = True
# Schedule the text to toggle every 0.5 seconds
pyglet.clock.schedule_interval(toggle_succeed_label, 1)
# Schedule the binary search to run every 1 second
pyglet.clock.schedule_interval(binary_search, 2)

pyglet.app.run()
