import random

class Card:
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    rank_values = {rank: i + 2 for i, rank in enumerate(ranks)}

    def __init__(self, rank, suit):
        if rank not in Card.ranks or suit not in Card.suits:
            raise ValueError("Invalid rank or suit")
        self.rank = rank
        self.suit = suit

    @property
    def value(self):
        return Card.rank_values[self.rank]

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def __eq__(self, other):
        return self.value == other.value

class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit) for suit in Card.suits for rank in Card.ranks]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop() if self.cards else None

    def deal_half(self):
        half = len(self.cards) // 2
        return self.cards[:half], self.cards[half:]

class Player:
    def __init__(self, name):
        self.name = name
        self.pile = []

    def has_cards(self):
        return len(self.pile) > 0

    def play_card(self):
        return self.pile.pop(0) if self.pile else None  # FIFO

    def receive_cards(self, cards):
        self.pile.extend(cards)  # add to bottom

    def card_count(self):
        return len(self.pile)

class WarGame:
    def __init__(self, player1_name, player2_name):
        self.p1 = Player(player1_name)
        self.p2 = Player(player2_name)
        self.turn_count = 0
        self.war_count = 0
        self.max_turns = 10000  # safety to avoid infinite loops

    def setup(self):
        deck = Deck()
        pile1, pile2 = deck.deal_half()
        self.p1.receive_cards(pile1)
        self.p2.receive_cards(pile2)

    def play_round(self):
        if not self.p1.has_cards() or not self.p2.has_cards():
            return False

        self.turn_count += 1
        table_cards = []

        card1 = self.p1.play_card()
        card2 = self.p2.play_card()
        table_cards.extend([card1, card2])

        if card1 > card2:
            self.p1.receive_cards(table_cards)
        elif card2 > card1:
            self.p2.receive_cards(table_cards)
        else:
            # WAR scenario
            self.handle_war(table_cards)

        return True

    def handle_war(self, table_cards):
        self.war_count += 1
        print(f"\n⚔️  WAR! (Turn {self.turn_count})")

        while True:
            if not self.p1.has_cards() or not self.p2.has_cards():
                return

            # each player puts down 3 face-down and 1 face-up if possible
            facedown = 3
            war_pile = []

            for _ in range(facedown):
                if self.p1.has_cards():
                    war_pile.append(self.p1.play_card())
                if self.p2.has_cards():
                    war_pile.append(self.p2.play_card())

            if not self.p1.has_cards() or not self.p2.has_cards():
                return

            c1 = self.p1.play_card()
            c2 = self.p2.play_card()
            war_pile.extend([c1, c2])
            table_cards.extend(war_pile)

            if c1 > c2:
                self.p1.receive_cards(table_cards)
                break
            elif c2 > c1:
                self.p2.receive_cards(table_cards)
                break
            else:
                print("Another tie — continuing WAR!")
                continue  # another tie → new loop

    def play_game(self):
        self.setup()
        print("Starting the War Game...\n")

        while self.p1.has_cards() and self.p2.has_cards() and self.turn_count < self.max_turns:
            self.play_round()

        self.show_result()

    def show_result(self):
        print("\n------ GAME OVER ------")
        print(f"Total turns: {self.turn_count}, Wars: {self.war_count}")
        if self.p1.has_cards() and not self.p2.has_cards():
            print(f"🏆 Winner: {self.p1.name}")
        elif self.p2.has_cards() and not self.p1.has_cards():
            print(f"🏆 Winner: {self.p2.name}")
        else:
            print("It's a draw (turn limit reached)!")


# -------------------- Run Game --------------------
if __name__ == "__main__":
    game = WarGame("Yaswanth", "Computer")
    game.play_game()
