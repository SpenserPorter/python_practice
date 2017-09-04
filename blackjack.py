from random import randint

class Card():

	def __init__(self, card_name):
		self.name = card_name
		if card_name[0] == 'A':
			self.is_ace = True
		self.is_ace = False

	def bj_value(self): 
	    if self[0] in ("K", "Q", "J", "1"):
	        return 10
	    if self[0] == 'A': 
	        return 11
	    return int(self[0])

class Shoe():

	def __init__(self, number_of_decks):
		self.list = self.build_shoe(number_of_decks)

	def draw(self, number_of_cards):
		cards = []
		for unused in range(0,number_of_cards):
			cards.append(self.list.pop())
		return cards


	def shuffle(self, list):
	    list_len = len(list)
	    for i in range(0,list_len-2):
	        j = randint(i, list_len-1)
	        list[i], list[j] = list[j], list[i]
	    return list

	def build_shoe(self, number_of_decks):
	    suits = ['s', 'c', 'h', 'd']
	    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
	    deck = []
	    for suit in suits:
	        for rank in ranks:
	            deck.append(rank + suit)
	    return self.shuffle(deck * number_of_decks)

class Hand():

	def __init__(self, cards):
		self.cards = cards
		self.value = self.sum_cards(self.cards)
		self.is_bust = False
		self.state = 0

	def add_cards(self, cards):
		for card in cards:
			self.cards.append(card)
		self.value = self.sum_cards(self.cards)

	def sum_cards(self, list_of_cards): #sum the list of cards
	    total = 0
	    ace_count = 0
	    for card in list_of_cards:
	        total += Card.bj_value(card)
	        if Card(card).is_ace:
	            ace_count += 1
	    for unused in range(0,ace_count):
	        if total > 21:
	            total -= 10
	    return total

class player():
	def __init__(self, is_dealer):
		self.is_dealer = is_dealer
		self.hands =

class Menu():

	def __init__(self, hand):
		self.state = hand.state

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






