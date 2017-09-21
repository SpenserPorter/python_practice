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

    def __init__(self, cards):
        self.cards = []
        self.add_cards(cards)
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

    def get_cards(self, card_index=None): #Return list of cards in hand
        if card_index is not None:
            return self.cards[card_index]
        return self.cards

class Player(object):

    def __init__(self, name, is_dealer=False, balance=1000):
        self.is_dealer = is_dealer
        self.balance = balance
        self.name = name

    def get_balance(self):
        return self.balance

    def modify_balance(self, amount):
        self.balance += amount

class Round(object):

    round_id = 0

    def __init__(self, shoe, players):
        self.shoe = shoe
        self.ledger = {}
        for player in players:
            self.add_player_to_round(player)
        Round.round_id += 1

    def add_player_to_round(self, player): #add player to ledger with with 1st wager/hand
        self.ledger[player.name] = [[0, None]]

    def get_players(self):
        player_list = []
        for p in self.ledger:
            player_list.append(p)
        return player_list

    def set_player_wager(self, player, wager, hand_index):
        self.ledger[player.name][hand_index][0] = wager

    def get_player_wager(self, player, hand_index=0):
        return self.ledger[player.name][hand_index][0]

    def add_hand_to_player(self, player, hand_index, cards=None):
        if player not in self.ledger:
            self.add_player_to_round(player)
        if cards is not None:
            self.ledger[player.name][hand_index][1] = Hand(cards)
        else:
            self.ledger[player.name][hand_index][1] = Hand(self.shoe.draw_cards(2))

    def get_player_hand(self, player_name, hand_index = 0):
        return self.ledger[player_name][hand_index][1]


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

        print(30 * "-", "Action", 30 * "-")
        print("1. Hit")
        print("2. Stand")
        if self.state == 1:
            print("3. Double")
        # print("4. Surrender")
        # print("5. Split")
        print(67 * "-")

class Game(object):

    def __init__(self, number_of_players):
        self.shoe = Shoe(6)
        self.players = [Player("Dealer", True)]
        self.initialize_player_list(number_of_players)
        self.current_round = Round(self.shoe, self.players)

    def initialize_player_list(self, number_of_players):
        for i in range(1, number_of_players + 1):
            name = "Player" + str(i)
            self.players.append(Player(name))

    def start(self):

        print ("Round", self.current_round.round_id)

        for player in self.players:

            if not player.is_dealer:

                print (player.name + "'s balance is " + str(player.balance))
                place_bet = input("Place your bet " + player.name + ":")

                while True: #validate bet is an integer between 1 and total balance
                    try:
                        wager = int(place_bet)
                        if wager in range(1, player.get_balance() + 1):
                            break
                        place_bet = input("Please enter a valid bet " + player.name + ":")
                    except ValueError:
                        place_bet = input("Please enter a valid bet " + player.name + ":")
                print("Test1")
                player.modify_balance(-1 * wager)
                print("Test2")
                self.current_round.set_player_wager(player, wager, 0)
                print("Test4")

            self.current_round.add_hand_to_player(player, 0)

        print("Dealer shows: %s X" % (self.current_round.get_player_hand("Dealer").get_cards(0)))


#test
        print(self.current_round.ledger)

        for player in self.players:
            print(self.current_round.ledger[player.name][0][0])
            print(player.name, player.balance, self.current_round.ledger[player.name])




















