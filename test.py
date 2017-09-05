import blackjack

shoe1 = blackjack.Shoe(1)

print (shoe1.list)

Jones = blackjack.Player(False)

Jones.add_hand_to_player(shoe1,2)

print(Jones.hands[0].cards, Jones.hands[0].value(), Jones.hands[1].cards, Jones.hands[1].value())


