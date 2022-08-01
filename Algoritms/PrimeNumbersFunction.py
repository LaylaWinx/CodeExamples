from typing import Tuple
from SearchElements import binary_search

def check_is_prime_number(number: int) -> bool:
    """
        Проверка, является ли число простым
        
        Input:
            number - число, которое надо проверить
            
        Output:
            result - bool-значение с ответом, является ли number простым числом
    """
    
    # Во-первых, стоит заметить, что простые делители необходимо искать не дальше, чем до корня из числа.
    prime_divider = 2
    result = {}
    while prime_divider * prime_divider <= number:
        if number % prime_divider == 0:
            return False
        prime_divider += 1
    return True


def factorize_number(number: int) -> dict[int, int]:
    """
        Факторизация натурального числа, то есть разложение его на множители
        
        Input:
            number - натуральное число, для которого получается факторизация
            
        Output:
            result - словарь, ключи которого - простые натуральные числа, а значения - степени соответственного числа в разложении
                     если словарь пустой - то число равно единице. 
    """
    
    # Во-первых, стоит заметить, что простые делители необходимо искать не дальше, чем до корня из числа.
    prime_divider = 2
    result = {}
    while prime_divider * prime_divider <= number:
        degree = 0
        while number % prime_divider == 0:
            degree += 1
            number //= prime_divider
        # Если окажется, что prime_number не простое число, то на него не будет делиться number
        if degree > 0:
            result[prime_divider] = degree
        prime_divider += 1
    if number != 1:
        result[number] = 1
    return result


def gcd(a: int, b: int) -> int:
    """
        Подсчет наибольшего общего делителя натуральных чисел a и b (GCD)
        
        Input:
            a - первое число
            b - второе число
        
        Output:
            result  - gcd(a, b)
    """
    while b > 0:
        a, b = b, a % b
    return a


def euler_function(number: int) -> int:
    """
        Подсчет функции Эйлера - количество чисел, не больших n, взаимно простых с ним
        https://e-maxx.ru/algo/euler_function

        Input:
            number - натуральное число

        Output:
            result - функция Эйлера для этого числа
    """
    factorization = factorize_number(number)
    
    result = 1
    for k, v in factorization.items():
        result *= (k - 1) * k ** (v - 1)
    return result


def eratosthenes_sieve(number: int) -> list[int]:
    """
        Подсчет решена Эратосфена - поиск всех простых чисел от 1 до number
        
        Input:
            number - число, до которого ищутся простые числа
            
        Output:
            result - набор простых чисел от 1 до number
    """
    is_prime_erat = [True for _ in range(number + 1)]
    is_prime_erat[0] = False
    is_prime_erat[1] = False
    for i in range(2, number + 1):
        if is_prime_erat[i]:
            k = 2
            while k * i <= number:
                is_prime_erat[k * i] = False
                k += 1
    result = []
    for i in range(2, number + 1):
        if is_prime_erat[i]:
            result.append(i)
    return result


def extended_euclid_algorithm(a: int, b: int) -> tuple[int, tuple[int, int]]:
    """
        Поиск gcd и коэффициентов x, y решения линейного уравнения
        ax + by = gcd(a, b)
        
        Input:
            a - натуральное число
            b - натуральное число
           
        Output:
            result - кортеж вида (gcd, (x, y))
    """
    if a == 0:
        return (b, (0, 1))
    res = extended_euclid_algorithm(b % a, a)
    gcd_num = res[0]
    x1, y1 = res[1]
    x = y1 - (b // a) * x1;
    y = x1;
    return (gcd_num, (x, y))


def inversed_in_ring(a: int, m: int) -> int:
    """
        Поиск обратного элемента в кольце по модулю m, то есть числа b, что (ab - 1) делится на m
        При этом гарантируется, что a и m - взаимно простые
        
        Input:
            a - натуральное число, к которому ищется обратный элемент
            m - порядок кольца
            
        Output:
            result - обратный элемент к a в кольце по модулю m
    """
    assert gcd(a, m) == 1, "a и m обязаны быть взаимно простыми"
    x, y = extended_euclid_algorithm(a, m)[1]
    return x


def meet_in_the_middle(f, g, x_array, y_array):
    """
        Решение задачи f(x) = g(y) для x из x_array и y из y_array
        
        Input:
            f - первая функция
            g - вторая функция
            x_array - возможные аргументы первой функции
            y_array - возможные аргументы второй функции
            
        Output:
            result - массив пар чисел x, y решений
    """
    left_values = []
    for x in x_array:
        left_values.append((f(x), x))
    left_values.sort()
    result = []
    for y in y_array:
        right_value = g(y)
        idx = binary_search(right_value, lambda idx: left_values[idx][0], len(left_values))
        if idx != -1:
            result.append((x_array[idx], y))
    return result