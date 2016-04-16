# implementation of card game - Memory

import simplegui
import random

state = 0
numbers = []
states = []
tries = []
count = 0

# helper function to initialize globals
def new_game():
    global state, numbers, tries, states, count
    state = 0
    numbers = range(8) + range(8)
    random.shuffle(numbers)
    states = []
    for i in range(16):
        states.append(False)
    tries = []
    label.set_text("Turns = 0")
    count = 0
     
# define event handlers
def mouseclick(pos):
    global state, tries, count
    idx = pos[0] / 50
    if not states[idx]:
        if not idx in tries:
            if state < 2:
                if state ==0:
                    count += 1
                    label.set_text("Turns = " + str(count))
                state += 1
                tries.append(idx)
            elif state == 2:
                state = 1
                if numbers[tries[0]] == numbers[tries[1]]:
                    states[tries[0]], states[tries[1]] = True, True
                tries = [idx]
                count += 1
                label.set_text("Turns = " + str(count))

# cards are logically 50x100 pixels in size    
def draw(canvas):
    global tries, numbers
    for i in range(16):
        if i in tries or states[i]:
            canvas.draw_polygon([[i * 50, 0], [(i + 1) * 50, 0], [(i + 1) * 50, 100], [i * 50, 100]], 5, "White", "Black")
            canvas.draw_text(str(numbers[i]), [i * 50 + 7, 75], 75, "White")
        else:
            canvas.draw_polygon([[i * 50, 0], [(i + 1) * 50, 0], [(i + 1) * 50, 100], [i * 50, 100]], 5, "White", "Green")

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
