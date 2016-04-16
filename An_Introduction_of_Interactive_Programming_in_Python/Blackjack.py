# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

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

    def draw(self, canvas, pos, invisible):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        if invisible:
            canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        else:
            canvas.draw_image(card_back, [CARD_BACK_CENTER[0], CARD_BACK_CENTER[1]], CARD_BACK_SIZE, [pos[0] + CARD_BACK_CENTER[0], pos[1] + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.cards = []

    def __str__(self):
            # return a string representation of a hand
        return ""

    def add_card(self, card):
            # add a card object to a hand
        self.cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
            # compute the value of the hand, see Blackjack video
        r = 0
        a = 0
        for i in self.cards:
            if i[0].get_rank() == 'A':
                a += 1
                r += 1
            else:
                r += VALUES[i[0].get_rank()]
        while (r + 10 < 21) and (a > 0):
            r += 10
            a -= 1
        return r
    
    def visible(self):
        for i in self.cards:
            i[1] = True
   
    def draw(self, canvas, pos):
            # draw a hand on the canvas, use the draw method for cards
        for i in self.cards:
            i[0].draw(canvas, [pos[0] + self.cards.index(i) * CARD_SIZE[0], pos[1] + CARD_SIZE[1]], i[1])
                
 
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.deck = []
        for i in SUITS:
            for j in RANKS:
                self.deck.append(Card(i, j))

    def shuffle(self):
        # shuffle the deck 
            # use random.shuffle()
        random.shuffle(self.deck)

    def deal_card(self):
            # deal a card object from the deck
        return self.deck.pop(0)
    
    def __str__(self):
            # return a string representing the deck
        return ""



#define event handlers for buttons
def deal():
    global outcome, in_play, score
    global deck, myhand, dealhand
    if in_play:
        score -= 1
    deck = Deck()
    deck.shuffle()
    myhand = Hand()
    dealhand = Hand()
    myhand.add_card([deck.deal_card(), True])
    dealhand.add_card([deck.deal_card(), True])
    myhand.add_card([deck.deal_card(), True])
    dealhand.add_card([deck.deal_card(), False])
    in_play = True
    outcome = "Hit or Stand?"

def hit():
        # replace with your code below
    global in_play, myhand, deck, score, outcome
    if in_play:
        myhand.add_card([deck.deal_card(), True])
        if myhand.get_value() > 21:
            in_play = False
            score -= 1
            outcome = "You lose! New deal?"
    # if the hand is in play, hit the player
   
    # if busted, assign a message to outcome, update in_play and score
       
def stand():
        # replace with your code below
    global in_play, dealhand, deck, myhand, score, outcome
    if in_play:
        dealhand.visible()
        while dealhand.get_value() < 17:
            dealhand.add_card([deck.deal_card(), True])
        in_play = False
        if dealhand.get_value() > 21:
            score += 1
            outcome = "You win! New deal?"
        elif myhand.get_value() > dealhand.get_value():
            score += 1
            outcome = "You win! New deal?"
        else:
            score -= 1
            outcome = "You lose! New deal?"
    
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more

    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    global myhand, dealhand, score, outcome
    canvas.draw_text("Blackjack", [240, 55], 40, "White")
    canvas.draw_text(outcome, [135, 550], 40, "White")
    canvas.draw_text("Score:" + str(score), [480, 40], 25, "White")
    canvas.draw_text("You", [100, 120], 30, "White")
    canvas.draw_text("Dealer", [80, 320], 30, "White")
    # test to make sure that card.draw works, replace with your code below
    myhand.draw(canvas, [50, 50])
    dealhand.draw(canvas, [50, 250])

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