import blackjack

shoe1 = blackjack.Shoe(1)

print (shoe1.list)

player1_hand = blackjack.Hand("Player1", shoe1.draw(2))

print (player1_hand.person, player1_hand.cards, player1_hand.value)
