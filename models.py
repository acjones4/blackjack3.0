from dataclasses import dataclass
from random import shuffle, randint
from typing import Optional

SUITS = ["♥", "♦", "♣", "♠"]

RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

# fmt: off
VALUES = { "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
    "10": 10, "J": 10, "Q": 10, "K": 10,  "A": 11}
# fmt: on

@dataclass (frozen=True)
class Card:
    suit: Optional[str]
    rank: Optional[str]

class CutCard(Card):
    def __init__(self):
        super().__init__(suit = None, rank= None)

    def __str__(self):
        return 'Cut Card'

class Deck:
    cards: list[Card]
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in SUITS for rank in RANKS]

class Shoe:
    decks: list[Deck] = []
    cards: list[Card] = []
    
    
    def __init__(self, num_decks):
        self.decks = [Deck() for _ in range(num_decks)]
        self.cards = [card for deck in self.decks for card in deck.cards]

class DiscardTray:
    cards: list[Card]
    
    def __init__(self):
        self.cards = []
        
class Dealer:
    def __init__(self, shoe: Shoe):
        self.name = "Dealer"
        self.shoe = shoe
    
    def prepare_shoe(self):
        cards = self.shoe.cards
        cutcard = CutCard()                 # Create a cut card
        
        shuffle(cards)                      # Shuffle the shoe
        cut_index = randint(10, len(cards)-10)  # Find a random cut position
        cards = cards[cut_index:] + cards[:cut_index]   # Complete the cut
        cards.insert(int(len(cards) * .75 + randint(-9,9)), # Place cutcard for
                     cutcard)                               # end of shoe
           
class Hand:
    cards: list[Card]
    is_active: bool
    is_busted: bool
    is_blackjack: bool
    
    def __init__(self):
        self.cards = []
        
class Player:
    name: str
    # bankroll: float
    strategy: dict
    # bet: float
    
class Seat:
    is_occupied: bool
    hand: Optional[Hand]
    player: Optional[Player]
    
class Table:
    seats: list[Seat]
    shoe: Shoe
    num_decks = 6
    discard_tray = DiscardTray()        # Create a discard tray
    dealer: Dealer
    
    def __init__(self, num_seats) -> None: 
        self.seats = [Seat for _ in range(num_seats)]

    def prepare_game(self):
        self.shoe = Shoe(self.num_decks)
        self.dealer = Dealer(self.shoe)
        self.dealer.prepare_shoe()
        
        
        
        
