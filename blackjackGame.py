import blackjackSim as bjs
import geneticAlgorithm as ga
import numpy as np
from random import randint
from time import sleep

cards = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
cardValues = {
    'A': 11, 'a': 1,
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10
}
cardCounter = {}
"""There are 8 decks in one game of blackjack, and four cards with the same value in one deck."""
for card in cards:
    cardCounter[card] = 32


# Import the bot's strategy
def importBot():
    try:
        data = np.load('highestIndividual.npz')
    except FileNotFoundError:
        print("Could not get an individual; file not found\n"
              "Try running the algorithm (again).")
        exit()

    return [data[key] for key in data]


def drawCard(deck):
    available = True
    while available:
        drawn = cards[randint(0, 12)]
        if cardCounter[card] <= 0:
            continue
        else:
            available = False
    deck.append(drawn)


def getDecision(pDeck):
    #  Deck with two of the same cards
    answer = True
    while answer:
        if len(pDeck) == 2 and (
                pDeck[0] == pDeck[1] or ((pDeck[0] == 'a' and pDeck[1] == 'A') or (pDeck[0] == 'A' and pDeck[1] == 'a'))):
            pDecision = input("Would you like to hit, stand, double down or split?\n> ")

        #  If hard deck and first turn
        elif len(pDeck) == 2:
            pDecision = input("Would you like to hit, stand or double down?\n> ")

        #  If hard deck and not first turn
        elif len(pDeck) != 2:
            pDecision = input("Would you like to hit or stand?\n> ")

        pDecision.lower()

        if pDecision == "hit" or pDecision == "stand" or pDecision == "double down" or "split":
            answer = False

        else:
            print("Please choose from: 'hit', 'stand', 'split', or 'double down' if available.")
    print("====================================================")
    return pDecision


def player(bet, dDeck):
    print("====================================================")
    print("Dealer:", dDeck[0], "\n")

    pDeck = []
    pDecision = "hit"
    drawCard(pDeck)

    while pDecision == "hit":
        drawCard(pDeck)

        #  Check for aces
        pDeck = bjs.checkAce(pDeck)

        if bjs.checkBlackjack(pDeck):
            bet *= 3
            return pDeck, bet

        print("You:", end=' ')
        for card in pDeck:
            print(card, end=' ')
        print("")
        print("Value:", bjs.value(pDeck), "\n")

        pDecision = getDecision(pDeck)

        if pDecision == "double down":
            bet *= 2
            drawCard(pDeck)
            pDecision = "stand"

        if pDecision == "stand" or bjs.bust(pDeck):
            return pDeck, bet

        elif pDecision == "split":
            bet *= 2

            pDeck1 = [pDeck[0]]
            pDeck2 = [pDeck[1]]
            pDecks = [pDeck1, pDeck2]

            deckCounter = -1
            for deck in pDecks:
                deckCounter += 1

                pDecision = "hit"

                while pDecision == "hit":
                    drawCard(deck)

                    deck = bjs.checkAce(deck)

                    print("You:", end=' ')
                    for card in deck:
                        print(card, end=' ')
                    print("")
                    print("Value:", bjs.value(deck))

                    pDecision = getDecision(deck)

                    if pDecision == "double down":
                        bet *= 2
                        drawCard(pDeck)
                        pDecision = "stand"

                    if pDecision == "stand" or bjs.bust(pDeck):
                        break
            return pDecks, bet


def botPlay(botStrat, dDeck):
    print("====================================================")
    print("Dealer:", dDeck[0], "\n")

    botChoice = "hit"
    bDeck = []
    drawCard(bDeck)

    while botChoice == "hit":
        drawCard(bDeck)

        bDeck = bjs.checkAce(bDeck)

        if bjs.checkBlackjack(bDeck):
            return bDeck

        print("Bot:", end=' ')
        for card in bDeck:
            print(card, end=' ')
        print("")
        print("Value:", bjs.value(bDeck), "\n")

        botDecision = ga.makeDecision(botStrat, bDeck, dDeck)

        if botDecision == 0:
            botChoice = "stand"
            print("Bot stands")

        elif botDecision == 1:
            botDecision = "hit"
            print("Bot hits")

        elif botDecision == 2:
            botDecision = "double down"
            print("Bot doubles down")

        elif botDecision == 3:
            botDecision = "split"
            print("Bot splits")

        if botChoice == "double down":
            drawCard(bDeck)
            botDecision = "stand"

        if botChoice == "stand" or bjs.bust(bDeck):
            return bDeck

        elif botChoice == "split":
            bDeck1 = [bDeck[0]]
            bDeck2 = [bDeck[1]]
            bDecks = [bDeck1, bDeck2]

            deckCounter = -1
            for deck in bDecks:
                deckCounter += 1

                botDecision = "hit"

                while botDecision == "hit":
                    drawCard(deck)

                    deck = bjs.checkAce(deck)

                    print("Bot:", end=' ')
                    for card in deck:
                        print(card, end=' ')
                    print("")
                    print("Value:", bjs.value(deck), "\n")

                    botDecision = ga.makeDecision(botStrat, deck, dDeck)

                    if botDecision == 0:
                        botChoice = "stand"
                        print("Bot stands")

                    elif botDecision == 1:
                        botDecision = "hit"
                        print("Bot hits")

                    elif botDecision == 2:
                        botDecision = "double down"
                        print("Bot doubles down")

                    elif botDecision == 3:
                        botDecision = "split"
                        print("Bot splits")

                    if botChoice == "double down":
                        drawCard(bDeck)
                        botDecision = "stand"

                    if botChoice == "stand" or bjs.bust(bDeck):
                        break
            return bDecks


def dealerAfter(deck):
    sleep(1.5)
    print("Dealer:", end=' ')
    for card in deck:
        print(card, end=' ')
    print("")
    print("Value:", bjs.value(deck), "\n")
    sleep(1.5)
    while bjs.value(deck) < 17:
        drawCard(deck)
        print("Dealer drew", deck[-1])
        print("Value:", bjs.value(deck), "\n")


def processResult(status, betAfterGame):
    if type(status) == list:

        deckCounter = 0
        for splitStatus in status:
            deckCounter += 1
            if splitStatus == -1:
                print(f"Deck {deckCounter}:\n"
                      f"You lost €{betAfterGame} :(")

            elif splitStatus == 0:
                print(f"Deck {deckCounter}:\n"
                      f"Your deck and the dealer's were equal. You received your bet of {betAfterGame} back.")

            elif splitStatus == 1:
                print(f"Deck {deckCounter}:\n"
                      f"Congratulations! You won €{betAfterGame}.")

    elif type(status) == int:
        if status == -1:
            print(f"You lost €{betAfterGame}, better luck next time!")

        elif status == 0:
            print(f"Your deck and the dealer's were equal. You received your bet of {betAfterGame} back.")

        elif status == 1:
            print(f"Congratulations! You won €{betAfterGame}.")


def evalDecks(deckDict, dDeck, betDict, bDeck):
    player = 0

    dealerAfter(dDeck)

    for deck in deckDict.values():
        if type(deck[0]) == str:
            player += 1
            print("====================================================")
            print(f"Player {player}:")

            dw, pw = bjs.compare(deck, dDeck)  # dw = dealer win ; pw = player win
            if dw == 1 and pw == 0:
                print("The dealer won, better luck next time.\n"
                      f"You lost €{betDict[player]}.")
            elif dw == 0 and pw == 0:
                print("You and the dealer had the same value\n"
                      f"You received your bet of €{betDict[player]} back.")
            elif dw == 0 and pw == 1:
                print(f"Congratulations! You won €{betDict[player]}")

        elif type(deck[0]) == list:
            player += 1
            for splitDeck in deck:
                print(f"Player {player}:")

                dw, pw = bjs.compare(splitDeck, dDeck)  # dw = dealer win ; pw = player win
                if dw == 1 and pw == 0:
                    print("The dealer won, better luck next time.\n"
                          f"You lost €{betDict[player]}.")
                elif dw == 0 and pw == 0:
                    print("You and the dealer had the same value\n"
                          f"You received your bet of €{betDict[player]} back.")
                elif dw == 0 and pw == 1:
                    print(f"Congratulations! You won €{betDict[player]}")

    if type(bDeck[0]) == str:
        player += 1
        print("====================================================")
        print("Bot:")

        dw, pw = bjs.compare(bDeck, dDeck)  # dw = dealer win ; pw = player win
        if dw == 1 and pw == 0:
            print("The dealer won, better luck next time.")
        elif dw == 0 and pw == 0:
            print("You and the dealer had the same value")
        elif dw == 0 and pw == 1:
            print(f"Congratulations, You won!")

    elif type(bDeck[0]) == list:
        player += 1
        for splitDeck in bDeck:
            print("Bot:")

            dw, pw = bjs.compare(splitDeck, dDeck)  # dw = dealer win ; pw = player win
            if dw == 1 and pw == 0:
                print("The dealer won, better luck next time.")
            elif dw == 0 and pw == 0:
                print("You and the dealer had the same value.")
            elif dw == 0 and pw == 1:
                print(f"Congratulations, you won!")


def main():
    playerCount = int(input("How many players will be playing?\n> "))

    initialBets = {}
    for play in range(playerCount):
        betAmount = int(input(f"Player {play + 1}, what is your bet?\n> "))
        initialBets[play] = betAmount

    dDeck = bjs.dealerInitial()  # Dealer cards

    playerDecks = {}
    betsAfter = {}

    playerCounter = 0
    for bet in initialBets.values():
        playerCounter += 1
        print(f"\n\nPlayer {playerCounter}:")
        deck, betAfter = player(bet, dDeck)

        playerDecks[playerCounter] = deck
        betsAfter[playerCounter] = betAfter

    botStrat = importBot()

    bDeck = botPlay(botStrat, dDeck)

    print(bDeck)

    evalDecks(playerDecks, dDeck, betsAfter, bDeck)


if __name__ == '__main__':
    main()
