import numpy as np

def fast_power(number, degree: int, multiplication_func=lambda x, y: x * y, one=1):
    """
        Функция быстрого возведения числа в степень
        
        Input:
            number              - это число, или вообще любая сущность, над которой существует ассоциативная операция
            degree              - степень возведения или применения ассоциативной операции
            multiplication_func - операция умножения по двум сущностям, или ассоциативная операция. По умолчанию - умножение
            one                 - единица в поле по этой операции
        
        Output:
            result - результат возведения сущности в степень по ассоцитивной операции
    """
    if degree == 0:
        return one
    if degree % 2 == 0:
        tmp_result = fast_power(number, degree // 2, multiplication_func, one)
        return multiplication_func(tmp_result, tmp_result)
    return multiplication_func(number, fast_power(number, degree - 1, multiplication_func, one))

def fast_fibon(number):
    """
        Функция быстрого подсчета числа Фибоначчи
        Функция не работает для больших номеров, поскольку numpy ограничены. Для более корректной реализации нужно реализовывать класс матрицы
        
        Input: 
            number - номер числа Фибоначчи
            
        Output:
            result - самое число Фибоначчи
    """
    return fast_power(np.array([[0, 1], [1, 1]]), number, lambda x, y: x @ y, np.array([[1, 0], [0, 1]]))[0][0]