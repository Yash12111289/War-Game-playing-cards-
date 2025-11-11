import random
ranks=['2','3','4','5','6','7','8','9','10','Jack','Queen','King','Ace']
suits=['Hearts','Diamonds','Clubs','Spades']
values={r:i+2 for i,r in enumerate(ranks)}

class Card:
    def __init__(self,rank,suit):
        self.rank = rank
        self.suit = suit
        self.value = values[rank]
    def __str__(self):
        return f'{self.rank} of {self.suit}'

class Deck:
    def __init__(self):
        self.cards=[Card(r,s) for s in suits for r in ranks]
    def shuffle(self):
        random.shuffle(self.cards)
    def deal_one(self):
        return self.cards.pop()

class Player:
    def __init__(self,name):
        self.name = name
        self.pile=[]
    def remove_one(self):
        return self.pile.pop(0)
    def add_new(self,new_cards):
        if type(new_cards)==type([]):
            self.pile.extend(new_cards)
        else:
            self.pile.append(new_cards)
    def __str__(self):
        return f'Player {self.name} has {len(self.pile)} cards'

#========================  game logic  ====================================
p1=Player('chinni')
p2=Player('yash')
new_deck=Deck()
new_deck.shuffle()
for x in range(26):
    p1.add_new(new_deck.deal_one())
    p2.add_new(new_deck.deal_one())
game_on=True
round_count=0
while game_on:
    round_count+=1
    if len(p1.pile)==0 or len(p2.pile)==0:
        winner=p1.name if len(p1.pile)<5 else p2.name
        print(f'Player {winner} has won!')
        game_on=False
        break
    p1_card=[p1.remove_one()]
    p2_card=[p2.remove_one()]
    war=True
    while war:
        if p1_card[-1].value > p2_card[-1].value:
            p1.add_new(p1_card+p2_card)
            war=False

        elif p1_card[-1].value < p2_card[-1].value:
            p2.add_new(p1_card+p2_card)
            war=False
        else:
            if len(p1.pile)<5:
                print(f"Player {p1.name} out of cards Player {p2.name} won the match")
                war=False
                game_on=False
                break
            elif len(p2.pile)<5:
                print(f"Player {p2.name} out of cards Player {p1.name} won the match")
                war=False
                game_on=False
                break
            else:
                for _ in range(5):
                    p1_card.append(p1.remove_one())
                    p2_card.append(p2.remove_one())
print("gave over")
