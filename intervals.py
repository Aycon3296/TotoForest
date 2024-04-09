from collections import namedtuple
import heapq


def min_values(intervals):
    # event queue
    events = [] # (x, is_end, index, value, label)
    for index, (start, stop, value, label) in enumerate(intervals):
        events.append((start, False, index, value, label))
        events.append((stop , True , index, value, label))
    events.sort()

    # status
    deleted = [False] * (len(events) // 2)
    heap = []

    # print
    last_start = None
    last_value = None
    last_label = None

    for x, is_end, index, value, label in events:
        # update status
        if is_end:
            deleted[index] = True
        else:
            heapq.heappush(heap, (value, index, label))

        # remove deleted items from heap top
        while heap and deleted[heap[0][1]]:
            heapq.heappop(heap)
        
        # print
        value = heap[0][0] if heap else None
        label = heap[0][2] if heap else None
        if value != last_value:
            if last_value is not None and last_start < x:
                yield last_label, last_start, x 
            last_start = x
            last_value = value
            last_label = label


def max_values(intervals):
    return min_values(
        (start, stop, (-value, stop - start), value)
        for value, start, stop in intervals
    )

def inlay_right_to_left(left: tuple[int, float, float], right: tuple[int, float, float]):
    #  0     [___]      target (right)
    #  1 [__]|   |      strict left
    #  2  [__]   |      left
    #  3    [__] |      intersect
    #  4     [__]|      intersect
    #  5     |[_]|      inner
    #  6     [___]      strict equal
    #  7    [____]      intersect
    #  8    [______]    external
    #  9     [_____]    intersect
    # 10     |[__]      intersect
    # 11     |  [__]    intersect
    # 12     |   [__]   right
    # 13     |   |[__]  strict right
    
    left_id_key, left_start, left_stop = left
    right_id_key, right_start, right_stop = right
    
    # strict left
    if (left_start < right_start and left_start < right_stop) and (left_stop < right_start and left_stop < right_stop):
        return [left, right]
    
    # left
    elif (left_start < right_start and left_start < right_stop) and (left_stop == right_start and left_stop < right_stop):
        return [left, right]
    
    # intersect
    elif (left_start < right_start and left_start < right_stop) and (left_stop > right_start and left_stop < right_stop):
        return [(left_id_key, left_start, right_start), (right_id_key, right_start, right_stop)]
    
    # intersect
    elif (left_start == right_start and left_start < right_stop) and (left_stop > right_start and left_stop < right_stop):
        return [right]
    
    # inner
    elif (left_start > right_start and left_start < right_stop) and (left_stop > right_start and left_stop < right_stop):
        return [right]
    
    # strict equal
    elif (left_start == right_start and left_start < right_stop) and (left_stop > right_start and left_stop == right_stop):
        return [right]
    
    # intersect
    elif (left_start < right_start and left_start < right_stop) and (left_stop > right_start and left_stop == right_stop):
        return [(left_id_key, left_start, right_start), right]
    
    # external
    elif (left_start < right_start and left_start < right_stop) and (left_stop > right_start and left_stop > right_stop):
        return [(left_id_key, left_start, right_start), right, (left_id_key, right_stop, left_stop)]
    
    # intersect
    elif (left_start == right_start and left_start < right_stop) and (left_stop > right_start and left_stop > right_stop):
        return [right, (left_id_key, right_stop, left_stop)]
    
    # intersect
    elif (left_start > right_start and left_start < right_stop) and (left_stop > right_start and left_stop == right_stop):
        return [right]
    
    # intersect
    elif (left_start > right_start and left_start < right_stop) and (left_stop > right_start and left_stop > right_stop):
        return [right, (left_id_key, right_stop, left_stop)]

    # right
    elif (left_start > right_start and left_start == right_stop) and (left_stop > right_start and left_stop > right_stop):
        return [right, left]
    
    # strict right
    else:
        # (terminate case)
        assert (left_start > right_start and left_start > right_stop) and (left_stop > right_start and left_stop > right_stop)
        return [right, left]

def test():
    for intervals, expected in (
        # value left > value right
        ([(2, 3, 6), (1, 0, 2)], [(1, 0, 2), (2, 3, 6)]),
        ([(2, 3, 6), (1, 1, 3)], [(1, 1, 3), (2, 3, 6)]),
        ([(2, 3, 6), (1, 2, 4)], [(1, 2, 3), (2, 3, 6)]),
        ([(2, 3, 6), (1, 3, 5)], [(2, 3, 6)]),
        ([(2, 3, 6), (1, 4, 5)], [(2, 3, 6)]),
        ([(2, 3, 6), (1, 3, 6)], [(2, 3, 6)]),
        ([(2, 3, 6), (1, 2, 6)], [(1, 2, 3), (2, 3, 6)]),
        ([(2, 3, 6), (1, 2, 7)], [(1, 2, 3), (2, 3, 6), (1, 6, 7)]),
        ([(2, 3, 6), (1, 3, 7)], [(2, 3, 6), (1, 6, 7)]),
        ([(2, 3, 6), (1, 4, 6)], [(2, 3, 6)]),
        ([(2, 3, 6), (1, 5, 7)], [(2, 3, 6), (1, 6, 7)]),
        ([(2, 3, 6), (1, 6, 8)], [(2, 3, 6), (1, 6, 8)]),
        ([(2, 3, 6), (1, 7, 9)], [(2, 3, 6), (1, 7, 9)]),
        
        # value left == value right
        ([(2, 3, 6), (2, 0, 2)], [(2, 0, 2), (2, 3, 6)]),               # 2 / (6 - 3) < 2 / (2 - 0)
        ([(2, 3, 6), (2, 1, 3)], [(2, 1, 3), (2, 3, 6)]),               # 2 / (6 - 3) < 2 / (3 - 1)
        ([(2, 3, 6), (2, 2, 4)], [(2, 2, 4), (2, 4, 6)]),               # 2 / (6 - 3) < 2 / (4 - 2)
        ([(2, 3, 6), (2, 3, 5)], [(2, 3, 5), (2, 5, 6)]),               # 2 / (6 - 3) < 2 / (5 - 3)
        ([(2, 3, 6), (2, 4, 5)], [(2, 3, 4), (2, 4, 5), (2, 5, 6)]),    # 2 / (6 - 3) < 2 / (5 - 4)
        ([(2, 3, 6), (2, 3, 6)], [(2, 3, 6)]),                          # 2 / (6 - 3) == 2 / (6 - 3) (copy)
        ([(2, 3, 6), (2, 2, 6)], [(2, 2, 3), (2, 3, 6)]),               # 2 / (6 - 3) > 2 / (6 - 2)
        ([(2, 3, 6), (2, 2, 7)], [(2, 2, 3), (2, 3, 6), (2, 6, 7)]),    # 2 / (6 - 3) > 2 / (7 - 2)
        ([(2, 3, 6), (2, 3, 7)], [(2, 3, 6), (2, 6, 7)]),               # 2 / (6 - 3) > 2 / (7 - 3)
        ([(2, 3, 6), (2, 4, 6)], [(2, 3, 4), (2, 4, 6)]),               # 2 / (6 - 3) < 2 / (6 - 4)
        ([(2, 3, 6), (2, 5, 7)], [(2, 3, 5), (2, 5, 7)]),               # 2 / (6 - 3) < 2 / (7 - 5)
        ([(2, 3, 6), (2, 6, 8)], [(2, 3, 6), (2, 6, 8)]),               # 2 / (6 - 3) < 2 / (8 - 6)
        ([(2, 3, 6), (2, 7, 9)], [(2, 3, 6), (2, 7, 9)]),               # 2 / (6 - 3) < 2 / (9 - 7)
        
        # value left < value right
        ([(2, 3, 6), (3, 0, 2)], [(3, 0, 2), (2, 3, 6)]),
        ([(2, 3, 6), (3, 1, 3)], [(3, 1, 3), (2, 3, 6)]),
        ([(2, 3, 6), (3, 2, 4)], [(3, 2, 4), (2, 4, 6)]),
        ([(2, 3, 6), (3, 3, 5)], [(3, 3, 5), (2, 5, 6)]),
        ([(2, 3, 6), (3, 4, 5)], [(2, 3, 4), (3, 4, 5), (2, 5, 6)]),
        ([(2, 3, 6), (3, 3, 6)], [(3, 3, 6)]),
        ([(2, 3, 6), (3, 2, 6)], [(3, 2, 6)]),
        ([(2, 3, 6), (3, 2, 7)], [(3, 2, 7)]),
        ([(2, 3, 6), (3, 3, 7)], [(3, 3, 7)]),
        ([(2, 3, 6), (3, 4, 6)], [(2, 3, 4), (3, 4, 6)]),
        ([(2, 3, 6), (3, 5, 7)], [(2, 3, 5), (3, 5, 7)]),
        ([(2, 3, 6), (3, 6, 8)], [(2, 3, 6), (3, 6, 8)]),
        ([(2, 3, 6), (3, 7, 9)], [(2, 3, 6), (3, 7, 9)]),
    ):
        # actual = list(max_values(intervals))
        intervals.sort(key= lambda inter: (float(inter[0]), float(inter[0]) / (float(inter[2]) - float(inter[1]))))        
        actual = list(inlay_right_to_left(intervals[0], intervals[1]))
        if actual != expected:
            print(intervals, expected, actual)


test()
