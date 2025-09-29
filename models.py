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

    def __init__(self, table: "Table"):
        self.name = "Dealer"
        self.table = table
    
    def prepare_shoe(self):
        cards = self.table.shoe.cards
        discard_tray = self.table.discard_tray
        cutcard = CutCard()                                     # Create a cut card
        shuffle(cards)                                          # Shuffle the shoe
        cut_index = randint(10, len(cards)-10)                  # Find a random cut position
        cards = cards[cut_index:] + cards[:cut_index]           # Complete the cut
        cards.insert(int(len(cards) * .75 + randint(-9,9)),     # Place cutcard for
                     cutcard)                                   # end of shoe
        self.table.shoe.cards = cards
        discard_tray.cards.append(self.table.shoe.cards.pop(0)) # Burn top card to discard tray
        self.table.shoe.is_active = True
        
    def deal_card(self, hand: Hand):
        cards = self.table.shoe.cards
        new_card = cards.pop(0)
        if new_card == CutCard:
            self.table.shoe.is_active = False
            new_card = cards.pop(0)
        hand.cards.append(new_card)
        
    def initial_deal(self):
        cards = self.table.shoe.cards
        player_seats = self.table.player_seats
        dealer_seat = self.table.dealer_seat
        for seat in player_seats:
            seat.hand = Hand()
        dealer_seat.hand = Hand()
        for _ in range(2):
            for seat in player_seats:
                assert seat.hand is not None
                self.deal_card(seat.hand)
            self.deal_card(dealer_seat.hand)


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
        self.is_occupied = False
        self.hand = None
        self.player = None
 
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
        self.dealer = Dealer(self)
        self.dealer_seat.player = self.dealer
        self.dealer.prepare_shoe()        
            
class Round:
    is_active: bool
    table: Table
    seats: list[Seat]
    players: list[Player]
    dealer: Dealer
    
    def seat_players(self):
        for seat, player in zip(self.seats, self.players):
            seat.player = player
            seat.is_occupied = True

    def __init__(self, table: Table) -> None:
        self.table = table
        self.seats = table.player_seats
        self.players = [Player(player["name"], player["strategy"]) for player in PLAYERS.values()]
        self.dealer = table.dealer
        self.seat_players()
        self.dealer.initial_deal()
        # deal initial cards
        # play out player hands
        # play out dealer hand
        # evaluate results
        # pay out (optional)
        pass
        

        


table = Table(6)
table.prepare_game()
round = Round(table)





