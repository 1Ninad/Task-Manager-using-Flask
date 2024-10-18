def mergeSort(arr, key=lambda x: x):
    """MergeSort implementation for sorting tasks."""
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]

        mergeSort(L, key)
        mergeSort(R, key)

        i = j = k = 0

        while i < len(L) and j < len(R):
            if key(L[i]) < key(R[j]):
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

    return arr