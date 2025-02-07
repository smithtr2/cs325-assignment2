import numpy as np
from check_cost import read_cost_matrix


COST_FILE = "imp2cost.txt"
INPUT_FILE = "imp2input.txt"
OUTPUT_FILE = "imp2output.txt"

# compute the edit distance between str1 and str2, and record the backtrace infomation
def edit_distance(str1, str2):
    m, n = len(str1), len(str2)
    # Read the cost from cost file
    loss_matrix, x_indexdict, y_indexdict = read_cost_matrix(fns=COST_FILE)
    # Initialize distance table and ptr
    d = np.zeros((m + 1, n + 1), dtype=int)
    ptr = np.full((m + 1, n + 1), None, dtype=object)
    # Initialize the distance for convert str1 to an empty string
    for i in range(1, m + 1):
        # it has different cost to remove different character
        # so, we need get the cost from loss_matrix
        d[i][0] = d[i-1][0] + loss_matrix[x_indexdict[str1[i-1]]][y_indexdict['-']]
        ptr[i][0] = (i-1, 0)

    # Initialize the distance for convert str2 to an empty string
    for j in range(1, n + 1):
        # it has different cost to remove different character
        # so, we need get the cost from loss_matrix
        d[0][j] = d[0][j-1] + loss_matrix[x_indexdict[str2[j-1]]][y_indexdict['-']]
        ptr[0][j] = (0, j - 1)
    
    # compute and fill up the distance table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            v1 = d[i-1][j] + loss_matrix[x_indexdict[str1[i-1]]][y_indexdict['-']] #delete a character
            v2 = d[i][j-1] + loss_matrix[x_indexdict['-']][y_indexdict[str2[j-1]]] #insert a character
            v3 = d[i-1][j-1] + loss_matrix[x_indexdict[str1[i-1]]][y_indexdict[str2[j-1]]] #replace a character
            # get the minimum distance, and record the trace information
            min_distance = min(v1, v2, v3)
            d[i][j] = min_distance
            if v1 == min_distance:
                ptr[i][j] = (i-1, j)
            elif v2 == min_distance:
                ptr[i][j] = (i, j - 1)
            else:
                ptr[i][j] = (i - 1, j - 1)
    return d[m][n], ptr

# Backtracing
def backtrace(ptr, str1, str2):
    i, j = len(str1), len(str2)
    aligned_str1 = []
    aligned_str2 = []
    while i > 0 or j > 0:
        prev_i, prev_j = ptr[i][j]
        if prev_i == i - 1 and prev_j == j - 1:
            # replace or keep original character
            aligned_str1.append(str1[i - 1])
            aligned_str2.append(str2[j - 1])
        elif prev_i == i - 1 and prev_j == j:
            # delete a character
            aligned_str1.append(str1[i - 1])
            aligned_str2.append('-')
        else:
            # insert a character
            aligned_str1.append('-')
            aligned_str2.append(str2[j - 1])
        i, j = prev_i, prev_j
    aligned_str1.reverse()
    aligned_str2.reverse()
    return ''.join(aligned_str1), ''.join(aligned_str2)

if __name__ == "__main__":
    # Read all the input data into memory
    lines = []
    with open(INPUT_FILE, "r") as file:
        lines = file.readlines()

    # Process each line to get the result
    results = []
    for line in lines:
        str1, str2 = line.strip().split(",")
        distance, ptr = edit_distance(str1, str2)
        str1_result, str2_result = backtrace(ptr, str1, str2)
        results.append(','.join([str1_result, str2_result]) + ':' + str(distance))

    # Write results into output file
    with open(OUTPUT_FILE, "w") as file:
        for result in results:
            file.write(result + "\n")
