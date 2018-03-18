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
        if total > 21:
            self.is_bust = True
        return total

    def is_blackjack(self):
        if self.get_value() == 21 and len(self.cards) == 2:
            return True
        return False

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

class HandWagerPair(object):

    def __init__(self, hand, wager):
        self.hand = hand
        self.wager = wager

    def __repr__(self):
        return str(self.wager) + ' - ' + str(self.hand)

    def set_wager(self, wager):
        self.wager = wager

    def set_hand(self, hand):
        self.hand = hand

    def get_hand(self):
        return self.hand

    def get_wager(self):
        return self.wager


class Round(object):

    round_id = 0

    def __init__(self, shoe, players):
        self.shoe = shoe
        self.ledger = {}
        self.game_state = 1
        for player in players:
            self.add_player_to_round(player)
        Round.round_id += 1

    def add_player_to_round(self, player):  # add player to ledger with with 1st wager/hand
        self.ledger[player.name] = None

    def get_players(self):
        player_list = []
        for p in self.ledger:
            player_list.append(p)
        return player_list

    def set_player_wager(self, player, wager, hand_index=0):
        self.ledger[player.name][hand_index].set_wager(wager)

    def get_player_wager(self, player, hand_index=0):
        return self.ledger[player.name][hand_index].get_wager()

    def add_hand_to_player(self, player, hand_index, cards=None):
        if player not in self.ledger:
            self.add_player_to_round(player)
        if cards is not None:
            self.ledger[player.name][hand_index].set_hand(Hand(cards))
        else:
            self.ledger[player.name][hand_index].set_hand(Hand(self.shoe.draw_cards(2)))

    def get_player_hand(self, player, hand_index = 0):
        return self.ledger[player][hand_index].get_hand()

    def get_result(self, player):
        player_value = self.get_player_hand(player).get_value()
        dealer_value = self.get_player_hand("Dealer").get_value()
        if self.get_player_hand(player).is_bust:
            return False
        if player_value == dealer_value:
            return "Push"
        elif player_value < dealer_value:
            return "Lose"
        elif player_value > dealer_value:
            return "Win"


class Menu(object):

    def __init__(self, state):
        self.state = state

    def menu(self, player):
        loop = True
        while loop:  # While loop which will keep going until loop = False
            self.print_menu(player)  # Displays menu
            choice = input("Enter your choice: ")
            if choice in ["1","h","H"]:
                return "Hit"
            elif choice in ["2","s","S"]:
                return "Stand"
            elif choice in ["3", "d","D"]:
                return "Double"
            elif choice == 4:
                return "Split"
            elif choice == 5:
                return "Surrender"
            loop = False  # This will make the while loop end


    def print_menu(self, player):

        print(30 * "-", player.name + " Action", 30 * "-")
        print("1. Hit")
        print("2. Stand")
        if self.state == 1:
            print("3. Double Down!")
            self.state = 3
        # print("4. Surrender")
        # print("5. Split")
        print((72 + len(player.name)) * "-")

class Game(object):

    def __init__(self, number_of_players):
        self.shoe = Shoe(6)
        self.players = []
        self.initialize_player_list(number_of_players)
        self.current_round = Round(self.shoe, self.players)

    def initialize_player_list(self, number_of_players):
        for i in range(1, number_of_players + 1):
            name = "Player" + str(i)
            self.players.append(Player(name))
        self.players.append(Player("Dealer", True))

    def next_round(self, shoe, players):
        self.current_round = Round(shoe, players)
        self.start()

    def start(self):

        while True:

            print ("Round", self.current_round.round_id)

            for player in self.players:

                wager = 0

                if not player.is_dealer:

                    print ("%s balance is %i" % (player.name, player.balance))
                    place_bet = input("Place your bet " + player.name + ":")

                    while True: #validate bet is an integer between 1 and total balance
                        try:
                            wager = int(place_bet)
                            if wager in range(1, player.get_balance() + 1):
                                break
                            place_bet = input("Please enter a valid bet " + player.name + ":")
                        except ValueError:
                            place_bet = input("Please enter a valid bet " + player.name + ":")

                    player.modify_balance(-1 * wager)

                self.current_round.ledger[player.name] = [HandWagerPair(Hand(self.current_round.shoe.draw_cards(2)), wager)]


            for player in self.players:
                if not player.is_dealer:
                    first_decision = True
                    #check if player can double based on wager/balance
                    if player.get_balance() >= self.current_round.get_player_wager(player):
                        self.current_round.game_state = 1
                    else:
                        self.current_round.game_state = 2

                    while True:
                        if first_decision:
                            print("Dealer shows: %s X" % (self.current_round.get_player_hand("Dealer").get_cards(0)))
                            print("%s's hand: %s %i total" % (player.name, self.current_round.get_player_hand(player.name), self.current_round.get_player_hand(player.name).get_value()))
                            first_decision = False


                        if self.current_round.get_player_hand(player.name).is_blackjack():
                            print ("%s Blackjack!, Win %f!" % (player.name, 2.5 * self.current_round.get_player_wager(player)))
                            player.modify_balance(2.5 * self.current_round.get_player_wager(player))
                            break

                        action = Menu(self.current_round.game_state).menu(player)

                        if action == "Hit" or action == "Double":
                            self.current_round.game_state = 2
                            self.current_round.get_player_hand(player.name).add_cards(self.current_round.shoe.draw_cards(1))
                            if not self.current_round.get_result(player.name):
                                print("Dealer shows: %s X" % (self.current_round.get_player_hand("Dealer").get_cards(0)))
                                print("%s's hand: %s %i total" % (player.name, self.current_round.get_player_hand(player.name), self.current_round.get_player_hand(player.name).get_value()))
                                print("%s Bust!" % (player.name))
                                break
                            else:
                                if action == "Double":
                                    player.modify_balance(-1 * self.current_round.get_player_wager(player))
                                    self.current_round.ledger[player.name][0].set_wager(self.current_round.get_player_wager(player) * 2)
                                    print("%s doubles to %i" %(player.name,self.current_round.get_player_wager(player)))
                                    print("%s hand: %s %i total" % (player.name, self.current_round.get_player_hand(player.name), self.current_round.get_player_hand(player.name).get_value()))
                                    break
                                else:
                                    print("Dealer shows: %s X" % (self.current_round.get_player_hand("Dealer").get_cards(0)))
                                    print("%ss hand: %s %i total" % (player.name, self.current_round.get_player_hand(player.name), self.current_round.get_player_hand(player.name).get_value()))

                        if action == "Stand":
                            break

            #Start dealer logic    

            while self.current_round.get_player_hand("Dealer").get_value() < 17:

                self.current_round.get_player_hand("Dealer").add_cards(self.current_round.shoe.draw_cards(1))
                print("Dealer draws 1 and shows %s, %i total" % (self.current_round.get_player_hand(player.name), self.current_round.get_player_hand(player.name).get_value()))

            if self.current_round.get_player_hand("Dealer").is_bust:
                print("Dealer busts!")
                for player in self.players:
                    if not self.current_round.get_player_hand(player.name).is_bust and not player.is_dealer:
                        print("%s wins %i!" % (player.name, 2 * self.current_round.get_player_wager(player)))
                        player.modify_balance(2 * self.current_round.get_player_wager(player))


            else:

                print("Dealer shows %s %i total" % (self.current_round.get_player_hand("Dealer"),self.current_round.get_player_hand("Dealer").get_value()) )

                for player in self.players:
                    if not self.current_round.get_player_hand(player.name).is_bust and not player.is_dealer and not self.current_round.get_player_hand(player.name).is_blackjack:
                        result = self.current_round.get_result(player.name)
                        if result == "Push":
                            print("%s %s %i total, Pushes, wager %i returned" % (player.name, self.current_round.get_player_hand(player.name),self.current_round.get_player_hand(player.name).get_value(), self.current_round.get_player_wager(player)))
                            player.modify_balance(self.current_round.get_player_wager(player))
                        elif result == "Win":
                            print("%s %s %i total, Wins %i!" % (player.name, self.current_round.get_player_hand(player.name),self.current_round.get_player_hand(player.name).get_value(), 2 * self.current_round.get_player_wager(player)))
                            player.modify_balance(2 * self.current_round.get_player_wager(player))
                        else:
                            print("%s %s %i total, Loses %i shit!!" % (player.name, self.current_round.get_player_hand(player.name),self.current_round.get_player_hand(player.name).get_value(), self.current_round.get_player_wager(player)))

            self.next_round(self.shoe, self.players)






















#test

        # for player in self.players:
        #     print(player.name, player.balance, self.current_round.ledger[player.name])




















