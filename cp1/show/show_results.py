import time
from typing import Callable
import factorization.factorization_methods as fm
from time_tester.time_tester import time_tester as timer

def to_continue() -> int:
    print('Бажаєте продовжити? (1 - так; усе інше - ні)')
    answer = input('Введіть номер відповіді: ')
    if answer.isnumeric(): 
        print()
        return int(answer)
    return False

def show_factorization(method_name: str, number: int, func: Callable) -> None:
    print(method_name + ': {}'.format(func(number)))
    print('Час виконання: {:.7f}\n'.format(timer(number, func)))

def show_factors(number: int) -> None:
    start_time = time.time()
    search, factors = fm.to_factors(number)
    to_factors_time = time.time() - start_time
    print('{} = {}'.format(number, factors))
    print(search)
    print('Час виконання: {:.7f}\n'.format(to_factors_time))