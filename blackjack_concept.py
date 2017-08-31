import random


def build_deck():
    suits = ['s', 'c', 'h', 'd']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    deck = []
    for suit in suits:
        for rank in ranks:
            deck.append(rank + suit)
    return deck

deck = build_deck()

def shuffle(list): #Fisher-Yates shuffle
    list_len = len(list)
    for i in range(0,list_len-2):
        j = random.randint(i, list_len-1)
        list[i], list[j] = list[j], list[i]
    return list


def shuffled_decks(n):
    return shuffle(deck * n) #Return n shuffled decks as a list

def draw_cards(deck, n): #Draw n cards from deck, return cards drawn as a list, and the remaining cards in the deck
    cards_drawn = []
    for unused in range(0,n):
        cards_drawn.append(deck.pop())
    return cards_drawn, deck

def sum_cards(list_of_cards): #sum the list of cards
    sum = 0
    ace_count = 0
    for card in list_of_cards:
        sum += card_value(card)
        if card[0][0] == 'A':
            ace_count += 1
    for unused in range(0,ace_count):
        if sum > 21:
            sum -= 10
    return sum


def card_value(card): #detemine blackjack value of cards from strings
    if card[0][0] in ("K", "Q", "J", "1"):
        return 10
    if card[0][0] == 'A': #treat Ace as 11, 11/1 case handled in sum_cards
        return 11
    return int(card[0][0])


def print_menu(game_state):  ## Your menu design here
    print(
    30 * "-", "Action", 30 * "-")
    print(
    "1. Hit"
    )
    print(
    "2. Stand"
    )
    if game_state == 1:
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

def choice_menu(game_state):
        loop = True
        while loop:  ## While loop which will keep going until loop = False
            print_menu(game_state)  ## Displays menu
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

def add_result_to_index(index, player_cards, dealer_cards, wager, result, balance):
    hand_number = len(index) + 1
    index[hand_number] = [player_cards,dealer_cards,wager,result,balance]

def win_rate(index):
    wins = 0
    push_count = 0
    result = None
    total_hands = len(index)
    if total_hands > 0:
        for hand in index:
            if index[hand][3] in ["Win", "Player Blackjack"]:
                wins += 1
            if index[hand][3] == "Push":
                push_count += 1
        result = wins / (total_hands - push_count)
    return result

def blackjack():

    deck = shuffled_decks(6) #initialize shoe of 6 decks
    play_another = True #placeholder, always continue for now
    game_state = 1 #for tracking what options to present to player
    balance = 1000

    while play_another: # placeholder, who doesn't want to keep playing?

        if len(deck) < 52: #Re-shuffle after 1 deck remains
            deck = shuffled_decks(6)
            print("Reshuffling shoe")

        if balance <= 0: #not much fun otherwise
            print ("Balance reset")
            balance = 1000

        print ("Your balance %d" % (balance)) #Display current balance

        if win_rate(index):

            print ("Current winrate is %d%%" % (win_rate(index) * 100))

        bet = int(input("Place your wager: ")) #Allow input, currently breaks on non int type strings

        while bet not in range(1,int(balance+1)): #Reject invalid wagers, possible for float balance due to blackjack payouts, not sure how to handle that
            print("Please input a valid wager")
            bet = int(input("Place your wager: "))

        balance -= bet #subtract bet from balance

        player,deck = draw_cards(deck, 2) #draw initiale cards
        dealer,deck = draw_cards(deck, 2)

#check for blackjack for player and dealer, if none continue.

        if sum_cards(player) == 21 and sum_cards(dealer) != 21:
            print ("Your cards: %s Blackjack, player wins %d!" % (player, bet * 2.5))
            print ("Dealer Shows: %s X" % (dealer[0]))
            balance +=  2.5 * bet
            result = "Player Blackjack"

        elif sum_cards(dealer) == 21 and sum_cards(player) != 21:
            print ("Your cards: %s for a total of %d" % (player, sum_cards(player) ))
            print ("Dealer shows %s %s Blackjack, shit!" % (dealer[0], dealer[1]))
            result = "Dealer Blackjack"

        elif sum_cards(dealer) == 21 and sum_cards(player) == 21:
            print ("Your cards: %s Blackjack!" % (player))
            print ("Dealer shows %s Also Blackjack, that's a push!" % (dealer))
            balance += bet
            result = "Push"

#game only continues if neither player has blackjack

        elif sum_cards(player) != 21 and sum_cards(dealer) != 21: 
            print ("Your cards: %s for a total of %d" % (player, sum_cards(player) ))
            print ("Dealer Shows: %s X" % (dealer[0]))

            game_state = 0 #initial game state, first decision
            if balance // bet >= 1:  # allow double only if balance is more than twice bet
                game_state = 1

            while True: #Start of decision loop

                action = choice_menu(game_state)

                if action == "Hit" or action == "Double":

                    game_state = 2 #Double not available after first decision

                    if action == "Double":
                        print ("Player doubles to %d, hitting 1 card" % (2*bet))
                        balance -= bet #subtract another bet from balance
                        bet = bet * 2 #double the bet

                    next_card,deck = draw_cards(deck,1) #draw 1 card and append to player hand
                    player.append(next_card[0])

                    print ("Your cards: %s for a total of %d" % (player, sum_cards(player)))

                    if action == "Hit": #avoid unneccesary repitation if doubling

                        print ("Dealer Shows: %s X" % (dealer[0]))

                    if sum_cards(player) > 21: #check for bust on each hit/double
                        print ("Busted! You lose")
                        print ("Dealer reveals %s for a total of %d" % (dealer, sum_cards(dealer)))
                        result = "Lose"
                        break #end decision loop, return to start

                if action == "Stand" or action == "Double":

                    if action == "Stand": #Avoid unnecesarry repittion if doubling
                        print ("Your cards: %s for a total of %d" % (player, sum_cards(player)))

                    print ("Dealer reveals %s for a total of %d" % (dealer, sum_cards(dealer)))

                    while sum_cards(dealer) < 17: #Dealers action loop, stand on soft 17
                        next_card, deck = draw_cards(deck,1)
                        dealer.append(next_card[0])
                        print ("Dealer hits")
                        print ("Dealer shows %s for a total of %d" % (dealer, sum_cards(dealer)))

                    if sum_cards(dealer) > 21:
                        print ("Dealer busts!!")
                        print ("Player wins %d!!"% (2*bet))
                        balance += 2 * bet
                        result = "Win"

                    elif sum_cards(player) > sum_cards(dealer):
                        print("Player wins %d!" % (bet * 2))
                        balance += 2 * bet
                        result = "Win"

                    elif sum_cards(player) == sum_cards(dealer):
                        print("That's a push, players bet of %d returned" % (bet))
                        balance += bet
                        result = "Push"

                    elif sum_cards(player) < sum_cards(dealer):

                        print("You lost, shits rigged!")
                        result = "Lose"

                    break #end of turn, return to start

        add_result_to_index(index, player, dealer, bet, result, balance)


            

index = {}

blackjack()