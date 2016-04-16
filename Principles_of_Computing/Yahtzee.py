"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def gen_all_permutations(outcomes, length):
    """
    Iterative function that enumerates the set of all permutations of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                if (not (item in partial_sequence)):
                    new_sequence = list(partial_sequence)
                    new_sequence.append(item)
                    temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    count_dict = {}
    for idx in hand:
        if count_dict.has_key(idx):
            count_dict[idx] += idx
        else:
            count_dict[idx] = idx
    max_score = 0
    for idx in count_dict:
        if (count_dict[idx] > max_score):
            max_score = count_dict[idx]
    return max_score


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value of the held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    sum_score = 0
    held_dice_list = list(held_dice)
    cases = gen_all_sequences(range(1, num_die_sides + 1), num_free_dice)
    for case in cases:
        case_list = list(case)
        case_list.extend(held_dice_list)
        sum_score += score(tuple(case_list))
    return float(sum_score) / len(cases)


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    total_cases = set([()])
    for remain_count in range(1, len(hand) + 1):
        cases_indexes = gen_all_permutations(range(len(hand)), remain_count)
        cases = []
        for case_item in cases_indexes:
            temp = []
            for item in case_item:
                temp.append(hand[item])
            cases.append(tuple(temp))
        cases_sorted = []
        for case in cases:
            case_list = list(case)
            case_list.sort()
            cases_sorted.append(tuple(case_list))
        total_cases = total_cases.union(set(cases_sorted))
    return total_cases


def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    max_expected = 0.0
    for case in gen_all_holds(hand):
        case_expected = expected_value(case, num_die_sides, len(hand) - len(case))
        if (case_expected > max_expected):
            best_hold = case
            max_expected = case_expected
    return (max_expected, best_hold)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
#run_example()


#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)
