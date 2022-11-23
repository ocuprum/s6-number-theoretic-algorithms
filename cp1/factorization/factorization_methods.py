import random
import galois
import numpy as np
from math import log, exp
from typing import Callable, List, Tuple, Union
import factorization.primes_to_300000 as pttt

# Знаходження НСД
def gcd(a: int, b: int) -> int:
    if a == 0:
        return b
    else:
        return gcd(b % a, a)

# Схема Горнера  
def horner_pow(a: int, b: int, module: int) -> int:
    if b == 0: return 1
    c = a
    degree = str(bin(b))[2:]
    for bit in degree[1:]:
        c = (c ** 2) % module
        if bit == '1': c = (c * a) % module
    return c

# Тест Міллера-Рабіна на простоту
def miller_rabin(p: int, k: int=5) -> bool:
    if p == 2: return True
    if p > 2 and k > 0:
        d = p - 1
        s = 0
        while d % 2 == 0:
            s += 1
            d //= 2
        
        counter = 0
        is_strong_pseudoprime = False
        while counter <= k:
            rand_x = random.randint(2, p - 1)
            if gcd(rand_x, p) == 1: 
                poss_pseudoprime = horner_pow(rand_x, d, p)
                if poss_pseudoprime == 1 or poss_pseudoprime == p-1 or poss_pseudoprime == -1:
                    is_strong_pseudoprime = True
                else: 
                    x = poss_pseudoprime
                    for _ in range(s):
                        x = (x ** 2) % p
                        if x == p-1 or x == -1: 
                            is_strong_pseudoprime = True
                            break
                        elif x == 1: 
                            return False
                if is_strong_pseudoprime: 
                    counter += 1
                    continue
                return False
            return False
        return True

# Метод пробних ділень (повертає False, якщо число просте)
def trial_division(n: int, B: int=10) -> Union[int, bool]:
    sq_n = int(n ** (1 / 2))
    nums = [int(num) for num in str(n)[::-1]]

    for prime in pttt.primes:
        if prime <= sq_n and prime <= 47:
            r = 1
            poss_n = 0
            for num in nums:
                poss_n += (num * r)
                r = (r * B) % prime
            if poss_n % prime == 0: return prime
    return False

# Функція f(x) = (x^2 + 1) mod n для rho-методу Полларда
def pollard_func(x: int, n: int) -> int:
    return (x ** 2 + 1) % n

# rho-метод Полларда, модифікація Флойда (повертає False, якщо алгоритм не знайшов дільника числа n)
def rho_pollard(n: int, x: int=2, y: int=2, func: Callable[[int], int]=pollard_func) -> Union[int, bool]:
    d = 1
    counter = 0
    while d == 1:
        if counter >= 5: return False 
        x = func(x, n)
        y = func(func(y, n), n)
        if x != y:
            d = gcd(y - x if y > x else x - y, n)
        else:
            x += 1
            y += 1
            counter += 1
    return d

# Обчислення символу Лежандра
def legendre_symbol(a: int, p: int) -> int:
    if p >= 2:
        if a >= p:
            a = a % p
        if a == 0:
            return 0
        elif a == 1:
            return 1
        elif a == -1 or a == p - 1:
            if ((p - 1) / 2) % 2 == 0: return 1 
            return -1
        elif a == 2:
            checker = horner_pow(p, 2, p)
            if ((checker - 1) / 8) % 2 == 0: return 1
            return -1
        else:
            result = horner_pow(a, (p - 1) // 2, p)
            return result if abs(result) < 2 else result - p

def sum_vectors(vectors: List[List[int]]) -> List[int]:
    sum_vector = galois.GF2([0] * len(vectors[0]))
    for vector in vectors:
        sum_vector += galois.GF2(vector)
    return sum_vector

def get_factor_base(n: int, degree: float) -> Union[List[int], bool]:
    # Формуємо факторну базу
    factor_base = [-1]
    bound = exp((log(n) * log(log(n))) ** (1 / 2)) ** degree

    if bound >= n ** (1 / 2) or bound >= 300000: return False

    for prime in pttt.primes:
        if legendre_symbol(n, prime) == 1 and 1 < prime < bound: 
            factor_base.append(prime)
    return factor_base

def get_el_of_continued_fraction(n: int, v_prev: int, alpha_prev: float, a_prev: int, u_prev: int) -> Tuple[int, float, int, int]:
    # Знаходимо наступний елемент ланцюгового дроба
    sq_n = n ** (1 / 2)

    v = (n - u_prev ** 2) / v_prev
    alpha = (sq_n + u_prev) / v
    a = int(alpha)
    u = a * v - u_prev
    return v, alpha, a, u

def get_fbase_vector(poss_smooth: int, factor_base: List[int]) -> List[int]:
    fbase_vector = [0] * len(factor_base)

    for i in range(len(factor_base)):
        if i != 0:
            while poss_smooth % factor_base[i] == 0:
                fbase_vector[i] = (fbase_vector[i] + 1) % 2
                poss_smooth //= factor_base[i]
        else:
            if poss_smooth < 0:
                fbase_vector[i] = 1
                poss_smooth //= -1
    return fbase_vector, poss_smooth

def zero_vector_x(system: List[List[int]]) -> Union[List[List[int]], bool]:
    x_s = []
    for i in range(len(system)):
        x = [0] * len(system[0])
        if system[i] == [0] * len(system[0]):
            x[i] = 1
            x_s.append(x)
    if len(x_s) > 1: x_s.append(sum_vectors(x_s))
    return x_s

def similar_vectors_x(system: List[List[int]]) -> Union[List[List[int]], bool]:
    x_s = []
    for i in range(len(system)):
        x = [0] * len(system)
        if system[i] in system[i+1:]: 
            x[i] = 1
            x[i + 1 + system[i+1:].index(system[i])] = 1
            x_s.append(x)
    if len(x_s) > 1: x_s.append(sum_vectors(x_s))
    return x_s

def solve_sle_GF2(system: List[List[int]]) -> List[int]:
    A = galois.GF2(system)
    b = galois.GF2([0] * len(system[0]))
    if np.linalg.matrix_rank(A) == len(system):
        x = np.linalg.solve(A, b)
        return x
    return False

def div_definer(n: int, x: List[int], b_s: List[int], smooth_nums: List[int]) -> Union[int, bool]:
    # Знайдемо X та Y
    X, Y = 1, 1
    for i in range(len(x)):
        if x[i] == 1:
            X = (X * b_s[i]) % n
            Y = (Y * smooth_nums[i])
    Y = (Y ** (1 / 2))

    if X != 1 and Y != 1:
        # Пошук дільника
        gcd1, gcd2 = gcd(X + Y, n), gcd(X - Y, n) 
        if 1 < gcd1 < n: return int(gcd1)
        elif 1 < gcd2 < n: return int(gcd2)
    return False


def check_x(x_s: Union[List[List[int]], List[int]], n: int, b_s: List[int], smooth_nums: List[int]) -> Union[int, bool]:
    if x_s:
        for x in x_s:
            if x is not False:
                result = div_definer(n, x, b_s, smooth_nums)
                if result: 
                    return result
    return False

# Метод Брілхарта-Моррісона
def brillhart_morrison(n: int, degree: float=(1 / (2 ** (1 / 2)))) -> int:
    if miller_rabin(n): return False
    if n % 2 == 0: return 2
    while True:
        # Формуємо факторну базу
        factor_base = get_factor_base(n, degree)
        if not factor_base: 
            return False
        
        # Розкладаємо n у ланцюговий дріб та шукаємо потенціальні гладкі числа
        v = 1
        alpha = n ** (1 / 2)
        a = int(alpha)
        u = a

        b_prev_prev, b_prev = 0, 1
        smooth_nums, b_s = [], []

        system = []
        iter_counter = 0
        while True:
            iter_counter += 1
            if iter_counter > 10000: return False
            # Обраховуємо новий елемент b за рекурентною формулою 
            b = (a * b_prev + b_prev_prev) % n
            b_prev_prev, b_prev = b_prev, b
            poss_smooth = (b ** 2) % n
            poss_smooth = poss_smooth if poss_smooth < n / 2 else poss_smooth - n

            # Перевіряємо, чи є число гладким, якщо так, то додаємо його вектор у систему
            num = poss_smooth
            fbase_vector, poss_smooth = get_fbase_vector(poss_smooth, factor_base)
            
            if poss_smooth == 1: 
                smooth_nums.append(num)
                b_s.append(b)
                system.append(fbase_vector)
            
                x_s = zero_vector_x(system)
                result = check_x(x_s, n, b_s, smooth_nums)
                if result: return result
                
                if len(system) > 1:
                    x_s = similar_vectors_x(system)
                    result = check_x(x_s, n, b_s, smooth_nums)
                    if result: return result

                if len(system) == len(system[0]):
                    x_s = [solve_sle_GF2(system)]
                    if x_s: result = check_x(x_s, n, b_s, smooth_nums)
                    if result: return result 
                    else: 
                        system = system[-1:]
                        b_s = b_s[-1:]
                        smooth_nums = smooth_nums[-1:]
            
            v, alpha, a, u = get_el_of_continued_fraction(n, v, alpha, a, u)

        degree += 0.1
        
def to_factors(n: int) -> Union[Tuple[str, List[int]], str]:
    search = ''
    factors = []
    while True:
        if miller_rabin(n): return search, factors + [n]

        div = trial_division(n)
        if not div: break
        search += '   Метод пробних ділень: {}\n'.format(div)
        factors.append(div)
        n //= div

    rho_pollard_flag = False
    while True:
        div = rho_pollard(n)
        if div and not rho_pollard_flag:
            search += '   ро-метод Полларда: {}\n'.format(div)
            if n < 999999999999: rho_pollard_flag = True
            factors.append(div)
            n //= div
            if miller_rabin(n): return search, factors + [n]
            else: continue
        else:
            while True:
                div = brillhart_morrison(n)
                if div:
                    search += '   Брілхарт-Моррісон: {}'.format(div)
                    factors.append(div)
                    n //= div
                    if miller_rabin(n): return search, factors + [n]
                    else: continue
                else: return 'unsuccesful'