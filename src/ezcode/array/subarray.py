

def subarrays_with_target_sum(array: list, target: int) -> list[tuple[int, int]]:
    sum_so_far, sum_occurence, output = 0, {0: [-1]}, list()
    for index_end, data in enumerate(array):
        sum_so_far += data
        sum_matched = sum_so_far - target
        if sum_matched in sum_occurence:
            for index_start in sum_occurence[sum_matched]:
                output.append((index_start + 1, index_end))
        if sum_so_far not in sum_occurence:
            sum_occurence[sum_so_far] = list()
        sum_occurence[sum_so_far].append(index_end)
    return output

