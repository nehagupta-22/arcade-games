# Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
prompt = "Hit or Stand?"


# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []
        
    def __str__(self):
        str_repr = "Hand contains "
        for card in self.cards:
            str_repr += str(card) + " "                   
        return str_repr	# return a string representation of a hand

    def add_card(self, card):
        self.cards.append(card) # add a card object to a hand
    
    def get_value(self):
        global value
        value = 0
        ace = False
        for card in self.cards:
            value += VALUES[str(card.rank)]
            if "A" == card.rank:
                ace = True
        if ace == True and value + 10 <= 21:
            value += 10
            ace = False              
        return value
    
    def draw(self, canvas, pos):
        for card in self.cards:
            card.draw(canvas, pos)
            pos[0] += 100
            
        
# define deck class 
class Deck:
    def __init__(self):
        self.cards = []	# create a Deck object
        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(suit,rank))        

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.cards)   # use random.shuffle()

    def deal_card(self):
        return self.cards.pop(random.randrange(0, len(self.cards)))	# deal a card object from the deck
    
    def __str__(self):
        str_repr = "Deck contains "
        for card in self.cards:
            str_repr += str(card) + " " 
        return str_repr # return a string representing the deck
        

#define event handlers for buttons
def deal():
    global outcome, in_play, deck, player_hand, dealer_hand, prompt, score
    
    deck = Deck()
    deck.shuffle()
    
    player_hand = Hand()
    dealer_hand = Hand()
    
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    
    if in_play:
        outcome = "You Quit!"
        score -= 1 
    else:
        outcome = " "
    prompt = "Hit or Stand?"
                              
    
    
    in_play = True

def hit():
    global player_hand, deck, outcome, prompt, in_play, score
    if player_hand.get_value() <= 21:
        player_hand.add_card(deck.deal_card())
        if player_hand.get_value() > 21:
            outcome = "You have busted!"
            prompt = "New Deal?"
            in_play = False
            score -= 1
            
 
    # if the hand is in play, hit the player
   
    # if busted, assign a message to outcome, update in_play and score
       
def stand():
    global player_hand, dealer_hand, busted, deck, outcome, prompt, in_play, score
    if player_hand.get_value() > 21:
        outcome = "You were busted. You cannot continue this game anymore"
        prompt = "New Deal?"
    else:
        prompt = " "
        in_play = False
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
            
        if dealer_hand.get_value() > 21:
            outcome = "Dealer busted. You win!"
            prompt = "New Deal?"
            score += 1
        else:
            if player_hand.get_value() > dealer_hand.get_value():
                outcome = "You win!"
                prompt = "New Deal?"
                score += 1
            else:
                outcome = "Dealer wins!"
                prompt = "New Deal?"
                score -= 1
        
    
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more

    # assign a message to outcome, update in_play and score

# draw handler
def draw(canvas):
    player_hand.draw(canvas, [50, 430])
    canvas.draw_text("Blackjack", [260, 60], 30, "Black")
    canvas.draw_text(outcome, [220, 350], 27, "Black")
    canvas.draw_text(prompt, [420, 140], 26, "Black")
    canvas.draw_text("Player", [60,400], 26, "Black")
    dealer_hand.draw(canvas, [50,200])
    canvas.draw_text("Dealer", [60,170], 26, "Black")
    canvas.draw_text("Score: " + str(score), [420, 110], 26, "Black")
    if in_play:
        canvas.draw_image(card_back, [36,48], [72, 96], [86,248], [72, 96])

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
