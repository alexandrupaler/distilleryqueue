import numpy as np
import fukudahiroshi as fh

def process_file(lines):
    current_state = 0

    states = {}
    states[0] = {-1: 0, 0: 0, 1: 0}

    total_transitions = 0
    for line in lines[2:]:
        # print(line)
        # each line is a transition -- for the moment

        # first line is header
        # second line is start configuration
        splts = line.split(",")

        if len(splts) != 3 or len(splts[1]) == 0:
            # something is wrong
            # just continue
            print("This line is problem --", line)
            continue

        total_transitions += 1

        line_state = int(splts[1])

        difference = line_state - current_state
        states[current_state][difference] += 1

        # change the current state
        current_state = line_state
        # is the current state in the collection?
        if not current_state in states:
            # seems not, then introduce it
            states[current_state] = {-1: 0, 0: 0, 1: 0}

    # for checking that probabilities are correct
    check_transitions = 0

    states_prob = {}
    if total_transitions > 0:
        for state in states:
            states_prob[state] = {}
            sum_trans = (states[state][-1] + states[state][0] + states[state][1])
            states_prob[state][state - 1] = states[state][-1] / sum_trans
            states_prob[state][state - 0] = states[state][-0] / sum_trans
            states_prob[state][state + 1] = states[state][+1] / sum_trans

            check_transitions += sum_trans

    assert (check_transitions == total_transitions)

    print("Transition probabilities:")
    print("Total transitions", total_transitions)
    print("Maximum state int,float", len(states), len(states_prob))

    # print(states)

    m = make_matrix(states_prob)

    return m

def main():
    fnames = [
        "./csv/adder0016_007.csv",
        # "./csv/adder0016_max.csv",
        # "./csv/adder0032_007.csv",
        # "./csv/adder0032_max.csv",
        # "./csv/adder0064_007.csv",
        # "./csv/adder0064_max.csv",
        # "./csv/adder0128_007.csv",
        # "./csv/adder0128_max.csv",
        # "./csv/adder0256_007.csv",
        # "./csv/adder0256_max.csv",
        # "./csv/adder0512_007.csv",
        # "./csv/adder0512_max.csv",
        # "./csv/adder1024_007.csv",
        # "./csv/adder1024_max.csv",
        # "./csv/adder1536_007.csv",
        # "./csv/adder1536_max.csv",
        # "./csv/adder2048_007.csv",
        # "./csv/adder2048_500.csv",
        # "./csv/adder2048_max.csv"
        ]

    for fname in fnames:
        with open(fname, 'r') as circfile:
            print("\n\n\n" + fname)
            # read entire file into string stored
            lines = circfile.read().split("\n")

            res_matrix = process_file(lines)

            res_fukuda = fh.markov(res_matrix)

            print(res_fukuda)

            sum = 0
            for x in res_fukuda:
                sum += x

            print("Sum", sum)
            print("Avg", weighted_average(res_fukuda))
            print("Utl", average_utilisation(res_fukuda))

            # s = print_matrix(res_matrix, precision)
            #
            # with open(fname + ".p_" + str(precision) + ".matrix", 'w') as savefile:
            #     savefile.write(s)


def weighted_average(steady_vector):
    avg = 0
    for i in range(len(steady_vector)):
        avg += i * steady_vector[i]
    return avg

def average_utilisation(steady_vector):
    return 1 - steady_vector[0]

def print_matrix(matrix, precision):
    '''
    https://stackoverflow.com/questions/13214809/pretty-print-2d-python-list
    :param matrix:
    :return:
    '''

    format_string = "%." + str(precision) + "f"

    float_formatter = lambda x: format_string % x

    s = [[str(float_formatter(e)) for e in row] for row in matrix]
    # s = [[str(e) for e in row] for row in matrix]
    lens = [max(map(len, col)) for col in zip(*s)]
    # fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    fmt = ' '.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    s = '\n'.join(table)
    return s

def make_matrix(states_prob):
    matrix = np.ndarray((len(states_prob), len(states_prob)), dtype=float)

    for i in range(len(states_prob)):
        for j in range(len(states_prob)):
            matrix[i][j] = 0

    for state in states_prob:
        for key in states_prob[state]:
            if key != -1 and key != len(states_prob):
                matrix[state][key] = float(states_prob[state][key])
                # matrix[key][state] = float(states_prob[key][state])

    return matrix

if __name__ == "__main__":


    main()







