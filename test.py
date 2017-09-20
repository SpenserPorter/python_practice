import blackjack
# card1 = blackjack.Card('5','h')
# card2 = blackjack.Card('A','d')
# hand1 = blackjack.Hand([card1, card2])

# print(hand1, hand1.get_value(), hand1.get_cards(0))

number_of_players = input("How many Players?: ")
while True:
    try:
        players = int(number_of_players)
        game1 = blackjack.Game(players)
        break
    except ValueError:
        number_of_players = input("How many Players?: ")

game1.start()

