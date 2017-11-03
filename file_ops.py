import csv
import codecs

def open_file(file_name):
    with open(file_name, 'rb') as f:
        data = f.readlines()
    return data


def read_file(file_name):
    f = codecs.open(file_name, 'r', 'iso-8859-15')
    data = f.read()
    return data

def open_csv(f):
    with open(f, 'rU') as f:
        reader = csv.reader(f)
        temp = [row for row in reader]
        return temp

def write_csv_row(f, row):
    with open(f, 'a') as csvfile:
        csv.writer(csvfile).writerow(row)

def write_csv_rows(f, rows):
    with open(f, 'wb') as csvfile:
        csv.writer(csvfile).writerows(rows)

def get_fnames(d):
    import os
    os.chdir(d)
    fnames = next(os.walk(os.getcwd()))[2]
    return fnames

def read_files(absolute, extension):
    fnames = get_fnames(absolute)
    all_data = []
    for f in fnames:
        if f.split('.')[-1] == extension:
            data = open_file(f)
            all_data.extend(data)
    return all_data

def read_files_string(absolute, extension):
    fnames = get_fnames(absolute)
    all_data = ''
    for f in fnames:
        if f.split('.')[-1] == extension:
            data = read_file(f)
            all_data = all_data + data
    return all_data

def write_freq_to_text(freq_dist):
    verb_file = raw_input('File to save verb frequency: ')
    target_dir = raw_input('Path to directory to save file: ')
    os.chdir(target_dir)
    for item in freq_dist:
        with open(verb_file, 'a') as f:
            line = '{0}: {1}\n'.format(item[0], item[1])
            f.write(line)
    return "Saved"
