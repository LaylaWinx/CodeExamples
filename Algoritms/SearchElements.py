def binary_search(element, getter, list_length):
    """
        Бинарный поиск на массиве структур
        
        Input:
            element - искомый элемент
            getter - функция получения поля по индексу
            
        Output:
            result - индекс в массиве, или -1, если элемента нет
    """
    left_idx = -1
    right_idx = list_length
    while left_idx < right_idx - 1:
        mid_idx = (left_idx + right_idx) // 2
        if getter(mid_idx) < element:
            left_idx = mid_idx
        else:
            right_idx = mid_idx
    if right_idx == list_length:
        return -1
    if getter(right_idx) == element:
        return right_idx
    return -1
    