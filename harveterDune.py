from typing import Callable, List

collected_ = []
collecting_ = []

#solution = lambda x: [w for w in x if not collecting_ and not collecting_.clear() and (len([z for z in x if (z[0] == w[-1] or z[-1] == w[0]) and z != w and not collecting_.append(True) and not collected_.append(z)]) > 0) and w not in collected_]

def solution(arr, previous_chain_word = '', chain = None):
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
        while i < len(attackers) and j < len(defenders):
            if i >= len(defenders) and i < len(attackers):
                ## in bounds of attackers but out-of-bounds for defenders
                attacker_survivors += 1
                attackers += 1
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
        print(attacker_survivors)
        print(defender_survivors)
        if attacker_survivors == defender_survivors:
            return base_attack_attackers > base_attack_defenders
        else:
            return attacker_survivors > defender_survivors
    except Exception as e:
        print(e)

if __name__ == '__main__':
    print(is_defended([ 2, 9, 9, 7 ], [ 1, 1, 3, 8]))