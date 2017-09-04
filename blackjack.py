from random import randint

class Card():

	def __init__(self, card_name):
		self.name = card_name

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

	def __init__(self, person, cards):
		self.person = person
		self.cards = cards
		self.value = self.sum_cards(self.cards)

	def sum_cards(self, list_of_cards): #sum the list of cards
	    total = 0
	    ace_count = 0
	    for card in list_of_cards:
	        total += Card.bj_value(card)
	        if card[0][0] == 'A':
	            ace_count += 1
	    for unused in range(0,ace_count):
	        if total > 21:
	            total -= 10
	    return total







