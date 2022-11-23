from typing import List, Dict, Tuple
from factorization.factorization_methods import horner_pow, to_factors, inversed_element, gcd

# Обчислення канонічного розкладу числа
def canonical_form(n: int) -> Dict[int, int]:
    factors = to_factors(n)[1]
    if factors == 'unsuccesful': return factors
    canonical_form = {}
    for factor in factors: 
        canonical_form[factor] = canonical_form.get(factor, 0) + 1
    return canonical_form

# Побудова таблиць для кожного простого числа у розкладі
def build_tables(generator: int, order: int, module: int, canonical: Dict[int, int]) -> Dict[int, Dict[int, int]]:
    table = {}
    for prime in canonical.keys():
        table[prime] = {}
        pow = order // prime
        for j in range(prime):
            table[prime][j] = horner_pow(generator, pow * j, module)
    return table

# Визначення рівняння конґруенції 
def find_equation(prime: int, power: int, generator: int, beta: int, order: int, module: int, tables: Dict[int, Dict[int, int]]) -> List[int]:
    x, div = 0, 1
    for _ in range(power):
        temp = horner_pow(beta * inversed_element(horner_pow(generator, x, module), module), order // (div * prime), module)
        for j, value in tables[prime].items():
            if value == temp  or value == (- module + temp): 
                x += j * div
                div *= prime
                break
    return x, div

# Побудова системи конґруенцій з отриманих рівнянь
def define_congruence_system(generator: int, beta:int, order: int, module: int, canonical: Dict[int, int], tables: Dict[int, Dict[int, int]]) -> List[Tuple[int, int]]:
    system = []
    for prime, power in canonical.items():
        system.append(find_equation(prime, power, generator, beta, order, module, tables))
    return system

def is_coprime(nums: List[int]) -> bool:
    for i in range(len(nums)):
        for j in range(i+1, len(nums)):
            if gcd(nums[i], nums[j]) != 1: return False
    return True
            
def solve_congruence_system(system: List[Tuple[int, int]]) -> int:
    xs = [xi for xi, _ in system]
    mods = [mod for _, mod in system]
    if not is_coprime(mods): return 'unsuccesful'

    M = 1
    for mod in mods:
        M *= mod
    
    Ms = {mod: M // mod for mod in mods}
    Ns = [inversed_element(Ms[mod] % mod, mod) for mod in mods]

    x = 0
    for i in range(len(mods)):
        x += xs[i] * Ms[mods[i]] * Ns[i]
    return x % M

def silver_pohlig_hellman(generator: int, beta: int, order: int, module: int) -> int:
    canonical = canonical_form(order)
    if canonical == 'unsuccesful': return canonical
    tables = build_tables(generator, order, module, canonical)
    system = define_congruence_system(generator, beta, order, module, canonical, tables)
    x = solve_congruence_system(system)
    return x