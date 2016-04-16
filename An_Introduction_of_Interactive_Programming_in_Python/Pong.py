# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2

PAD_VEL = 5
ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [0, 0]

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel, vel_mul # these are vectors stored as lists
    global WIDTH, HEIGHT
    
    ball_pos[0] = WIDTH / 2
    ball_pos[1] = HEIGHT / 2
    if direction:
        ball_vel[0] = random.randrange(20,40) / 10.0
    else:
        ball_vel[0] = -random.randrange(20,40) / 10.0
    ball_vel[1] = -random.randrange(5,30) / 10.0
    vel_mul = 1.0

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    
    paddle1_pos = HEIGHT / 2
    paddle2_pos = paddle1_pos
    paddle1_vel = 0
    paddle2_vel = paddle1_vel
    score1 = 0
    score2 = score1
    spawn_ball(True)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, vel_mul
    global WIDTH, HEIGHT, PAD_WIDTH, BALL_RADIUS, HALF_PAD_HEIGHT, HALF_PAD_WIDTH
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0] * vel_mul
    ball_pos[1] += ball_vel[1] * vel_mul
    if ball_pos[0] < PAD_WIDTH + BALL_RADIUS:
        if ball_pos[1] >= paddle1_pos - HALF_PAD_HEIGHT and ball_pos[1] <= paddle1_pos + HALF_PAD_HEIGHT:
            ball_pos[0] -= ball_vel[0] * vel_mul
            ball_vel[0] = -ball_vel[0]
            ball_pos[0] += ball_vel[0] * vel_mul
            vel_mul += 0.2
        else:
            score2 += 1
            spawn_ball(True)
    elif ball_pos[0] > WIDTH - PAD_WIDTH - BALL_RADIUS:
        if ball_pos[1] >= paddle2_pos - HALF_PAD_HEIGHT and ball_pos[1] <= paddle2_pos + HALF_PAD_HEIGHT:
            ball_pos[0] -= ball_vel[0] * vel_mul
            ball_vel[0] = -ball_vel[0]
            ball_pos[0] += ball_vel[0] * vel_mul
            vel_mul += 0.2
        else:
            score1 += 1
            spawn_ball(False)
    if ball_pos[1] > HEIGHT - BALL_RADIUS or ball_pos[1] < BALL_RADIUS:
        ball_pos[1] -= ball_vel[1]
        ball_vel[1] = -ball_vel[1]
        ball_pos[1] += ball_vel[1]
    
            
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS / 2, BALL_RADIUS, "White")
    
    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos += paddle1_vel
    if paddle1_pos > HEIGHT - HALF_PAD_HEIGHT or paddle1_pos < HALF_PAD_HEIGHT:
        paddle1_pos -= paddle1_vel
    paddle2_pos += paddle2_vel
    if paddle2_pos > HEIGHT - HALF_PAD_HEIGHT or paddle2_pos < HALF_PAD_HEIGHT:
        paddle2_pos -= paddle2_vel
    
    # draw paddles
    canvas.draw_line([HALF_PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT], [HALF_PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT], PAD_WIDTH, "White")
    canvas.draw_line([WIDTH - HALF_PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT], [WIDTH- HALF_PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT], PAD_WIDTH, "White")    
    # draw scores
    canvas.draw_text(str(score1), [WIDTH / 4 + HALF_PAD_WIDTH, HEIGHT / 5], HEIGHT / 10, "White")
    canvas.draw_text(str(score2), [WIDTH / 4 * 3 - HALF_PAD_WIDTH, HEIGHT / 5], HEIGHT / 10, "White")
        
def keydown(key):
    global paddle1_vel, paddle2_vel, PAD_VEL
    
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -PAD_VEL
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = PAD_VEL
    elif key == simplegui.KEY_MAP["W"]:
        paddle1_vel = -PAD_VEL
    elif key == simplegui.KEY_MAP["S"]:
        paddle1_vel = PAD_VEL

   
def keyup(key):
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP["up"]:
        if paddle2_vel < 0:
            paddle2_vel = 0
    elif key == simplegui.KEY_MAP["down"]:
        if paddle2_vel > 0:
            paddle2_vel = 0
    elif key == simplegui.KEY_MAP["W"]:
        if paddle1_vel < 0:
            paddle1_vel = 0
    elif key == simplegui.KEY_MAP["S"]:
        if paddle1_vel > 0:
            paddle1_vel = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

frame.add_button("Restart", new_game)

# start frame
new_game()
frame.start()
