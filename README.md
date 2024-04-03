# N-Queens-AMI
Algoritmi a Miglioramento Iterativo per la risoluzione del problema delle N Regine, realizzato per il corso di Intelligenza Artificiale presso l'Università Sapienza di Roma

Per eseguire correttamente il programma usare il comando `python N-Queens.py` per Unix o `py N-Queens.py` per Windows, aggiungendo i seguenti parametri:
- N = numero di regine e lato della scacchiera (con N >= 4)
- A = algoritmo da ulitizzare:
  + \'SD\' per utilizzare Steepest Descent
  + \'HC\' per utilizzare Hill Climbing First Choice
  + \'SA\' per utilizzare Simulated Annealing
- ml = numero massimo di mosse laterali (facoltativo, default=0)
- mr = numero massimo di restart (facoltativo, default=0)
- tf = funzione raffreddamento temperatura (obbligatorio con SA):
  + \'lin\' lineare
  + \'exp\' esponenziale
  + \'log\' logaritmica (best)

seguendo ad esempio il formato: `N-Queens.py N=8 A=sa tf=log mr=10`
