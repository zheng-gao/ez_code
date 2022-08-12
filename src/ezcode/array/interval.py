

def intervals_overlapped(i1: tuple[int, int], i2: tuple[int, int]) -> bool:
    return i1[0] <= i2[1] and i2[0] <= i1[1]

  
def merge_overlapped_intervals(self, intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    intervals.sort(key=lambda x: x[0])
    merged, output = None, list()
    for interval in intervals:
        if merged is None:
            merged = interval
            continue
        if interval[0] <= merged[1]:
            if interval[1] > merged[1]:
                merged[1] = interval[1]
        else:
            output.append(merged)
            merged = interval
    if merged is not None:
        output.append(merged)
    return output




