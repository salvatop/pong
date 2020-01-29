# Implementation of classic arcade game Pong
import simplegui
import random
import math

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 40
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [0, 0]
paddle1_pos = HEIGHT / 2
paddle2_pos = HEIGHT / 2
paddle1_vel = 0
paddle2_vel = 0
score1 = 0
score2 = 0
speed = 5

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel 
    ball_pos = [WIDTH / 2, HEIGHT / 2]   
    if direction == RIGHT:
        r = random.randrange(3, 5)
        r1 = random.randrange(1, 3)
        ball_vel = [r, -r1]
    if direction == LEFT:
        l = random.randrange(3, 5)
        l1 = random.randrange(1, 3)
        ball_vel = [-l, -l1]

def distance(p,q):
    return math.sqrt((p[0] - q[0])**2 + (p[1] - q[1])**2)
                    
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    paddle1_pos = HEIGHT/2 
    paddle2_pos = HEIGHT/2
    paddle1_vel = 0
    paddle2_vel = 0
    score1 = 0
    score2 = 0
    d = random.randint(0,1)
    if d == 0:
        spawn_ball(LEFT)
    else:
        spawn_ball(RIGHT)
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, paddle1_vel, paddle2_vel 
    global HALF_PAD_WIDTH, HALF_PAD_HEIGHT
    # draw mid line and gutters
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH / 2, (HEIGHT/2) - 15],[WIDTH / 2, (HEIGHT / 2) +15], 2, "White")
    canvas.draw_line([WIDTH / 2, 150],[WIDTH / 2, 180], 2, "White")
    canvas.draw_line([WIDTH / 2, 110],[WIDTH / 2, 145], 2, "White")
    canvas.draw_line([WIDTH / 2, 70],[WIDTH / 2, 105], 2, "White")
    canvas.draw_line([WIDTH / 2, 30],[WIDTH / 2, 65], 2, "White")
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, 25], 2, "White")
    canvas.draw_line([WIDTH / 2, 190],[WIDTH / 2, 220], 2, "White")
    canvas.draw_line([WIDTH / 2, 225],[WIDTH / 2, 260], 2, "White")
    canvas.draw_line([WIDTH / 2, 265],[WIDTH / 2, 300], 2, "White")
    canvas.draw_line([WIDTH / 2, 305],[WIDTH / 2, 340], 2, "White")
    canvas.draw_line([WIDTH / 2, 345],[WIDTH / 2, 380], 2, "White")
    canvas.draw_line([WIDTH / 2, 385],[WIDTH / 2, 420], 2, "White")
    
    # update ball, next position = current position + current velocity
    ball_pos[0] += ball_vel[0] #X
    ball_pos[1] += ball_vel[1] #Y    
    
    # draw ball
    canvas.draw_circle(ball_pos, 4, 8, 'White')
    
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos + paddle1_vel < (HEIGHT - PAD_HEIGHT) and paddle1_pos + paddle1_vel > PAD_HEIGHT:
        paddle1_pos += paddle1_vel
    if paddle2_pos + paddle2_vel < (HEIGHT - PAD_HEIGHT) and paddle2_pos + paddle2_vel > PAD_HEIGHT:
        paddle2_pos += paddle2_vel
     
    # draw paddles
    canvas.draw_polyline([[(PAD_WIDTH + HALF_PAD_WIDTH), paddle1_pos + PAD_HEIGHT ],[(PAD_WIDTH + HALF_PAD_WIDTH), paddle1_pos - PAD_HEIGHT]], PAD_WIDTH, 'White')	
    canvas.draw_polyline([[(WIDTH - (PAD_WIDTH + HALF_PAD_WIDTH)), paddle2_pos + PAD_HEIGHT],[(WIDTH - (PAD_WIDTH + HALF_PAD_WIDTH)), paddle2_pos - PAD_HEIGHT]], PAD_WIDTH, 'White')
    
    # determine whether walls/paddles and ball collide    
    if ball_pos[1] > HEIGHT - BALL_RADIUS: #bottom
        ball_vel[1] = -ball_vel[1]
    if ball_pos[1] < 0 + BALL_RADIUS: #top
        ball_vel[1] = -ball_vel[1]
    if ball_pos[0] >= WIDTH - BALL_RADIUS: #right
        score1 = score1 + 1
        spawn_ball(LEFT)
    if ball_pos[0] <= 0 - BALL_RADIUS: #left
        score2 = score2 + 1
        spawn_ball(RIGHT)
    
    paddle1_pos_x = (PAD_WIDTH + HALF_PAD_WIDTH)
    paddle1_pos_y = (paddle1_pos + paddle1_vel)
    d1 = distance([paddle1_pos_x,paddle1_pos_y],ball_pos)
    top1 = distance([(PAD_WIDTH + HALF_PAD_WIDTH), paddle1_pos - PAD_HEIGHT], ball_pos)    
    if top1 < (PAD_WIDTH + BALL_RADIUS):
        ball_vel[0] = -ball_vel[0]            
        ball_vel[0] += speed / 5 
    if d1 < (PAD_WIDTH + BALL_RADIUS):
        ball_vel[0] = -ball_vel[0]            
        ball_vel[0] += speed / 5 
        
    paddle2_pos_x = WIDTH - (PAD_WIDTH + HALF_PAD_WIDTH)
    paddle2_pos_y = (paddle2_pos + paddle2_vel)
    d2 = distance([paddle2_pos_x,paddle2_pos_y],ball_pos)
    bottom2 = distance([WIDTH - (PAD_WIDTH + HALF_PAD_WIDTH), paddle2_pos + PAD_HEIGHT], ball_pos)
    if bottom2 < (PAD_WIDTH + BALL_RADIUS):
        ball_vel[0] = -ball_vel[0]            
        ball_vel[0] -= speed / 5
    if d2 < (PAD_WIDTH + BALL_RADIUS):
        ball_vel[0] = -ball_vel[0]            
        ball_vel[0] -= speed / 5
    
    # draw scores       
    sc1 = str(score1)
    sc2 = str(score2)
    canvas.draw_text(sc1,(136, 60), 62, "White")
    canvas.draw_text(sc2,(436, 60), 62, "White")
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel -= speed
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel += speed
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel -= speed
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel += speed 

def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0    
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0      
            
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.add_button("Restart", new_game, 100)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

# start frame
new_game()
frame.start()
