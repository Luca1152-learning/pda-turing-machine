from dataclasses import dataclass
from typing import Dict, Tuple


@dataclass
class TM(object):
    # States
    start_state: str
    end_state: str

    transitions: Dict[Tuple[str,], Tuple[str, ...]]
    tape: Dict[int, str]


def read_tm(file_path) -> TM:
    with open(file_path) as file:
        start_state = file.readline().strip()
        end_state = file.readline().strip()

        file.readline()

        transitions_dict = {}
        while line := file.readline():
            transition_list = line.strip().split(",")
            transitions_dict[tuple(transition_list[0:2])] = tuple(transition_list[2:])

        return TM(start_state, end_state, transitions_dict, {})


def is_accepted(tm: TM, word: str):
    tm.tape = {}
    for index, letter in enumerate(word):
        tm.tape[index] = letter

    current_index = 0
    current_state = tm.start_state

    while (True):
        # The tape (which is a dict) is too short to fit in the current index. Place the empty symbol.
        if current_index not in tm.tape:
            tm.tape[current_index] = "_"

        # Accepted condition
        if current_state == tm.end_state:
            return True

        # There are no more moves from the current (state, symbol) pair
        if (current_state, tm.tape[current_index]) not in tm.transitions:
            return False

        new_state, new_letter, direction = tm.transitions[(current_state, tm.tape[current_index])]
        tm.tape[current_index] = new_letter
        if direction == ">":
            current_index += 1
        elif direction == "<":
            current_index -= 1
        current_state = new_state


def main():
    tm = read_tm('input.txt')

    for word in ["0110", "001", "111001100111", "01"]:
        print(f"'{word}' -> {is_accepted(tm, word)}")


if __name__ == '__main__':
    main()
