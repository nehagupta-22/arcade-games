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
LEFT = False
RIGHT = True
ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [0, 0]
paddle1_pos = [HALF_PAD_WIDTH, 30]
paddle2_pos = [WIDTH - HALF_PAD_WIDTH, 30]
paddle1_vel = 0
paddle2_vel = 0
PADDLE_VEL = 4.5

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    global score_1, score_2
    ball_pos = [WIDTH / 2, HEIGHT / 2]    
    ball_vel[1] = random.randrange(-3, 0)
    if direction == RIGHT:
        ball_vel[0] = random.randrange(2, 5)
        
    else:
        ball_vel[0] = random.randrange(-4, -1)
        
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score_1, score_2  # these are ints
    spawn_ball(RIGHT)
    score_1 = 0
    score_2 = 0

def draw(canvas):
    global score_1, score_2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, paddle1_vel, paddle2_vel
            
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # bouncing off of walls
    
    if 0 >= ball_pos[1] - BALL_RADIUS or ball_pos[1] + BALL_RADIUS > HEIGHT:
        ball_vel[1] = -ball_vel[1]
    
    # gutters
    
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        if ball_pos[1] >= paddle1_pos[1] and ball_pos[1] <= paddle1_pos[1] + PAD_HEIGHT:
            ball_vel[0] = -ball_vel[0] * 1.1
            ball_vel[1] *= 1.1
        else:
            spawn_ball(RIGHT)
            score_2 += 1
                        
    elif ball_pos[0] >= WIDTH - BALL_RADIUS - PAD_WIDTH:
        if ball_pos[1] >= paddle2_pos[1] and ball_pos[1] <= paddle2_pos[1] + PAD_HEIGHT:
            ball_vel[0] = -ball_vel[0] * 1.1
            ball_vel[1] *= 1.1
        else:
            spawn_ball(LEFT)
            score_1 += 1
            
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, "White", "White")
    
    # update paddle's vertical position, keep paddle on the screen
        
    if paddle1_pos[1] + paddle1_vel > 0 and paddle1_pos[1] + paddle1_vel + PAD_HEIGHT < HEIGHT:
        paddle1_pos[1] += paddle1_vel  
        
    if paddle2_pos[1] + paddle2_vel > 0 and paddle2_pos[1] + paddle2_vel + PAD_HEIGHT < HEIGHT:
        paddle2_pos[1] += paddle2_vel  
                
    # draw paddles
    canvas.draw_line(paddle1_pos, [HALF_PAD_WIDTH, paddle1_pos[1] + PAD_HEIGHT], 8 , "White")
    canvas.draw_line(paddle2_pos, [WIDTH - HALF_PAD_WIDTH, paddle2_pos[1] + PAD_HEIGHT], 8 ,"White") 
   
    # determine whether paddle and ball collide    
    
    # draw scores
    canvas.draw_text(str(score_1), [30, 50], 40, "White")
    canvas.draw_text(str(score_2), [550, 50], 40, "White")
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel -= PADDLE_VEL
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel += PADDLE_VEL
    elif key == simplegui.KEY_MAP["w"]:
        paddle1_vel -= PADDLE_VEL
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel += PADDLE_VEL
        

def keyup(key):
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
        


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("New Game", new_game)


# start frame
new_game()
frame.start()
