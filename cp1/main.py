import csv
import time
import data.data as data
import factorization.factorization_methods as fm
from show.show_results import to_continue, show_factorization, show_factors

while True:
    print('Оберіть режим (для виходу з програми введіть 0)')
    print('1 - Одиничний\n2 - Автоматичний\n3 - Значення для чисел, наданих в умові КП\n')
    answer = int(input('Введіть номер відповіді: '))
    print()

    if answer == 0:
        break
    elif answer == 1:
        number = int(input('Введіть вхідне значення: '))
        print()
        if number > 1:
            print('Факторизація\n------------')
            show_factorization('Метод пробних ділень', number, fm.trial_division)
            show_factorization('ро-метод Полларда', number, fm.rho_pollard)
            show_factorization('Брілхарт-Моррісон:', number, fm.brillhart_morrison)

            print('Канонічний розклад\n------------------')
            show_factors(number)

            answer = to_continue()
            if answer == 1: continue 
            exit()
        
    elif answer == 2:
        while True:
            filename = input("Введіть ім'я файлу або Enter, якщо ім'я файлу 'cp_1_input.csv': ")
            if len(filename) == 0: filename = 'cp_1_input.csv'
            try:
                with open(filename, 'r') as csv_handle:
                    csv_reader = csv.reader(csv_handle, delimiter='\n')
                    numbers = []
                    for row in csv_reader:
                        if ''.join(row).isnumeric(): numbers.append(int(''.join(row)))
                break
            except:
                print('\nФайл ' + filename + ' не знайдено!\nСпробуйте ще раз.\n')
        
        with open('cp_1_output.csv', 'w') as csv_handle:
            csv_writer = csv.writer(csv_handle, delimiter=',')
            for number in numbers: csv_writer.writerow(fm.to_factors(number)[1])
        
        print('Розклад записано у файл "cp_1_output.csv"\n')

        answer = to_continue()
        if answer == 1: continue 
        exit()

    elif answer == 3:
        print('Факторизація\n------------')
        for number in data.nums_to_div:
            print('Число: {}\n'.format(number))
            show_factorization('ро-метод Полларда', number, fm.rho_pollard)
            show_factorization('Брілхарт-Моррісон', number, fm.brillhart_morrison)

        print('Канонічний розклад\n------------------')
        for number in data.nums_to_factorize:
            print('Число: {}\n'.format(number))
            start_time = time.time()
            search, factors = fm.to_factors(number)
            to_factors_time = time.time() - start_time
            print('{} = {}'.format(number, factors))
            print(search)
            print('Час виконання: {:.7f}\n'.format(to_factors_time))

        answer = to_continue()
        if answer == 1: continue
        exit()
    else: 
        print('Введено невірне значення!\nСпробуйте ще раз.\n')