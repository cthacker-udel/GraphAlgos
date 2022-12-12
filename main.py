from enum import Enum
from typing import Callable, List

collected_ = []
collecting_ = []


# solution = lambda x: [w for w in x if not collecting_ and not collecting_.clear() and (len([z for z in x if (z[0] == w[-1] or z[-1] == w[0]) and z != w and not collecting_.append(True) and not collected_.append(z)]) > 0) and w not in collected_]

def solution(arr, previous_chain_word='', chain=None):
    result = False
    if not chain:
        chain = []
    if len(arr) == 0:
        return True
    else:
        print(chain)
        for i in range(len(arr)):
            curr_word = arr[i]
            if previous_chain_word:
                if previous_chain_word[-1] == curr_word[0]:
                    result = result or solution(arr[:i] + arr[i + 1:], curr_word, [curr_word] + chain)
                else:
                    result = False
            else:
                result = result or solution(arr[:i] + arr[i + 1:], curr_word, [curr_word] + chain)
        return result


def is_defended(attackers: List[int], defenders: List[int]) -> bool:
    try:
        attacker_survivors = 0
        defender_survivors = 0
        base_attack_attackers = sum(attackers)
        base_attack_defenders = sum(defenders)
        i = 0
        j = 0
        while i < len(attackers) or j < len(defenders):
            if i >= len(defenders) and i < len(attackers):
                ## in bounds of attackers but out-of-bounds for defenders
                attacker_survivors += 1
                i += 1
            elif j >= len(attackers) and j < len(defenders):
                ## in bounds of defenders but out-of-bounds for attacker
                defender_survivors += 1
                j += 1
            elif i < len(attackers) and j < len(defenders):
                attacker_survivors += 1 if attackers[i] > defenders[j] else 0
                defender_survivors += 1 if defenders[j] > attackers[i] else 0
                i += 1
                j += 1
        # print(attacker_survivors)
        # print(defender_survivors)
        if attacker_survivors == defender_survivors:
            return base_attack_defenders >= base_attack_attackers
        else:
            return defender_survivors > attacker_survivors
    except Exception as e:
        print(e)


def perpendicular(n):
    if n == 0:
        return 0
    starter = 1
    first = False
    total = 0
    for i in range(1, n):
        total += starter
        starter += 1 if first else 0
        first = True if not first else False
    return total


def bouncing_ball(h: float, bounce: float, window: float) -> float:
    """
    Computes the # of times a ball bounced from height **h** passes through the window **window**

    :param h: The initial height of the drop
    :param bounce: The bounce the ball takes when bounced
    :param window: The height of the window
    :return: How many times the ball will pass through the window
    """
    if h <= 0 or (bounce <= 0 or bounce >= 1) or window >= h:  # if the height is 0, or the bounce is 0, or the window is higher then the initial height, then calculation is impossible, so return -1
        return -1
    times = 1  # the number of times the ball is seen, by default 1
    seen = True  # true while the ball is seen
    going_up = True  # true if the ball is moving down from above the window
    while seen:  # while the ball has been seen through the window
        curr_bounce_height = h * bounce  # calculates the next height the ball will be falling from
        seen = curr_bounce_height > window  # if the bounce height is greater than the window, ball has been seen
        times += 2 if seen else 0  # add 2 times if the seen variable is true, meaning that the ball has gone up and gone down
        h = curr_bounce_height  # set the new height to the pre-calculated height `curr_bounce_height`
    return times  # return the number of times the ball has been seen


class Turn(Enum):
    FRANK = 0
    SAM = 1
    TOM = 2

class TurnCycle(Enum):
    FIRST = 0,  ## Frank, Sam, Tom
    SECOND = 1,  ## Sam, Tom, Frank
    THIRD = 2  ## Tom, Frank, Sam

class Player(Enum):
    FRANK = 'f'
    SAM = 's'
    TOM = 't'



def solution(frank: List[int], sam: List[int], tom: List[int]) -> bool:
    who_goes_first = Turn.FRANK if 0 in frank else Turn.SAM if 0 in sam else Turn.TOM
    frank_wins = 0
    won = False
    if who_goes_first == Turn.FRANK:
        frank.remove(0)
    elif who_goes_first == Turn.SAM:
        sam.remove(0)
    else:
        tom.remove(0)

    first_turn = True
    ## does frank have a card that is greater then the min of both players
    while frank_wins < 2:
        for eachcard in frank:
            if first_turn and who_goes_first == Turn.SAM:
                if eachcard > min(tom):
                    tom.remove(min(tom))
                    frank.remove(eachcard)
                    first_turn = False
                    won = True
                    frank_wins += 1
                    break
            elif first_turn and who_goes_first == Turn.TOM:
                if eachcard > min(sam):
                    sam.remove(min(sam))
                    frank.remove(eachcard)
                    first_turn = False
                    won = True
                    frank_wins += 1
                    break
            elif first_turn and who_goes_first == Turn.FRANK:
                sam.remove(max(sam))
                tom.remove(max(tom))
                first_turn = False
                won = True
                break
            elif not first_turn and eachcard > min(sam) and eachcard > min(tom):
                frank_wins += 1
                sam.remove(min(sam))
                tom.remove(min(tom))
                frank.remove(eachcard)
                won = True
                break
            else:
                won = False
        if not won:
            break
    return frank_wins == 2







if __name__ == '__main__':
    print(solution([5, 7, 8, 9], [0, 2, 10, 11], [1, 3, 4, 6])) # T
    print(solution([0, 8, 9, 10], [2, 4, 7, 11], [1, 3, 5, 6]))
