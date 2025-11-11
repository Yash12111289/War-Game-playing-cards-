import random

ranks = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
values = {r: i+2 for i, r in enumerate(ranks)}

class Deck:
    def __init__(self):
        self.cards = ranks * 4
    def shuffle(self):
        random.shuffle(self.cards)
    def split(self):
        return self.cards[:26], self.cards[26:]

class Player:
    def __init__(self, name):
        self.name = name
        self.cards = []
    def receive(self, cards):
        self.cards = cards
    def play_card(self):
        return self.cards.pop(0) if self.cards else None
    def add_cards(self, won_cards):
        if isinstance(won_cards, list):
            self.cards.extend(won_cards)
        else:
            self.cards.append(won_cards)

class Game:
    def __init__(self):
        print("Welcome to the War Card Game!")
        self.deck = Deck()
        self.p1 = Player("Yash")
        self.p2 = Player("Chinni")
    def setup(self):
        self.deck.shuffle()
        c1, c2 = self.deck.split()
        self.p1.receive(c1)
        self.p2.receive(c2)
        print(f"Game started between {self.p1.name} and {self.p2.name}!\n")
    def war(self):
        if not self.p1.cards or not self.p2.cards:
            return
        c1 = self.p1.play_card()
        c2 = self.p2.play_card()
        table = [c1, c2]
        if c1 is None or c2 is None:
            return
        if values[c1] > values[c2]:
            self.p1.add_cards(table)
        elif values[c2] > values[c1]:
            self.p2.add_cards(table)
        else:
            self.handle_war(c1, c2, table)
    def handle_war(self, c1, c2, table):
        while values[c1] == values[c2]:#war condition
            if len(self.p1.cards) < 4 or len(self.p2.cards) < 4:# not enough cards
                return
            war_c1 = [self.p1.play_card() for _ in range(3)]
            war_c2 = [self.p2.play_card() for _ in range(3)]
            c1 = self.p1.play_card()
            c2 = self.p2.play_card()
            table += war_c1 + war_c2 + [c1, c2]
        if values[c1] > values[c2]:# Winner takes all cards on the table
            self.p1.add_cards(table)
        else:
            self.p2.add_cards(table)
    def check_winner(self):
        if not self.p1.cards:# Check if any player ran out of cards
            print(f"{self.p2.name} wins the game!")
            return True
        elif not self.p2.cards:
            print(f"{self.p1.name} wins the game!")
            return True
        return False
    def start(self):
        # Main game loop
        self.setup()
        while not self.check_winner():
            self.war()
        print("Game Over.")

g = Game()
g.start()
