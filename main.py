import os

nuc_num = 4
tables_path = 'tables'
repeats_path = 'repeats'
results_path = 'results'
table = {}

def read_table():
    filepath = os.path.join(tables_path, 'nuc_table_' + str(nuc_num) + '.txt')
    with open(filepath, 'r', encoding='utf-8') as f:
        # Читаем файл построчно
        for line in f:
            str_lst = line.split('\t')
            table[str_lst[0]] = float(str_lst[1])

def read_repeats(directory):
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
                    score = float(str_lst[1])
                else:
                    if (score > 4.2):
                        process_repeat(line)


shifts_num = 30
aver_values = [0] * shifts_num
run_number = 1

def write_results(values):
    filepath = os.path.join(results_path, 'result_' + str(nuc_num) + '.txt')
    with open(filepath, 'a', encoding='utf-8') as f:
        for v in values:
            v_str = f"{v:.8f}"
            v_str = v_str.replace('.', ',') # FOR RUSSIAN Excel
            f.write(v_str + '\t')
        f.write('\n')

def process_repeat(repeat):
    global shifts_num, run_number, aver_values
    values = []
    key = repeat[:nuc_num]
    for i in range(0, shifts_num):
        values.append(table[key])
        key = key[1:] + repeat[nuc_num+i]

    write_results(values)

    # calc average value for each position
    coeff0 = (run_number-1)/run_number
    coeff1 = 1/run_number
    for i, v in enumerate(values, start=0):
        aver_values[i] = coeff0 * aver_values[i] + coeff1 * v
    print (values)
    run_number += 1

read_table()
read_repeats(repeats_path)
write_results(aver_values)
print(aver_values)
