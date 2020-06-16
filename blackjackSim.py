import random

cards = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
cardValues = {
    'A': 11, 'a': 1,
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10
    }


#  Add a card to the deck.
def hit(deck):
    randCard = random.randint(0, 12)
    deck.append(cards[randCard])
    return deck


#  Split the deck into two separate decks.
def split(deck):
    deck1 = [deck[0]]
    deck2 = [deck[1]]
    return deck1, deck2


#  Initialize the bot's deck.
def bot():
    pDeck = []
    hit(pDeck)
    hit(pDeck)
    return pDeck


#  Initialize the dealer's deck.
def dealerInitial():
    dDeck = []
    hit(dDeck)
    hit(dDeck)
    return dDeck


#  Return value of deck.
def value(deck):
    value = 0
    for card in deck:
        value += cardValues[card]
    return value


def dealerAfter(deck):
    while value(deck) < 17:
        deck = hit(deck)


def checkAce(deck):
    for card in deck:
        deckValue = value(deck)
        if cardValues[card] == 11 and deckValue > 21:
            acePos = deck.index("A")
            deck[acePos] = "a"
    return deck


def checkBlackjack(deck):
    if value(deck) == 21:
        return True
    return False


def bust(deck):
    if value(deck) > 21:
        return True
    return False


def compare(pDeck, dDeck):
    dealerWin = 0
    playerWin = 0
    pValue = value(pDeck)
    dValue = value(dDeck)

    if bust(pDeck):
        dealerWin += 1
        return dealerWin, playerWin
    elif bust(dDeck):
        playerWin += 1
        return dealerWin, playerWin

    elif checkBlackjack(pDeck):
        if checkBlackjack(dDeck):
            return dealerWin, playerWin
        else:
            playerWin += 1
            return dealerWin, playerWin
    elif checkBlackjack(dDeck):
        dealerWin += 1

    elif dValue < 21 and pValue < 21:
        if dValue > pValue:
            dealerWin += 1
            return dealerWin, playerWin
        elif pValue > dValue:
            playerWin += 1
            return dealerWin, playerWin
        elif pValue == dValue:
            return dealerWin, playerWin
    return dealerWin, playerWin
