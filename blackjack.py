from random import randint

class Card(object):


    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return str(self.rank) + str(self.suit)

    def bj_value(self): 
        if self.rank in ('K', 'Q', 'J'):
            return 10
        if self.rank == 'A': 
            return 11
        return int(self.rank)

class Deck(list):

    def __init__(self):
        self.deck = self.build_deck()
            
    def build_deck(self):
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

    def draw(self, number_of_cards):
        cards = []
        for unused in range(0,number_of_cards):
            cards.append(self.list.pop())
        return cards
                    
class Hand(object):

    def __init__(self, cards):
        self.cards = cards
        self.is_bust = False
        self.state = 0

    def add_cards(self, cards):
        for card in cards:
            self.cards.append(card)

    def value(self): #sum the list of cards
        total = 0
        ace_count = 0
        for card in self.cards:
            total += Card.bj_value(card)
            if card.rank == 'A':
                ace_count += 1
        for unused in range(0,ace_count):
            if total > 21:
                total -= 10
        return total

class Player(object):

    def __init__(self, is_dealer):
        self.is_dealer = is_dealer
        self.hands = []
        self.balance = 1000

    def add_hand_to_player(self, shoe, number_of_hands):
        for unused in range(number_of_hands):
            self.hands.append(Hand(shoe.draw(2))) #hands always start with 2 cards


#Todo list
# class Round(object):

# class Game(object):


# class Menu(object):

#       def __init__(self, hand):
#               self.state = hand.state

#       def menu(self):
#               loop = True
#               while loop:  ## While loop which will keep going until loop = False
#                       self.print_menu()  ## Displays menu
#                   choice = input("Enter your choice: ")
#                   if choice in ["1","h"]:
#                       return "Hit"               
#                   elif choice in ["2","s"]:
#                       return "Stand"
#                   elif choice in ["3", "d"]:
#                       return "Double"  
#                   elif choice == 4:
#                       return "Split"
#                   elif choice == 5:
#                       return "Surrender"     
#                   loop = False  # This will make the while loop to end as not value of loop is set to False

#     def print_menu(self):

#     print(
#          30 * "-", "Action", 30 * "-"
#         )
#     print(
#          "1. Hit"
#           )
#     print(
#          "2. Stand"
#                )
#     if self.state == 1:

#         print(
#              "3. Double"
#              )
#     # print(
#     # "4. Surrender"
#     # )
#     # print(
#     #     "5. Split")
#     print(
#     67 * "-"
#     )






