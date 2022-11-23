import csv
import time
from sph_method.sph_method import silver_pohlig_hellman

def to_continue() -> int:
    print('Бажаєте продовжити? (1 - так; усе інше - ні)')
    answer = input('Введіть номер відповіді: ')
    if answer.isnumeric(): 
        print()
        return int(answer)
    return False

while True:
    print('Оберіть режим (для виходу з програми введіть 0)')
    print('1 - Одиничний\n2 - Автоматичний\n')
    answer = int(input('Введіть номер відповіді: '))
    print()

    if answer == 0:
        break
    elif answer == 1:
        inp = input('Введіть вхідні значення (генератор, бета, порядок групи) через пробіл: ')
        generator, beta, p = (int(num) for num in inp.split())
        print()
        if generator < p and beta < p:
            print('Задача: {}^x = {} mod {}'.format(generator, beta, p))
            start_time = time.time()
            result = silver_pohlig_hellman(generator, beta, p-1, p)
            worktime = time.time() - start_time
            print('x -> {}'.format(result))
            print('Час виконання: {}'.format(worktime))
            print()

            answer = to_continue()
            if answer == 1: continue 
            exit()
        
    elif answer == 2:
        while True:
            filename = input("Введіть ім'я файлу або Enter, якщо ім'я файлу 'cp_2_input.csv': ")
            if len(filename) == 0: filename = 'cp_2_input.csv'
            try:
                with open(filename, 'r') as csv_handle:
                    csv_reader = csv.reader(csv_handle, delimiter='\n')
                    problems = []
                    for row in csv_reader:
                        problem = row[0].split(',')
                        problems.append(problem)
                    problems = problems[1:]
                break
            except:
                print('\nФайл ' + filename + ' не знайдено!\nСпробуйте ще раз.\n')
        
        with open('cp_2_output.csv', 'w') as csv_handle:
            csv_writer = csv.writer(csv_handle, delimiter=',')
            for problem in problems: 
                generator, beta, p = int(problem[0]), int(problem[1]), int(problem[2])
                csv_writer.writerow([silver_pohlig_hellman(generator, beta, p-1, p)])
        
        print('Розклад записано у файл "cp_2_output.csv"\n')

        answer = to_continue()
        if answer == 1: continue 
        exit()

    else: 
        print('Введено невірне значення!\nСпробуйте ще раз.\n')
