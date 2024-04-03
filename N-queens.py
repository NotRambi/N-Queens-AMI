import random
import sys

### N-QUEENS PROBLEM ###

# numero di regine e grandezza scacchiera
maxLateral = 0
maxRestart = 0
n = 0
A = ""
tf = ""
for attr in sys.argv:
    attr = attr.split('=')
    if attr[0] == 'N':
        n = int(attr[1])
    elif attr[0] == 'A':
        A = attr[1]
        A = A.upper()
    elif attr[0] == "ml":
        maxLateral = int(attr[1])
    elif attr[0] == "mr":
        maxRestart = int(attr[1])
    elif attr[0] == "tf":
        tf = attr[1]
        tf = tf.lower()
    
if n<=3 or not(A == "SD" or A == "HC" or A == "SA") or (A=="SA" and not(tf=="lin" or tf=="exp" or tf=="log")):
    print("\nImplementazione in Python degli algoritmi a miglioramento iterativo per la ricerca della soluzione del problema N-Queens\n"+
          "Per eseguire il programma digitare \"$ python N-queens.py N=int A=str ml=int mr=int tf=str\", dove:\n"+
          "- N = numero di regine e lato della scacchiera (N >= 4)\n"
          "- A = algoritmo da ulitizzare:\n"
          "   + \'SD\' per utilizzare Steepest Descent\n"
          "   + \'HC\' per utilizzare Hill Climbing First Choice\n"
          "   + \'SA\' per utilizzare Simulated Annealing\n"
          "- ml = numero massimo di mosse laterali (facoltativo, default=0)\n"
          "- mr = numero massimo di restart (facoltativo, default=0)\n"
          "- tf = funzione raffreddamento temperatura (obbligatorio con SA):\n"
          "   + \'lin\' lineare\n"
          "   + \'exp\' esponenziale\n"
          "   + \'log\' logaritmica (best)\n"
          "\nsto uscendo...\n\n")
    sys.exit()

#n = 0
#while n<=3:
#    n = int(input("Inserisci il numero di Regine: "))
#
#maxRestart = 100 # successivamente da implementare la possibilità di inserirlo da terminale all'avvio
#maxLateral = 100 # idem

# decisione algoritmo risolutivo
#A = ""
#while not(A == "SD" or A == "HC" or A == "SA"):
#    A = input("Quale algoritmo di ricerca utilizzare? \nDigitare: \n- SD per Steepest Descent \n- HC per First-choice Hill Climbing \n- SA per Simulated Annealing \nDigitare qui: ")
#    A = A.upper()

# creazione board
board = []
def PopulateBoard():
    board.clear()
    for i in range(0,n):
        r = random.randint(0,n-1)
        board.append(r)
PopulateBoard()

# stampa board di partenza generata randomicamente
print("\n\nScacchiera iniziale generata randomicamente\n")
for i in range(0,n):
    row = []
    for j in board:
        if j == i:
            row.append('1')
        else:
            row.append('0')
    print(row)

# funzione che trova il numero di scacchi tra coppie di regine
def CheckCounterFinder(board):
    CheckCounter = 0
    for i in range(0,n): #regina 1
        for j in range(0,n): # regina 2
            if i != j :
                if board[i] == board[j]: # scacco orizzontale
                    CheckCounter+=1
                elif i+board[i] == j+board[j]:  # scacco diagonale primaria 
                    CheckCounter+=1     
                elif i-board[i] == j-board[j]: # scacco diagonale secondaria
                    CheckCounter+=1           
    CheckCounter/=2
    return CheckCounter

def SteepestDescent():
    countRestart = 0
    countLateral = 0
    bestbestCheck = n
    BestBestBoard = board.copy()
    NewBoard = board.copy()
    BestBoard = [] # contenitore di stati migliorativi
    ActualBestBoard = board.copy()
    ActualBestCheck = CheckCounterFinder(ActualBestBoard)
    bestCheck = CheckCounterFinder(NewBoard)
    bestTry = bestCheck
    while True:
        flagLateral = False
        flagMove = False
        BestBoard.clear()
        # ricerca stati migliorativi
        for i in range(0,n):
            for j in range(0,n):
                if NewBoard[i] == j:
                    continue
                TryBoard = NewBoard.copy()
                TryBoard[i] = j
                TryCheck = CheckCounterFinder(TryBoard)
                #print("tentativo:",TryBoard,TryCheck)
                if TryCheck == 0:
                    return TryBoard
                if TryCheck < bestCheck: # mossa migliorativa
                    if TryCheck == bestTry:
                        flagMove = True
                        BestBoard.append(TryBoard)
                        #print("aggiunto in best")
                    elif TryCheck < bestTry:
                        flagLateral = True
                        BestBoard.clear()
                        flagMove = True
                        BestBoard.append(TryBoard)
                        #print("aggiunto in best")
                        bestTry = TryCheck
                elif TryCheck == bestCheck and flagLateral == False:
                    if TryCheck == bestTry:
                        flagMove = True
                        BestBoard.append(TryBoard)
                        #print("aggiunto in best")
        if flagLateral == False: # non sono presenti mosse migliorative
            countLateral+=1
            #print(countLateral)
        else:
            countLateral=0
        if countLateral == maxLateral or flagMove==False: # raggiungimento numero massimo di mosse laterali consentito
            if ActualBestCheck<bestbestCheck:             # o non ci sono mosse disponibili
                BestBestBoard=ActualBestBoard.copy()
                bestbestCheck=ActualBestCheck
                #print("nuovo best:",BestBestBoard,bestbestCheck)
            if countRestart < maxRestart:
                countRestart+=1
                PopulateBoard()
                NewBoard = board.copy()
                ActualBestBoard = board.copy()
                ActualBestCheck = CheckCounterFinder(ActualBestBoard)
                bestCheck = CheckCounterFinder(NewBoard)
                bestTry = bestCheck
                #print("RESTART")
                continue
            return BestBestBoard
        else:
            # scelta random prossimo stato
            ActualBestBoard = random.choice(BestBoard).copy()
            ActualBestCheck = CheckCounterFinder(ActualBestBoard)
            #print("choose:",ActualBestBoard,ActualBestCheck)
            NewBoard = ActualBestBoard.copy()

            
def HillClimbing():
    countRestart = 0
    bestbestCheck = n*(n-1)
    NewBoard = board.copy()
    bestBoard = board.copy()
    bestCheck = CheckCounterFinder(bestBoard)
    allTry = []
    for x1 in range(0,n):
        for x2 in range(0,n):
            allTry.append([x1,x2])
    alreadyTry = []
    cont = 0
    while True:
        canTry = []
        for elem in allTry:
            if elem not in alreadyTry:
                canTry.append(elem)
        if len(canTry) > 0:
            newTry = random.choice(canTry)
            alreadyTry.append(newTry)
            i = newTry[0]
            j = newTry[1]
            if j == NewBoard[i]:
                continue
            NewBoard = bestBoard.copy()
            NewBoard[i] = j
            newCheck = CheckCounterFinder(NewBoard)
            #print("try: ",NewBoard,newCheck)
            if newCheck == 0:
                return NewBoard # ottimo globale
            if newCheck < bestCheck:
                #print("choose: ",NewBoard,newCheck)
                bestCheck = newCheck
                bestBoard = NewBoard.copy()
                cont = 0
                alreadyTry.clear()
                continue
        cont+=1
        if cont >= n*(n-1):
            if bestCheck < bestbestCheck:
                bestbestBoard = bestBoard.copy()
                bestbestCheck = bestCheck
            if countRestart < maxRestart:
                countRestart+=1
                #print("best of restart n.",countRestart,bestBoard,bestCheck)
                cont = 0
                PopulateBoard()
                NewBoard = board.copy()
                bestBoard = board.copy()
                bestCheck = CheckCounterFinder(bestBoard)
                #print("newBoard:",bestBoard,bestCheck)
                alreadyTry.clear()
                continue       
            return bestbestBoard  # ottimo locale

def Raffreddamento(t,T):
    if tf == "log":
        T = T * (1/t) # log
    elif tf == "exp":
        T = T - t #exp
    elif tf == "lin":
        T = 1000 - t #lin
    #print("time: ",t,"Temp: ",T)
    return T

def SimulatedAnnealing():
    countRestart = 0
    t = 0
    T = 1000
    e = 2.718281828459045
    bestbestCheck = n*(n-1)
    NewBoard = board.copy()
    bestBoard = board.copy()
    bestCheck = CheckCounterFinder(bestBoard)
    allTry = []
    for x1 in range(0,n):
        for x2 in range(0,n):
            allTry.append([x1,x2])
    alreadyTry = []
    while True:
        t += 1
        T = Raffreddamento(t,T)
        if T <= 0:
            if bestCheck < bestbestCheck:
                bestbestBoard = bestBoard.copy()
                bestbestCheck = bestCheck
            if countRestart < maxRestart:
                countRestart+=1
                PopulateBoard()
                t = 0
                NewBoard = board.copy()
                bestBoard = board.copy()
                bestCheck = CheckCounterFinder(bestBoard)
                alreadyTry.clear()
                continue
            return bestbestBoard
        canTry = []
        for elem in allTry:
            if elem not in alreadyTry:
                canTry.append(elem)
        if len(canTry) == 0:
            continue
        newTry = random.choice(canTry)
        alreadyTry.append(newTry)
        i = newTry[0]
        j = newTry[1]
        if j == NewBoard[i]:
            continue
        NewBoard = bestBoard.copy()
        NewBoard[i] = j
        newCheck = CheckCounterFinder(NewBoard)
        if newCheck == 0:
            return NewBoard # ottimo globale
        if newCheck < bestCheck:
            bestCheck = newCheck
            bestBoard = NewBoard.copy()
            alreadyTry.clear()
            continue
        else:
            dE = abs(newCheck-bestCheck)
            prob = e**(-dE/T)
            #print("Probability: ",prob)
            if random.random() < prob:
                bestCheck = newCheck
                bestBoard = NewBoard.copy()
                alreadyTry.clear()
                continue


def NQueenResolver():
    if A == "SD":
        Sol = SteepestDescent()
    elif A == "HC":
        Sol = HillClimbing()
    elif A == "SA":
        Sol = SimulatedAnnealing()
    for i in range(0,n):
        row = []
        for j in Sol:
            if j == i:
                row.append('1')
            else:
                row.append('0')
        print(row)
    print("\n",Sol,CheckCounterFinder(Sol))
    
print("\n",board,CheckCounterFinder(board))
print("\n\n")
NQueenResolver()
print()