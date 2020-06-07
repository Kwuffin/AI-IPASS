"""Some of the code is inspired by various people online."""

from random import randint


cards = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
cardValues = {
    'A': 11, 'a': 1,
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10
}
cardCounter = {}
hasSplit = False
hasBet = False
betAmount = 0

"""There are 8 decks in one game of blackjack, and four of the same value cards in one deck."""
for card in cards:
    cardCounter[card] = 32


def drawCard():
    available = True
    while available:
        card = cards[randint(0, 12)]
        if cardCounter[card] <= 0:
            cardCounter[card] = cardCounter[card] - 1
        else:
            available = False
    return card


def split(deck):
    deck1 = []
    deck2 = []
    allDecks = [deck1, deck2]
    deck1.append(deck[0])
    deck2.append(deck[1])
    print("Splitting deck:")
    print("Deck 1:", deck1[0])
    print("Deck 2:", deck2[0])
    print("\n")
    for deck in allDecks:
        print("Your current deck:\n", deck[0])
        print("")
        pChoice = input("Would you like to hit or stand?\n> ")
        pChoice.lower()
        if pChoice == "hit":
            while pChoice == "hit":
                deck.append(drawCard())
                deck = checkAce(deck)
                print("Player:")
                for card in deck:
                    print(card, end= ' ')
                print("\nTotal:", getValue(deck))
                if checkBust(deck):
                    break
                if checkBlackjack(deck):
                    break
                print("")
                pChoice = input("Would you like to hit or stand?\n> ")
                print("=============================================================================================")
    return allDecks


def player():
    pDeck = []
    pDeck.append(drawCard())
    pChoice = "hit"
    while pChoice == "hit":
        pDeck.append(drawCard())
        pDeck = ["2", "2"]
        pDeck = checkAce(pDeck)
        print("Player:")
        for card in pDeck:
            print(card, end= ' ')
        print("\nTotal:", getValue(pDeck))
        if checkBust(pDeck):
            break
        if checkBlackjack(pDeck):
            break
        print("=============================================================================================")
        if pDeck[0] == pDeck[1]:
            pChoice = input("Would you like to hit, stand or split?\n> ")
            pChoice.lower()
        else:
            go = False
            while not go:
                pChoice = input("Would you like to hit or stand?\n> ")
                pChoice.lower()
                if pChoice != "hit" and pChoice != "stand":
                    print("\nThat's not an option.\n")
                else:
                    go = True
    if pChoice == "split":
        global hasSplit
        global betAmount
        hasSplit = True
        betAmount *= 2
        return split(pDeck)
    else:
        return pDeck


def dealerFirst():
    dDeck = [drawCard(), drawCard()]
    return dDeck


def dealerAfter(dDeck):
    while getValue(dDeck) < 17:
        print("Dealer:\n"
              "Value:", getValue(dDeck), "\n")
        newCard = drawCard()
        dDeck.append(newCard)
        dDeck = checkAce(dDeck)
        print("\nDraws", newCard)
        print("Value:", getValue(dDeck))
    return dDeck


def getValue(deck):
    value = 0
    for card in deck:
        value += cardValues[card]
    return value


def checkAce(deck):
    value = getValue(deck)
    for card in deck:
        if cardValues[card] == 11 and value > 21:
            acePos = deck.index("A")
            deck[acePos] = "a"
    return deck


def checkBust(deck):
    if getValue(deck) > 21:
        return True


def checkBlackjack(deck):
    if getValue(deck) == 21:
        return True


def deckCompare(pDeck, dDeck):
    dealerWin = 0
    playerWin = 0
    pValue = getValue(pDeck)
    dValue = getValue(dDeck)
    if checkBust(pDeck): #  If player busts.
        dealerWin += 1
        print("You bust!")
        print("Your value was", getValue(pDeck))
    elif checkBust(dDeck): # Else, if dealer busts
        playerWin += 1
        print("The dealer bust!")
        print("Their value was", getValue(dDeck))

    elif checkBlackjack(pDeck): # If player has blackjack
        if checkBlackjack(dDeck): #  If dealer also has blackjack
            print("Both had blackjack!")
        else:
            playerWin += 1
            print("Blackjack!")
    elif checkBlackjack(dDeck):
        dealerWin += 1
        print("The dealer had blackjack.")

    elif getValue(dDeck) < 21 and getValue(pDeck) < 21:
        if dValue > pValue:
            dealerWin += 1
            print("The dealer's value is higher than yours.")
            print("Dealer:", getValue(dDeck))
            print("Player:", getValue(pDeck))
        elif getValue(pDeck) > getValue(dDeck):
            playerWin += 1
            print("The player's value is higher than the dealer's!")
            print("Dealer:", getValue(dDeck))
            print("Player:", getValue(pDeck))
        elif getValue(pDeck) == getValue(dDeck):
            print("Both hands were the same, it's a push.")
            print("Dealer:", getValue(dDeck))
            print("Player:", getValue(pDeck))

    return dealerWin, playerWin


def win_decide(dealerWin, playerWin):
    print("=============================================================================================")
    print("\n")
    if betAmount > 0:
        if dealerWin > playerWin:
            print("The dealer has won.")
            print("You lost", betAmount)
        elif playerWin > dealerWin:
            print("Congratulations, you won!")
            print("You earned", betAmount)
    else:
        if dealerWin > playerWin:
            print("The dealer has won.")
        elif playerWin > dealerWin:
            print("Congratulations, you won!")


def game():
    dDeck = dealerFirst()
    print("Dealer:")
    print(dDeck[0], "\n")
    pDeck = player()
    dealerAfter(dDeck)

    if hasSplit:
        counter = 1
        for deck in pDeck:
            print("")
            print("Deck", str(counter) + ":")
            dealerWin, playerWin = deckCompare(deck, dDeck)
            counter += 1

    else:
        dealerWin, playerWin = deckCompare(pDeck, dDeck)

    win_decide(dealerWin, playerWin)
    print("Ending game...")


def bet():
    while True:
        try:
            bet = input("Press enter to go back.\nHow much do you want to bet?\n> ")
            if bet == '':
                main()
                break
            else:
                global betAmount
                betAmount = int(bet)
                global hasBet
                hasBet = True
                game()
            break
        except ValueError:
            print("Please give a number.")


def help():
    print("\n\n\n\n\n\n\n\nHello!")
    print("You are playing blackjack, the goal is to have the total value of your cards higher than the dealer's cards")
    print("without going over 21.")
    ruleNumber = input("What would you like more information about?\n"
                       "  1. Cards and their values\n"
                       "  2. Commands\n"
                       "  3. Rules for the dealer\n"
                       "  4. Back\n"
                       "  > "
                       )
    print("\n\n\n\n\n\n\n")
    if ruleNumber == '1':
        helpCards()
    elif ruleNumber == '2':
        helpCommands()
    elif ruleNumber == '3':
        helpDealerRules()
    else:
        main()


def helpCards():
    print("These are all the values of cards:\n")
    for card, value in cardValues.items():
        print("{:2}  -  {:2}".format(card, value))
    print("\nNote: An Ace can have either a value of 1, or 11. Its value is 11 if the total value of the deck\n"
            "is 21 or lower, also called; a 'soft' deck.\n"
            "If the total value of a deck is over 21, the Ace will have a value of 1.\n"
            "A soft deck with an ace (11) will be visualized as a capital 'A', and a hard deck with an ace will\n"
            "be visualized as an uncapitalized 'a'.")


def helpCommands():
    print("Commands:\n"
          " In blackjack, you can 'hit', 'stand', or 'split'.\n"
          "  - Hitting means that the player will pick another card, and thus"
          " adding more value to their deck.\n"
          "  - Staning means that the player will stop drawing cards and the dealer will unveil their other card.\n"
          "  - Splitting is only possible when your starting hand has two of the same cards. This will split your\n"
          "    deck into two separate decks, however your bet will be doubled (due to having two decks).")


def helpDealerRules():
    print("Dealer's rules:\n"
          " 1. A dealer only shows their first drawn card.\n"
          " 2. A dealer has to keep hitting until the value of their deck is 17 or above."
          )


def main():
    menuOption = input("Select an option:\n"
                       "  1. Start\n"
                       "  2. Help/Rules\n"
                       "  3. Quit\n"
                       "  > "
                       )
    if menuOption == '1':
        print("==================================║ Welcome to blackjack! ║==================================")
        betting = input("Would you like to bet any money? (Yes/No)\n> ")
        betting.lower()
        if betting == "yes":
            global betAmount
            betAmount = bet()
        else:
            game()
    elif menuOption == '2':
        help()
    elif menuOption == '3':
        exit()
    else:
        print("That's not even an option, but I'll just quit then...\n")
        exit()


if __name__ == "__main__":
    main()