from dataclasses import dataclass
import queue

"""
PDA

Cum arata fisierul:

#           <- caracterul pt lambda
S           <- starea initiala
A B C       <- starile
C           <- starile finale
a           <- alfabetul
ASZ         <- alfabetul stivei
Z           <- caracterul de la baza stivei

            <- tranzitiile:
S A a Z/ASZ    <-   Stare de unde se deplaseaza, noua stare, litera citita din cuvant, cum modifica stiva
A A a A/AA    <-   Stare de unde se deplaseaza, noua stare, litera citita din cuvant, cum modifica stiva

A B # A/A    <-   Stare de unde se deplaseaza, noua stare, litera citita din cuvant, cum modifica stiva
B B # AAA/A
B C # SZ/Z



<- si vom valida doar cand si stiva ramane goala
<- cu stare finala
<- cu ambele


1. Cititi PDA si salvati-l intr-o structura utila
    (spre exemplu folosim @dataclass cu typing "ca lumea")
2.


"""
# TODO Ce tip de dictionar ne-ar fi util ca sa verificam daca putem trece de la o stare la alta stare? Stim stiva si litera pe care o citeste PDA-ul.

# Deci facem ca la DFA, avand doua stari poate exista o singura tranzitie cu o anume litera citita
# adica (stare1, stare2, litera) formeaza o cheie, iar valoarea este un tuplu de cuvinte din alfabetul stivei, adica ce sa citeasca si ce sa scrie in stive

"""
{
    ('A','A,'a') : ("A", "A"),
    ('B','C,'#') : ("SZ", "Z"),
    ...
}
"""

from typing import List, Dict, Tuple


@dataclass
class PDA(object):
    LAMBDA: str

    start_state: str
    states: List[str]
    end_states: List[str]

    alpha: str
    stack_alpha: str

    """
    {
        ('A','A','a') : ("A", "AA"),
        ('B','C,'#') : ("Z", "Z"),
        ...
    }
    """
    d: Dict[Tuple[str, ...], Tuple[str, ...]]

    STACK_BASE: str


def read_PDA(infile):
    with open(infile) as file:
        LAMBDA = file.readline().strip()

        start = file.readline().strip()
        states = file.readline().strip().split(' ')
        end_states = file.readline().strip().split(' ')

        alpha = file.readline().strip()
        stack_alpha = file.readline().strip()

        STACK_BASE = file.readline().strip()

        d = dict()
        # while line := file.readline().strip():
        for line in file.readlines():
            line = line.strip()

            components = line.split(' ')
            if len(components) != 4:
                continue
            key, value = tuple(components[: 3]), tuple(components[3].split('/'))
            d[key] = value

    return PDA(LAMBDA, start, states, end_states, alpha, stack_alpha, d, STACK_BASE)


@dataclass
class Snapshot(object):
    word: str
    state: str
    stack: List[str]


def can_read_stack_top(stack: List[str], to_read: str):
    # TODO modificam sa "faca peek" la un singur caracter
    stack_cpy = [item for item in stack]
    for letter in to_read:
        stack_top = stack_cpy.pop(-1)
        if stack_top != letter:
            return False
    return True


def read_stack_top(stack: List[str], to_read: str) -> List[str]:
    # TODO modificam sa citeasca un singur caracter
    stack_cpy = [item for item in stack]
    for letter in to_read:
        stack_top = stack_cpy.pop(-1)
        if stack_top != letter:
            return None
    return stack_cpy

# TODO  sa gasiti o modalitate de tratare diferita a tipurilor de validare (doar stare finala / stare finala si stiva goala)

def is_accepted(pda: PDA, word: str):
    stare_finala, stiva_vida = False, False

    # un snapshot are cuvantul (ce a ramasa de citit), are starea curenta, si are si o copie a stivei

    # stack = []
    queue = [
        # la inceput, avem tot cuvantul de input, suntem in starea initiala si stiva contine doar caracterul de la baza stivei
        Snapshot(word, pda.start_state, [pda.STACK_BASE])  # Descriere instantanee
    ]

    while len(queue) > 0:

        top_snap = queue.pop()
        # TODO am ajuns in stare finala?
        if len(top_snap.word) == 0:
            # validarea 1:
            # am ajuns intr-o stare finala dupa ce am citit intreg cuvantul?
            if top_snap.state in pda.end_states:
                print('Validare 1 (stare finala, stiva nu neaparat goala)')
                stare_finala = True
                # verificam daca stiva a e goala
                if len(top_snap.stack) == 1 and top_snap.stack[0] == pda.STACK_BASE:  # doar 'Z'
                    stiva_vida = True
                    # PUTEM intrerupe inclusiv tot algoritmul, deoarece mai bine de atata nu exista :)
                    return True, True

        # vom cauta deplasari posibile (adica.. avand urmatoare litera, sau lambda, cum se poate modifica PDA-ul?)
        state1 = top_snap.state  # 'S' la primul pas

        if len(top_snap.word) == 0:  # chiar si daca nu mai ai litere, poate mai exista lambda-tranzitii, unde cuvantul este '#'
            letter = pda.LAMBDA  # '#'
        else:
            letter = top_snap.word[0]

        stack = top_snap.stack  # ['Z'] la primul pas


        next_snaps = []

        for state2 in pda.states:  # cautam noi in d o cheie (state1, ?state2?, letter)

            d_key = (state1, state2, letter)
            # cautam si lambda tranzitii
            d_lambda_key = (state1, state2, pda.LAMBDA)

            # pt chei care nu contin lambda
            if d_key != d_lambda_key and pda.d.__contains__(d_key):
                # valoarea cheiei spune cum trebuie sa modificam stiva.
                # TODO to_read va trebui sa fie in topul stivei ca sa ne putem deplasa
                #   iar in mod pozitiv, vom inlocui topul stivei cu to_write
                to_read, to_write = pda.d[d_key]
                # check if we can remove the specified letters ('A')
                if can_read_stack_top(stack, to_read):
                    new_stack = read_stack_top(stack, to_read)  # stiva fara 'A'
                    # for letter in to_write[::-1]:
                    for letter in reversed(to_write):
                        new_stack.append(letter)

                    next_snaps.append(
                        Snapshot(top_snap.word[1:], state2, new_stack)  # in order: 'a', 'A'
                    )

            if pda.d.__contains__(d_lambda_key):
                # valoarea cheiei spune cum trebuie sa modificam stiva.
                # to_read ar trebui sa gasim in elementele dinspre varf,
                #   iar in mod pozitiv, vom inlocui cu to_write
                to_read, to_write = pda.d[d_lambda_key]
                # check if we can remove the specified letters ('A')
                if can_read_stack_top(stack, to_read):
                    new_stack = read_stack_top(stack, to_read)  # stiva fara 'A'
                    # for letter in to_write[::-1]:
                    for letter in reversed(to_write):
                        new_stack.append(letter)

                    next_snaps.append(
                        Snapshot(top_snap.word, state2, new_stack)  # in order: 'a', 'A'
                    )

        print()
        for snap in next_snaps:
            queue.append(snap)
            print(top_snap, '->', snap)
        print()

        # TODO test if the conditions for accepting/rejecting the word are met

    return stare_finala, stiva_vida

"""
TODO pt  +4p
1. citirea de pe stiva este implementata ca si cum citeste mai multe caractere la un pas. Trebuie sa faceti cu citirea unui singur caracter.
2. sa gasiti o alta modalitate de tratare diferita a tipurilor de validare (doar stare finala / stare finala si stiva goala)
"""

def main():
    pda = read_PDA('input.txt')

    print(pda)

    """
    
    """
    for word in ['aa', 'a', 'aaaaaaaaaa', '']:  # TODO treat empty str ''
        print(word,  is_accepted(pda, word))


if __name__ == '__main__':
    main()
