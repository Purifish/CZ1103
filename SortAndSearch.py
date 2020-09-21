
def BinarySearch(list1, key, lower, upper):
    if lower > upper:
        return -1
    mid = (upper + lower) // 2
    if list1[mid] == key:
        return mid #returns index of target value
    if list1[mid] > key:
        return BinarySearch(list1, key, lower, mid - 1)
    return BinarySearch(list1, key, mid + 1, upper)


def BubbleSort(list1):
    listLen = len(list1)

    for i in range(listLen-1, 0, -1): #from last index to 1(not 0)
        swaps = False
        for j in range(i):
            if list1[j] > list1[j + 1]:
                list1[j], list1[j + 1] = list1[j + 1], list1[j] #Swap
                swaps = True
        if not swaps:
            break

def Merge(leftList, rightList):
    mergedList = []
    while leftList and rightList: #while both are not empty
        if leftList[0] < rightList[0]:
            mergedList.append(leftList[0])
            leftList.pop(0)
        else:
            mergedList.append(rightList[0])
            rightList.pop(0)

    if leftList:
        mergedList.extend(leftList)
    else:
        mergedList.extend(rightList)
    return mergedList
    
def MergeSort(list1):
    listLen = len(list1)
    if listLen > 1:
        leftHalf = list1[:listLen // 2]
        rightHalf = list1[listLen // 2:]
        leftHalf = MergeSort(leftHalf)
        rightHalf = MergeSort(rightHalf)
        list1 = Merge(leftHalf, rightHalf)

    return list1
