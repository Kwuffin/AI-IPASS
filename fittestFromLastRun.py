import numpy as np
from tkinter import *


def createWindow(data):
    root = Tk()

    label = Label(root, text="View strategy for", font=("Helvetica", 16)).pack()
    hard = Button(root, text="Hard decks", font=("Helvetica", 14), width=20, height=2, command=lambda: hardDeck(data)).pack()
    soft = Button(root, text="Soft decks", font=("Helvetica", 14), width=20, height=2, command=lambda: softDeck(data)).pack()
    split = Button(root, text="Split decks", font=("Helvetica", 14), width=20, height=2, command=lambda: splitDeck(data)).pack()

    root.geometry('500x500')
    root.title('Menu')
    root.mainloop()


def hardDeck(data):
    hard = Tk()

    for row in range(2, 12):
        if row == 11:
            label = Label(hard, text="A    ")
        else:
            label = Label(hard, text=f"{row}    ")
        label.grid(row=0, column=row-1)

    counter = 0
    for column in range(20, 4, -1):
        counter += 1
        label = Label(hard, text=column)
        label.grid(row=counter, column=0)

    hardData(hard, data[0].tolist())

    hard.title("Hard decks")
    hard.geometry('280x380')


def softDeck(data):
    soft = Tk()

    for row in range(2, 12):
        if row == 11:
            label = Label(soft, text="A    ")
        else:
            label = Label(soft, text=f"{row}    ")
        label.grid(row=0, column=row-1)

    counter = 0
    for column in range(9, 1, -1):
        counter += 1
        label = Label(soft, text=f"A-{column}")
        label.grid(row=counter, column=0)

    softData(soft, data[1].tolist())

    soft.title("Soft decks")
    soft.geometry('300x220')


def splitDeck(data):
    split = Tk()

    for row in range(2, 12):
        if row == 11:
            label = Label(split, text="A    ")
        else:
            label = Label(split, text=f"{row}    ")
        label.grid(row=0, column=row-1)

    counter = 0
    for column in range(11, 1, -1):
        counter += 1
        if column == 11:
            label = Label(split, text=f"A-A")
        else:
            label = Label(split, text=f"{column}-{column}")
        label.grid(row=counter, column=0)

    splitData(split, data[2].tolist())

    split.title("Split decks")
    split.geometry('300x250')


def hardData(master, data):
    rowNr = 0
    for row in data:
        rowNr += 1
        geneNr = 0
        for gene in row:
            geneNr += 1
            if gene == 0:
                label = Label(master, text="S")
                label['bg'] = 'red2'
            elif gene == 1:
                label = Label(master, text="H")
                label['bg'] = 'green2'
            elif gene == 2:
                label = Label(master, text="D")
                label['bg'] = 'deep sky blue'

            label.grid(row=rowNr, column=geneNr)


def softData(master, data):
    rowNr = 0
    for row in data:
        rowNr += 1
        geneNr = 0
        for gene in row:
            geneNr += 1
            if gene == 0:
                label = Label(master, text="S")
                label['bg'] = 'red2'
            elif gene == 1:
                label = Label(master, text="H")
                label['bg'] = 'green2'
            elif gene == 2:
                label = Label(master, text="D")
                label['bg'] = 'deep sky blue'

            label.grid(row=rowNr, column=geneNr)


def splitData(master, data):
    rowNr = 0
    for row in data:
        rowNr += 1
        geneNr = 0
        for gene in row:
            geneNr += 1
            if gene == 0:
                label = Label(master, text="S")
                label['bg'] = 'red2'
            elif gene == 1:
                label = Label(master, text="H")
                label['bg'] = 'green2'
            elif gene == 2:
                label = Label(master, text="D")
                label['bg'] = 'deep sky blue'
            elif gene == 3:
                label = Label(master, text="P")
                label['bg'] = 'yellow'

            label.grid(row=rowNr, column=geneNr)


def main():
    try:
        data = np.load('highestIndividual.npz')
    except FileNotFoundError:
        print("Could not get an individual; file not found\n"
              "Try running the algorithm (again).")
        exit()

    lst = [data[key] for key in data]

    print("The fittest individual from your last run was:\n", lst)

    createWindow(lst)


if __name__ == '__main__':
    main()
