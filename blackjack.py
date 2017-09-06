from random import randint

class Card(object):


    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return str(self.rank) + str(self.suit)

    def get_bjvalue(self):
        if self.rank in ('K', 'Q', 'J'):
            return 10
        if self.rank == 'A':
            return 11
        return int(self.rank)

class Deck(list):

    def __init__(self):
        self.deck = Deck.create_deck()

    @staticmethod
    def create_deck():
        suits = ['s', 'c', 'h', 'd']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        deck = []
        for suit in suits:
            for rank in ranks:
                deck.append(Card(rank, suit))
        return deck

class Shoe(list):

    def __init__(self, number_of_decks):
            self.list = self.build_shoe(number_of_decks)

    def build_shoe(self, number_of_decks):
        return self.shuffle(Deck().deck * number_of_decks)

    def shuffle(self, list):
        list_len = len(list)
        for i in range(0,list_len-2):
            j = randint(i, list_len-1)
            list[i], list[j] = list[j], list[i]
        return list

    def draw_cards(self, number_of_cards):
        cards = []
        for unused in range(0,number_of_cards):
            cards.append(self.list.pop())
        return cards

class Hand(list):

    def __init__(self, cards=[]):
        self.cards = cards
        self.is_bust = False
        self.state = 0

    def __repr__(self):
        out = ''
        for card in self.cards:
            out += str(card)
        return out

    def add_cards(self, cards):
        for card in cards:
            self.cards.append(card)

    def split_hand(self):
        new_hands = []
        for card in self.cards:
            new_hands.append(Hand(card))
        return new_hands

    def get_value(self): #sum the list of cards
        total = 0
        ace_count = 0
        for card in self.cards:
            total += Card.get_bjvalue(card)
            if card.rank == 'A':
                ace_count += 1
        for unused in range(0,ace_count):
            if total > 21:
                total -= 10
        return total

    def get_cards(self): #Return list of cards in hand
        return self.cards

class Player(object):

    def __init__(self, name, is_dealer=False, balance=1000):
        self.is_dealer = is_dealer
        self.balance = balance
        self.name = name

    def add_hand_to_player(self, shoe, number_of_hands, number_of_cards):
        for unused in range(number_of_hands):
            self.hands.append(Hand(shoe.draw_cards(number_of_cards)))

    def modify_balance(self, amount):
        self.balance += amount

    def get_hands(self):
        return self.hands

    def get_hands_values(self):
        hand_value_list = []
        for hand in self.hands:
            hand_value_list.append(Hand.get_value(hand))
        return hand_value_list

class Round(object):

    round_id = 0

    def __init__(self, shoe, players):
        self.shoe = shoe
        self.players = players
        self.wagers = {}
        Round.round_id += 1

    def add_player_to_round(self, player):
        self.players.append(player)

    def get_players(self):
        return self.players

    def set_player_wager(self, player, wager):
        self.wagers[player.name] = wager

class Menu(object):

    def __init__(self, state):
        self.state = state


    def menu(self):
        loop = True
        while loop:  ## While loop which will keep going until loop = False
            self.print_menu()  ## Displays menu
            choice = input("Enter your choice: ")
            if choice in ["1","h"]:
                return "Hit"
            elif choice in ["2","s"]:
                return "Stand"
            elif choice in ["3", "d"]:
                return "Double"
            elif choice == 4:
                return "Split"
            elif choice == 5:
                return "Surrender"
            loop = False  # This will make the while loop to end as not value of loop is set to False

    def print_menu(self):

        print(
            30 * "-", "Action", 30 * "-"
            )
        print(
             "1. Hit"
              )
        print(
             "2. Stand"
                   )
        if self.state == 1:

            print(
                 "3. Double"
                 )
        # print(
        # "4. Surrender"
        # )
        # print(
        #     "5. Split")
        print(
        67 * "-"
        )

class Game(object):

    def __init__(self):
        self.shoe = Shoe(6)
        self.players = [Player("Player1"), Player("Player2"), Player("Dealer", True)]
        self.current_round = Round(self.shoe, self.players)

    def start(self):

        for player in self.current_round.players:
            if player.is_dealer is False:
                wager = input("Enter your wager" + player.name + ":")
                self.current_round.set_player_wager(player, wager)
        print(self.current_round.wagers)


















