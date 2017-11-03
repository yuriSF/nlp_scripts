from file_ops import open_file
import os
import random
import pickle

d = '../filt_all/'

def open_files(d):
    os.chdir(d)
    files = next(os.walk(os.getcwd()))[2]
    print files
    all_data = []
    for f in files:
        if '.p' not in f:
            f = os.getcwd() + '/' + f
            data = open_file(f)
            all_data.extend(data)
            print len(all_data)
    print 'all ', len(all_data)
    print 'uniq ', len(list(set(all_data)))
    return all_data

def check(data, target):
    for line in data:
        if target in line:
            print line
            
user = raw_input('search word: ')
check(open_files(d), user)
