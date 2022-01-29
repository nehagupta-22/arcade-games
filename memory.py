# Memory

import simplegui
import random

exposed = [False] * 16
card1 = None
card2 = None
turn = 0

# helper function to initialize globals
def new_game():
    global cards, state, exposed, turn
    cards = range(8) * 2
    random.shuffle(cards)
    state = 0
    turn = 0
    exposed = [False] * 16
    label.set_text("Turns = " + str(turn))

     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global cards, exposed, state, card1, card2, turn
    
    if pos[0] >= 30 and pos[0] <= 16 * 50 + 25 and pos[1] >= 10 and pos[1] <= 110:    
        index = (pos[0] - 30) // 50
        if exposed[index] == False:
            exposed[index] = True
            if state == 0:
                card1 = index
                state = 1
            elif state == 1:
                state = 2
                card2 = index
                turn += 1    
                label.set_text("Turns = " + str(turn))
            else:
                state = 1
                if cards[card1] != cards[card2]:
                    exposed[card1] = False
                    exposed[card2] = False
                    
                card1 = index
                
   
                                            
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global cards, exposed, state, turn
    
    #draws cards and numbers in cards
    num_x = 47
    card_x = 30
    for num in cards:
        canvas.draw_text(str(num), [num_x, 70], 33, "White")
        num_x += 50
        
    for card in exposed:
        if card:
            canvas.draw_polygon([[card_x, 10], [card_x + 50,10], [card_x + 50, 110], [card_x,110]], 3, "pink") 
        elif not card:
            canvas.draw_polygon([[card_x, 10], [card_x + 50,10], [card_x + 50, 110], [card_x ,110]], 3, "pink", "Blue") 
        card_x += 50   

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 16 * 50 + 50, 120)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = " + str(turn))


# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
