# this is a merge sort algorithm that sorts objects with an attribute 'fitness' from greatest to least


def mergeSort(arr):
    # if this array contains 1 element or less, it is sorted
    if len(arr) <= 1:
        return arr
    # split array in halfs
    former = arr[:len(arr) // 2]
    latter = arr[len(arr) // 2:]

    # recursively sort
    former = mergeSort(former)
    latter = mergeSort(latter)

    # return the sorted array
    return merge(former, latter)


def merge(former, latter):
    arr = []

    # while both halfs have elements, add the higher element first in the list
    while len(former) > 0 and len(latter) > 0:
        if former[0].fitness > latter[0].fitness:
            arr.append(former.pop(0))
        else:
            arr.append(latter.pop(0))

    # now only one list should have elments, so add the remaining elements

    while len(former) > 0:
        arr.append(former.pop(0))
    while len(latter) > 0:
        arr.append(latter.pop(0))

    # return merged array
    return arr


# this method is specifically for numbers
# yes this is a really dumb way to code this by just copy pasting the code but whatever
def mergeSortNum(arr):
    # if this array contains 1 element or less, it is sorted
    if len(arr) <= 1:
        return arr
    # split array in halfs
    former = arr[:len(arr) // 2]
    latter = arr[len(arr) // 2:]

    # recursively sort
    former = mergeSortNum(former)
    latter = mergeSortNum(latter)

    # return the sorted array
    return mergeNum(former, latter)


# this method is specifically for numbers
# yes this is a really dumb way to code this by just copy pasting the code but whatever
def mergeNum(former, latter):
    arr = []

    # while both halfs have elements, add the higher element first in the list
    while len(former) > 0 and len(latter) > 0:
        if former[0] > latter[0]:
            arr.append(former.pop(0))
        else:
            arr.append(latter.pop(0))

    # now only one list should have elments, so add the remaining elements

    while len(former) > 0:
        arr.append(former.pop(0))
    while len(latter) > 0:
        arr.append(latter.pop(0))

    # return merged array
    return arr
