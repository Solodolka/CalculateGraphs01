import os

nuc_num = 2
tables_path = 'tables'
repeats_path = 'repeats'
results_path = 'results'
table = {}
shifts_num = 30
aver_beg_values = [0] * shifts_num
aver_end_values = [0] * shifts_num
run_number = 1


def read_table():  #Загрузка таблицы 'AA...' - 3.14
    filepath = os.path.join(tables_path, 'nuc_table_' + str(nuc_num) + '.txt')
    with open(filepath, 'r', encoding='utf-8') as f:
        # Читаем файл построчно
        for line in f:
            str_lst = line.split('\t')
            table[str_lst[0]] = float(str_lst[1])

def read_and_process_repeats(directory): # Перебор всех файлов с репитами
    global run_number
    # Получаем список всех файлов в заданной директории
    files = os.listdir(directory)
    for file in files:
        filepath = os.path.join(directory, file)
        with open(filepath, 'r', encoding='utf-8') as f:
            # print(f'File {file}:')
            # Читаем файл построчно
            score = 0
            for line_number, line in enumerate(f, start=1):
                if (line_number % 2 == 1):
                    str_lst = line.split('\t')
                    str_lst = str_lst[2].split(' ')
                    score = float(str_lst[1])  # Читаем скор из нечетной строчки
                else:
                    if (score > 4.2): # Если скор больше порога, обрабатываем репит
                        process_repeat_beg(line)  # Обрабатываем начало
                        process_repeat_end(line)  # Обрабатываем конец
                        run_number += 1

def process_repeat_beg(repeat):   # Обрабатываем начало
    global shifts_num, run_number, aver_beg_values
    values = []
    key = repeat[:nuc_num]
    for i in range(0, shifts_num):
        values.append(table[key])
        key = key[1:] + repeat[nuc_num + i]
    write_results( values, '_beg')

    # calc average value for each position
    coeff0 = (run_number-1)/run_number
    coeff1 = 1/run_number
    for i, v in enumerate(values, start=0):
        aver_beg_values[i] = coeff0 * aver_beg_values[i] + coeff1 * v
    print (values)

def process_repeat_end(repeat):   # Обрабатываем конец
    global shifts_num, run_number, aver_end_values
    values = []
    key = repeat[-(shifts_num + 1 + nuc_num):- (shifts_num + 1)]
    rep_len = len(repeat)
    for i in range(0, shifts_num):
        values.append(table[key])
        key = key[1:] + repeat[(rep_len - shifts_num - 1) + i]
    write_results( values, '_end')

    # calc average value for each position
    coeff0 = (run_number-1)/run_number
    coeff1 = 1/run_number
    for i, v in enumerate(values, start=0):
        aver_end_values[i] = coeff0 * aver_end_values[i] + coeff1 * v
    print (values)

def write_results(values, pref = ''):
    filepath = os.path.join(results_path, 'result_' + str(nuc_num) + pref + '.txt')
    with open(filepath, 'a', encoding='utf-8') as f:
        for v in values:
            v_str = f"{v:.8f}"
            v_str = v_str.replace('.', ',') # FOR RUSSIAN Excel
            f.write(v_str + '\t')
        f.write('\n')


read_table()
read_and_process_repeats(repeats_path)
write_results(aver_beg_values, '_beg')
write_results(aver_end_values, '_end')
print(aver_beg_values)
print(aver_end_values)
