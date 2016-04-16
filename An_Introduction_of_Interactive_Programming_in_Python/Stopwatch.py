# "Stopwatch: The Game"
import simplegui

# define global variables
current_time = 0
time_display = "0:00.0"
attempts = 0
succeeds = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def time_format(t):
    D = t % 10
    t /= 10
    BC = t % 60
    A = t / 60
    if BC < 10:
        return str(A) + ":0" + str(BC) + "." + str(D)
    else:
        return str(A) + ":" + str(BC) + "." + str(D)

def result_format(x, y):
    return str(x) + "/" + str(y)
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start_click():
    if not timer.is_running():
        timer.start()

def stop_click():
    global attempts, succeeds
    if timer.is_running():
        timer.stop()
        attempts += 1
        if current_time % 10 ==0:
            succeeds += 1

def reset_click():
    global current_time, time_display, attempts, succeeds
    if timer.is_running():
        timer.stop()
    current_time = 0
    time_display = "0:00.0"
    succeeds = 0
    attempts = 0

# define event handler for timer with 0.1 sec interval
def timer_tick():
    global current_time, time_display
    current_time += 1
    time_display = time_format(current_time)

# define draw handler
def draw_handler(canvas):
    global time_display, attempts, succeeds
    if time_display[-1] == '0' and not timer.is_running():
        canvas.draw_text(time_display, [50,110], 50, "Green")
        canvas.draw_text("Nice!", [70,175], 50, "White")
    elif time_display[-1] != '0' and not timer.is_running():
        canvas.draw_text(time_display, [50,110], 50, "Red")
        canvas.draw_text("Oops!", [70,175], 50, "White")
    else:
        canvas.draw_text(time_display, [50,110], 50, "Blue")
    canvas.draw_text(result_format(succeeds, attempts), [200,45], 40, "White")
    
# create frame
frame = simplegui.create_frame("Stopwatch", 300, 200)

# register event handlers
btn_start = frame.add_button("Start", start_click)
btn_stop = frame.add_button("Stop", stop_click)
btn_reset = frame.add_button("Reset", reset_click)
timer = simplegui.create_timer(100, timer_tick)
frame.set_draw_handler(draw_handler)

# start frame
frame.start()
