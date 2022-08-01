from PrimeNumbersFunction import check_is_prime_number
from PrimeNumbersFunction import factorize_number
from PrimeNumbersFunction import euler_function
from PrimeNumbersFunction import gcd
from PrimeNumbersFunction import eratosthenes_sieve
from PrimeNumbersFunction import extended_euclid_algorithm
from PrimeNumbersFunction import inversed_in_ring

from FastPower import fast_power

from SearchElements import binary_search


def test__check_is_prime_number():
    wrong_answer_numbers = []
    for number in range(2, 10000):
        my_answer = check_is_prime_number(number)
        real_answer = True
        for i in range(2, number):
            if number % i == 0:
                real_answer = False
        if my_answer != real_answer:
            wrong_answer_numbers.append(number)
    assert len(wrong_answer_numbers) == 0, "Тест проверки на простоту числа не пройден! (check_is_prime_number)"
                
        
def test__factorize_number():
    wrong_answer_numbers = []
    for number in range(2, 10000):
        my_answer = factorize_number(number)
        prod = 1
        for k, v in my_answer.items():
            assert check_is_prime_number(k), "Тест факторизации числа не пройден (factorize_number)"
            prod *= k ** v
        assert prod == number, "Тест факторизации числа не пройден (factorize_number)"
        
def test__euler_function():
    wrong_answer_numbers = []
    for number in range(2, 10000):
        my_answer = euler_function(number)
        real_answer = 0
        for b in range(1, number):
            if gcd(b, number) == 1:
                real_answer += 1
        if my_answer != real_answer:
            wrong_answer_numbers.append(number)
    assert len(wrong_answer_numbers) == 0, "Тест подсчета функции Эйлера не пройден (euler_function)"


def test__fast_power__numbers():
    wrong_answer_pairs = []
    for number in range(2, 51):
        for degree in range(1, 16):
            my_answer = fast_power(number, degree)
            
            real_answer = 1
            for p in range(degree):
                real_answer *= number
            if my_answer != real_answer:
                wrong_answer_pairs.append({"number": number, "degree": degree})
    assert len(wrong_answer_pairs) == 0, "Тест на быстрое возведение в степень не пройден (fast_power)"
    
    
def test__eratosthenes_sieve():
    for number in range(2, 3001):
        my_answer = eratosthenes_sieve(number)
        
        real_answer = []
        for i in range(2, number + 1):
            if check_is_prime_number(i):
                real_answer.append(i)
        if real_answer != my_answer:
            assert False, "Тест на решето Эратосфена не пройден (eratosthenes_sieve)"

            
def test__extended_euclid_algorithm():
    for a in range(1, 1000):
        for b in range(1, 1000):
            my_answer = extended_euclid_algorithm(a, b)
            failed_text = "Тест на расширенный алгоритм Евклида не пройден (extended_euclid_algorithm)"
            assert my_answer[0] == gcd(a, b), failed_text
            assert a * my_answer[1][0] + b * my_answer[1][1] == my_answer[0], failed_text

            
def test__inversed_in_ring():
    for a in range(1, 1000):
        for m in range(1, 1000):
            if gcd(a, m) == 1:
                my_answer = inversed_in_ring(a, m)
                assert (a * my_answer - 1) % m == 0, "Тест на поиск обратного элемента в кольце не пройден (inversed_in_ring)"
                
                
def test__binary_search():
    arr = [2 * i + 1 for i in range(1, 11)]
    for i in range(len(arr)):
        found_idx = binary_search(arr[i], lambda x: arr[x], len(arr))
        assert found_idx == i
    assert binary_search(4, lambda x: arr[x], len(arr)) == -1
    assert binary_search(-1, lambda x: arr[x], len(arr)) == -1
    assert binary_search(100, lambda x: arr[x], len(arr)) == -1
    
    arr = [2 * i + 1 for i in range(1, 10)]
    for i in range(len(arr)):
        found_idx = binary_search(arr[i], lambda x: arr[x], len(arr))
        assert found_idx == i
    assert binary_search(4, lambda x: arr[x], len(arr)) == -1
    assert binary_search(-1, lambda x: arr[x], len(arr)) == -1
    assert binary_search(100, lambda x: arr[x], len(arr)) == -1
    
    assert binary_search(100, lambda x: 2, 1) == -1
    assert binary_search(2, lambda x: 2, 1) == 0
    assert binary_search(0, lambda x: 2, 1) == -1
    
    assert binary_search(100, lambda x: None, 0) == -1