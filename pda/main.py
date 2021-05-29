from dataclasses import dataclass
from typing import List, Dict, Tuple


@dataclass
class PDA(object):
    # Chars
    LAMBDA: str
    STACK_BASE: str

    # States
    start_state: str
    states: List[str]
    end_states: List[str]

    # Alphabets
    alpha: str
    stack_alpha: str

    # Dictionary with states + stack updates
    d: Dict[Tuple[str, ...], Tuple[str, ...]]


def read_pda(infile):
    with open(infile) as file:
        # Read the values
        LAMBDA = file.readline().strip()

        start = file.readline().strip()
        states = file.readline().strip().split(' ')
        end_states = file.readline().strip().split(' ')

        alpha = file.readline().strip()
        stack_alpha = file.readline().strip()

        STACK_BASE = file.readline().strip()

        # Create the dictionary
        d = dict()
        for line in file.readlines():
            line = line.strip()

            components = line.split(' ')
            if len(components) != 4:
                continue
            key, value = tuple(components[: 3]), tuple(components[3].split('/'))
            d[key] = value

    return PDA(LAMBDA, STACK_BASE, start, states, end_states, alpha, stack_alpha, d)


@dataclass
class Snapshot(object):
    word: str
    state: str
    stack: List[str]


def can_read_stack_top(stack: List[str], to_read: str):
    stack_cpy = [item for item in stack]

    stack_top = stack_cpy.pop(-1)

    # The symbol is at the stack's top
    if stack_top != to_read:
        return False

    # The symbol is at the stack's top
    return True


def read_stack_top(stack: List[str], to_read: str) -> List[str]:
    stack_cpy = [item for item in stack]

    stack_top = stack_cpy.pop(-1)
    if stack_top != to_read:
        return None

    return stack_cpy


def is_accepted(pda: PDA, word: str, check_final_state, check_empty_stack):
    reached_final_state, reached_empty_stack = False, False

    queue = [
        Snapshot(word, pda.start_state, [pda.STACK_BASE])
    ]

    while len(queue) > 0:
        top_snap = queue.pop()

        # The word is empty
        if len(top_snap.word) == 0:
            # Check 1: Is the current state final?
            if top_snap.state in pda.end_states:
                reached_final_state = True

            # Check 2: Is the stack empty? (Is 'Z' the only element in the stack?)
            if len(top_snap.stack) == 1 and top_snap.stack[0] == pda.STACK_BASE:
                reached_empty_stack = True

            if (reached_final_state >= check_final_state and reached_empty_stack >= check_empty_stack):
                return True

        # Search for possible movements for the top snapshot
        state1 = top_snap.state  # Would be 'S' at the first step

        # Get the current letter
        if len(top_snap.word) == 0:
            # Even if the word doesn't have any more letters, maybe there are λ-transitions from the current state
            letter = pda.LAMBDA  # '#'
        else:
            # The word is not empty, so use its first letter (the word is read from left to right)
            letter = top_snap.word[0]

        # Get the current stack
        stack = top_snap.stack  # ['Z'] initially

        # Will contain future snapshots. Possibly more than one, due to PDAs' nondeterministic nature
        next_snaps = []

        for state2 in pda.states:
            # Keys to search for
            d_key = (state1, state2, letter)
            d_lambda_key = (state1, state2, pda.LAMBDA)

            # If the d_key and d_lambda_key are not the same (as to not check them twice)
            if d_key != d_lambda_key and pda.d.__contains__(d_key):
                to_read, to_write = pda.d[d_key]

                # check if we can remove the specified letters ('A')
                if can_read_stack_top(stack, to_read):
                    new_stack = read_stack_top(stack, to_read)  # stiva fara 'A'
                    for letter in reversed(to_write):
                        new_stack.append(letter)

                    next_snaps.append(
                        Snapshot(top_snap.word[1:], state2, new_stack)  # in order: 'a', 'A'
                    )

            if pda.d.__contains__(d_lambda_key):
                to_read, to_write = pda.d[d_lambda_key]

                # Check if we can remove the specified letters ('A')
                if can_read_stack_top(stack, to_read):
                    new_stack = read_stack_top(stack, to_read)  # stiva fara 'A'
                    for letter in reversed(to_write):
                        new_stack.append(letter)

                    next_snaps.append(
                        Snapshot(top_snap.word, state2, new_stack)  # in order: 'a', 'A'
                    )

        for snap in next_snaps:
            queue.append(snap)

    # No 'return True' was reach so far, all snapshots were checked, so the word is not in accepted by the PDA
    return False

def main():
    pda = read_pda('input.txt')

    for word in ['aa', 'a', 'aaaaaaaaaa', '']:
        print(f"'{word}' -> {is_accepted(pda, word, True, True)}")


if __name__ == '__main__':
    main()
