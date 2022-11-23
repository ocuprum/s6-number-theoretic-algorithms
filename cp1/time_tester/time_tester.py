import time
from typing import Callable, Union, List

def time_tester(n: int, func_to_test: Union[Callable[[int, int], Union[int, bool]], Callable[[int, int, int, Callable[[int], int]], Union[int, bool]], Callable[[int, float], int], Callable[[int], Union[str, List[int]]]]) -> float:  
    start_time = time.time()
    func_to_test(n)
    result = time.time() - start_time
    return result
