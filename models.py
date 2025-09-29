from dataclasses import dataclass
from random import shuffle, randint
from typing import Optional

SUITS = ["♥", "♦", "♣", "♠"]

RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

# fmt: off
VALUES = { "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
    "10": 10, "J": 10, "Q": 10, "K": 10,  "A": 11}
# fmt: on

PLAYERS = {
    "Tracy": {"name": "Tracy", "bankroll": 1000, "strategy": "BS17"},
    "Lena": {"name": "Lena", "bankroll": 1000, "strategy": "BS17"},
}

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
    is_active: bool
    
    def __init__(self, num_decks):
        self.decks = [Deck() for _ in range(num_decks)]
        self.cards = [card for deck in self.decks for card in deck.cards]

class DiscardTray:
    cards: list[Card]
    
    def __init__(self):
        self.cards = []
    
class Hand:
    cards: list[Card]
    is_active: bool
    is_busted: bool
    is_blackjack: bool
    
    def __init__(self):
        self.cards = []
            
class Dealer:
    def __init__(self, shoe: Shoe):
        self.name = "Dealer"
        self.shoe = shoe
    
    def prepare_shoe(self):
        cards = self.shoe.cards
        cutcard = CutCard()                                 # Create a cut card
        shuffle(cards)                                      # Shuffle the shoe
        cut_index = randint(10, len(cards)-10)              # Find a random cut position
        cards = cards[cut_index:] + cards[:cut_index]       # Complete the cut
        cards.insert(int(len(cards) * .75 + randint(-9,9)), # Place cutcard for
                     cutcard)                               # end of shoe
        self.shoe.cards = cards
        self.shoe.is_active = True
        
    def deal_card(self, hand: Hand):
        cards = self.shoe.cards
        new_card = cards.pop(0)
        if new_card == CutCard:
            self.shoe.is_active = False
            new_card = cards.pop(0)
        hand.cards.append(new_card)
        
    def initial_deal(self):
        pass

           

        
class Player:
    name: str
    # bankroll: float
    strategy: dict
    # bet: float

    def __init__(self, name: str, strategy: dict):
        self.name = name
        self.strategy = strategy
    
class Seat:
    is_occupied: bool
    hand: Optional[Hand]
    player: Optional[Player | Dealer]
    
    def __init__(self, ) -> None:
        pass
    
class Table:
    player_seats: list[Seat]
    shoe: Shoe
    num_decks = 6
    discard_tray = DiscardTray()        # Create a discard tray
    dealer: Dealer
    dealer_seat: Seat
    
    def __init__(self, num_seats) -> None: 
        self.player_seats = [Seat() for _ in range(num_seats)]
        self.dealer_seat = Seat()

    def prepare_game(self):
        self.shoe = Shoe(self.num_decks)
        self.dealer = Dealer(self.shoe)
        self.dealer_seat.player = self.dealer
        self.dealer.prepare_shoe()
        for card in self.shoe.cards:
            print(card)
            
class Round:
    is_active: bool
    table: Table
    seats: list[Seat]
    players: list[Player]
    
    def __init__(self, table: Table) -> None:
        self.table = table
        self.seats = table.player_seats
        self.players = [Player(player["name"], player["strategy"]) for player in PLAYERS.values()]
        # seat_players
        # deal initial cards
        # play out player hands
        # play out dealer hand
        # evaluate results
        # pay out (optional)
        pass
        
    def seat_players(self):
        for seat, player_name in zip(self.seats, self.players):
            seat.player = PLAYERS[name]
    
        
table = Table(6).prepare_game()





