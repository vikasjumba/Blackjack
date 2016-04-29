#http://www.codeskulptor.org/#user40_zO94H34dxiol3dH.py
# Mini-project #6 - Blackjack
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
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
action = ""
score = 0
# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

player = None
dealer = None
deck = None
# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
            self.hidden = False
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + '.' + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank
    
    def hideCard(self, _hidden):
        self.hidden = _hidden
    def isHidden(self):
        return self.hidden
    
    def draw(self, canvas, pos):
        if self.hidden:
            card_loc = (CARD_BACK_CENTER[0] + CARD_BACK_SIZE[0], CARD_BACK_CENTER[1])
            canvas.draw_image(card_back, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        else:
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
            canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

# define hand class
class Hand:
    def __init__(self,id):
        self.cards = list()	# create Hand object
        self.id = id
    def __str__(self):
        disp = self.id + ' hand contains '       
        for card in self.cards:
            if card.isHidden():
                disp += "(hidden card) "
            else:
                disp += card.get_suit()+ card.get_rank() + ' '	# return a string representation of a hand
        return disp       
        
    def add_card(self, card):
        self.cards.append(card)	# add a card object to a hand
        
    def hideFirstCard(self, hidden):
        card = self.cards[0]
        card.hideCard(hidden)
        
    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        val = 0
        aceCount = 0
        for card in self.cards:	# compute the value of the hand, see Blackjack video
            val = val + VALUES.get(card.get_rank())
            if card.get_rank() == 'A':
                aceCount += 1 
        if (aceCount > 0) and (val + 10 <= 21):
            val += 10
        return val
    def draw(self, canvas, pos):
        horzGap = 10
        for card in self.cards:	# draw a hand on the canvas, use the draw method for cards
            card.draw(canvas, [pos[0], pos[1]])
            pos[0] += CARD_SIZE[0] + horzGap

        
# define deck class 
class Deck:
    def __init__(self):
        self.cards = [Card(S,R) for S in SUITS for R in RANKS]	# create a Deck object

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.cards)    # use random.shuffle()

    def deal_card(self):
        return self.cards.pop()	# deal a card object from the deck
    
    def __str__(self):
        disp = 'Deck contains '	# return a string representing the deck
        for card in self.cards:
            disp += card.get_suit() + card.get_rank() + ' '
        return disp

#define event handlers for buttons
def deal():
    global outcome, action, in_play, player, dealer, deck, score
    if in_play:
        score -= 1
    in_play = True
    outcome = ""
    action = 'Hit or Stand?'
    dealer = Hand("Dealer")
    player = Hand("Player")
    deck = Deck()
    deck.shuffle()
    for i in range(0,2):
        player.add_card(deck.deal_card())
    for i in range(0,2):
        dealer.add_card(deck.deal_card())
    dealer.hideFirstCard(True)
#    print dealer
#    print player
    
def hit():
    global player, outcome, score, in_play, action, dealer	# replace with your code below
    # if the hand is in play, hit the player
    if in_play:
        player.add_card(deck.deal_card())
        pVal = player.get_value()
        # if busted, assign a message to outcome, update in_play and score
        if pVal > 21:
            outcome = "You have busted and loose"
            dealer.hideFirstCard(False)
            action = "New deal?"
            in_play = False
            score -= 1 
    else:
        if not outcome.startswith("Deal? "):
            outcome = "Deal? " + outcome
def stand():
    global dealer, outcome, score, in_play, action
    if not in_play:	# replace with your code below
        if not outcome.startswith("Deal? "):
            outcome = "Deal? " + outcome
    else: # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
        dealer.hideFirstCard(False)
        dVal = dealer.get_value()        
        while dVal < 17:
            dealer.add_card(deck.deal_card())
            dVal = dealer.get_value()
        pVal = player.get_value()
        in_play = False
#        print pVal,dVal
        if dVal > 21:
            outcome = "Dealer is busted. You won."
            action = "New deal?"
            score += 1 
        elif pVal <= dVal:
            outcome = "You loose."
            action = "New deal?"
            score -= 1 
        else:
            outcome = "You won."
            action = "New deal?"
            score += 1 
    # assign a message to outcome, update in_play and score
      
# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    scores = 'Score = ' + str(score) 
    canvas.draw_text('Blackjack', (200, 75), 50, 'White', 'serif')
    canvas.draw_text(scores, (450, 110), 18, 'White', 'serif')
    canvas.draw_text('Dealer', (150, 150), 18, 'White', 'serif')
    canvas.draw_text(outcome, (350, 150), 18, 'White', 'serif')
    canvas.draw_text('Player', (150, 350), 18, 'White', 'serif')
    canvas.draw_text(action, (350, 350), 18, 'White', 'serif')
    
    dCardPos = [114,180]
    pCardPos = [114,380]
    dealer.draw(canvas, dCardPos)
    player.draw(canvas, pCardPos)


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