""" Datele de intrare vor fi:

q0                          <- starea initiala
qAccept                     <- starea finala

q0,0,qRight0,_,>            <- o deplasare: separate prin ',' avem: starea actuala, caracterul de pe banda, noua stare, ce scrie pe banda (_ inseamna caracterul gol/vid), >/</_ este deplasarea)

qRight0,0,qRight0,0,>
qRight0,1,qRight0,1,>
q0,1,qRight1,_,>
qRight1,0,qRight1,0,>
qRight1,1,qRight1,1,>
qRight0,_,qSearch0L,_,<
qSearch0L,0,q1,_,<
qRight1,_,qSearch1L,_,<
qSearch1L,1,q1,_,<
q1,0,qLeft0,_,<
qLeft0,0,qLeft0,0,<
qLeft0,1,qLeft0,1,<
q1,1,qLeft1,_,<
qLeft1,0,qLeft1,0,<
qLeft1,1,qLeft1,1,<
qLeft0,_,qSearch0R,_,>
qSearch0R,0,q0,_,>
qLeft1,_,qSearch1R,_,>
qSearch1R,1,q0,_,>
qSearch0R,1,qReject,1,-
qSearch1R,0,qReject,0,-
qSearch0L,1,qReject,1,-
qSearch1L,0,qReject,0,-
q0,_,qAccept,_,-
q1,_,qAccept,_,-
qSearch0L,_,qAccept,_,-
qSearch0R,_,qAccept,_,-
qSearch1L,_,qAccept,_,-
qSearch1R,_,qAccept,_,-

"""

# TODO iar programul ar trebui sa citeasca datele si dupa oricate cuvinte diferite si sa afiseze
#   daca sunt validate sau nu. Spre exemplu:
"""

Ati citit masina Turing cu configurarea ... (si sa afisati datele citite aici)
Puteti introduce cuvinte pe care sa le testeze MT :).

cuvant: 0110
OK
cuvant: 001
not OK..
cuvant: 11100110111
OK
cuvant: 01
not OK..

"""

# TODO me: make a configuration that uses left side of the tape
# sa impart punctaj inre assignemnturile deja puse?