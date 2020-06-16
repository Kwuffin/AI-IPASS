import blackjackSim as bjs
from random import randint
import numpy as np
import time

cardValues = {
    'A': 11, 'a': 1,
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10
}


#  Create an individual of our population, where the genes are the
#  decisions whether the AI wants to stand, hit, split or double down.
def createIndividual():
    #  0 = stand ; 1 = hit ; 2 = double down ; 3 = split
    genes = [
        #  Hard decks
        np.random.randint(0, 3, (16, 10)),

        #  Soft decks
        np.random.randint(0, 3, (8, 10)),

        #  Splitting decks
        np.random.randint(0, 4, (10, 10))
    ]

    return genes


#  Create a population of N amount of individuals.
def createPopulation(amount):  # TODO: Add comments
    population = []
    for x in range(0, amount):
        population.append(createIndividual())
    return population


#  For each individual, there is a chance for each gene to mutate to the same or a different gene.
def mutate(individual, chance):  # TODO: Finish this
    for table in individual:
        for gene in table:
            randint(0, 100)
            if randint < chance:
                if len(table) == 100:
                    gene = randint(0, 3)
                else:
                    gene = randint(0, 2)
    return individual


"""The fitness is calculated by making each individual play the game X amount of times.
    The amount of money won/lost will be its fitness value, that means that the fitness
    can be a negative value."""


def calcFitness(statusDict, betDict):
    fitnessTemp = {}
    fitnessDict = {}
    counter = 0

    for results in statusDict.values():
        counter += 1
        temp = []

        counter2 = -1
        #  For every win/loss/push for all simulations of an individual.
        for result in results:
            counter2 += 1
            fitness = 0

            #  If the deck wasn't split in simulation
            if type(result) == int:

                #  If player lost
                if result == -1:
                    fitness -= betDict[counter][counter2]
                    temp.append(fitness)

                #  If player won
                elif result == 1:
                    fitness += betDict[counter][counter2]
                    temp.append(fitness)

            #  If the deck was split in simulation
            if type(result) == list:

                #  For each deck in the simulation.
                for splitResult in result:

                    #  If player lost
                    if splitResult == -1:
                        fitness -= betDict[counter][counter2]
                        temp.append(fitness)

                    #  If player won
                    elif splitResult == 1:
                        fitness += betDict[counter][counter2]
                        temp.append(fitness)

        fitnessTemp[counter] = temp.copy()

    indCounter = 1
    for results in fitnessTemp.values():
        fitnessDict[indCounter] = sum(results) / len(results)
        indCounter += 1

    print("fitness Temp:", fitnessTemp)
    print("FitnessDict:", fitnessDict)
    return fitnessDict


def cross(individual1, individual2):  # TODO: Finish this
    pass


def makeDecision(individual, pDeck, dDeck):
    pValue = bjs.value(pDeck)
    dValue = cardValues[dDeck[0]]

    rowCount = -1

    #  If the player gets a deck with two of the same cards.
    if len(pDeck) == 2 and (pDeck[0] == pDeck[1] or ((pDeck[0] == 'a' and pDeck[1] == 'A') or (pDeck[0] == 'A' and pDeck[1] == 'a'))):
        for pValueGuess in range(22, 3, -2):
            rowCount += 1
            columnCount = -1
            for dValueGuess in range(2, 12):
                columnCount += 1
                if dValue == dValueGuess and pValue == pValueGuess:
                    print(individual[2])
                    return individual[2].item(rowCount, columnCount)

    #  If the player gets a soft deck
    elif 'A' in pDeck:
        for pValueGuess in range(20, 12, -1):
            rowCount += 1
            columnCount = -1
            for dValueGuess in range(2, 12):
                columnCount += 1
                if dValue == dValueGuess and pValue == pValueGuess:
                    print(individual[1])
                    return individual[1].item(rowCount, columnCount)

    #  If the player gets a hard deck
    elif pDeck[0] != pDeck[1] or len(pDeck) > 2:
        for pValueGuess in range(20, 4, -1):
            rowCount += 1
            columnCount = -1
            for dValueGuess in range(2, 12):
                columnCount += 1
                if dValue == dValueGuess and pValue == pValueGuess:
                    print(individual[0])
                    return individual[0].item(rowCount, columnCount)


def simulate(individual, betAmount):

    # status = -1 = dealer win ; 0 = push (equal valued decks) ; 1 = player win.
    dDeck = bjs.dealerInitial()  # Give dealer two cards.

    botChoice = 1
    bDeck = []
    bjs.hit(bDeck)

    #  While botChoice = 1 (hit)
    while botChoice == 1:
        #  Give a card
        bjs.hit(bDeck)

        #  Check for soft aces.
        bDeck = bjs.checkAce(bDeck)

        #  Check if bust
        if bjs.bust(bDeck):  # If player busts
            status = -1
            return status, betAmount
        #  Check for 21
        if bjs.checkBlackjack(dDeck):
            break

        print("Bot:", bDeck)
        print("Dealer:", dDeck)
        print(botChoice)
        print(makeDecision(individual, bDeck, dDeck))

        #  Make a new choice with the new deck.
        botChoice = makeDecision(individual, bDeck, dDeck)

    #  If the player has a blackjack
    if bjs.checkBlackjack(bDeck):
        #  If the dealer also has a blackjack.
        if bjs.checkBlackjack(dDeck):
            status = 0
            return status, betAmount
        #  If the dealer doesn't have blackjack.
        else:
            status = 1
            betAmount *= 3
            return status, betAmount

    #  If the dealer has a blackjack
    elif bjs.checkBlackjack(dDeck):
        status = -1
        return status, betAmount

    #  If stand
    if botChoice == 0:
        bjs.dealerAfter(dDeck)
        dw, pw = bjs.compare(bDeck, dDeck)
        if dw == 1 and pw == 0:
            status = -1
            return status, betAmount
        elif dw == 0 and pw == 1:
            status = 1
            return status, betAmount
        elif dw == 0 and pw == 0:
            status = 0
            return status, betAmount

    #  If double down
    elif botChoice == 2:
        #  Double the betting money.
        betAmount *= 2

        #  Give bot a single random card from the deck.
        bDeck = bjs.hit(bDeck)

        #  Check if bust.
        if bjs.bust(bDeck):
            status = -1
            return status, betAmount

        #  Compare to dealer
        dw, pw = bjs.compare(bDeck, dDeck)
        if dw == 1 and pw == 0:
            status = -1
            return status, betAmount
        elif dw == 0 and pw == 1:
            status = 1
            return status, betAmount
        elif dw == 0 and pw == 0:
            status = 0
            return status, betAmount

    #  If split
    elif botChoice == 3:
        #  Create two separate decks.
        bDeck1 = [bDeck[0]]  # Deck 1
        bDeck2 = [bDeck[1]]  # Deck 2

        bDecks = [bDeck1, bDeck2]

        # For each deck, player win, equal or dealer win.
        deckStatus = [0, 0]  # -1 = dealer win ; 0 = push (equal valued decks) ; 1 = player win.

        #  Play with both hands
        deckNumber = -1

        #  Double the bet
        betAmount *= 2

        for deck in bDecks:
            deckNumber += 1
            botChoice = 1

            #  While botChoice = 1 (hit)
            while botChoice == 1:
                #  Give a card
                bjs.hit(deck)

                #  Check for soft aces.
                deck = bjs.checkAce(deck)

                #  Check if bust
                if bjs.bust(deck):
                    deckStatus[deckNumber] = -1
                    break

                #  Check for 21
                if bjs.checkBlackjack(deck):
                    break

                #  Make a new choice with the new deck.
                botChoice = makeDecision(individual, deck, dDeck)

            #  If the player has a blackjack
            if bjs.checkBlackjack(deck):
                #  If the dealer also has a blackjack.
                if bjs.checkBlackjack(dDeck):
                    deckStatus[deckNumber] = 0
                #  If the dealer doesn't have blackjack.
                else:
                    deckStatus[deckNumber] = 1
            #  If the dealer has a blackjack
            elif bjs.checkBlackjack(dDeck):
                deckStatus[deckNumber] = -1

            #  If stand
            if botChoice == 0:
                bjs.dealerAfter(dDeck)
                dw, pw = bjs.compare(deck, dDeck)
                if dw == 1 and pw == 0:
                    deckStatus[deckNumber] = -1
                elif dw == 0 and pw == 1:
                    deckStatus[deckNumber] = 1
                elif dw == 0 and pw == 0:
                    deckStatus[deckNumber] = 0

            #  If double down
            elif botChoice == 2:
                #  Double the betting money.
                betAmount *= 2

                #  Give bot a single random card from the deck.
                deck = bjs.hit(deck)

                #  Check if bust.
                if bjs.bust(deck):
                    deckStatus[deckNumber] = -1

                #  Compare to dealer
                dw, pw = bjs.compare(deck, dDeck)
                if dw == 1 and pw == 0:
                    deckStatus[deckNumber] = -1
                elif dw == 0 and pw == 1:
                    deckStatus[deckNumber] = 1
                elif dw == 0 and pw == 0:
                    deckStatus[deckNumber] = 0
        return deckStatus, betAmount


def main():
    populationAmount = input("Amount of individuals in population: ")
    populationAmount = int(populationAmount)

    simAmount = input("Amount of simulated games per individual: ")
    simAmount = int(simAmount)

    mut_chance = input("Chance for each gene to mutate: ")
    mut_chance = int(mut_chance)

    betAmountInput = input("Bet: ")
    betAmountInput = int(betAmountInput)

    global start_time
    start_time = time.time()

    population = createPopulation(populationAmount)

    #  Simulate x amount of games for every individual in a population and
    #  put all results (win, loss, push) in a dictionary.
    statusDict = {}
    indCount = 0
    betDict = {}
    for individual in population:
        indCount += 1
        statusList = []
        betList = []
        for x in range(0, simAmount):
            print("==========================================")
            print("Simulation", x + 1)
            print("Individual", indCount)
            status, betAmount = simulate(individual, betAmountInput)
            statusList.append(status)
            betList.append(betAmount)

        statusDict[indCount] = statusList.copy()
        betDict[indCount] = betList.copy()

    print("StatusDict:", statusDict)
    print("BetDict:", betDict)

    #  Calculate the fitness for each individual
    calcFitness(statusDict, betDict)


start_time = 0
if __name__ == '__main__':

    main()

    end_time = time.time()
    print("==========================================\nExecution time:\n",
          (end_time - start_time) // 60, "minutes,",
          (end_time - start_time) % 60, "seconds")
