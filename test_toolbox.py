""" functions for the benchmarking """
import os
from main import parse
from timeit import timeit
from memory_profiler import memory_usage
import numpy as np


def getMemoryUsage(file_path, dtd_path):
    memory_measures = memory_usage((parse, (file_path, dtd_path), {'verbose': False}), include_children=True)
    return np.mean(memory_measures)


def getParseTime(file_path, dtd_path, number=10):
    parse_function = wrap(parse, file_path, dtd_path, verbose=False)
    return timeit(parse_function, number=number)


def wrap(func, *args, **kwargs):
    def wraped():
        return func(*args, **kwargs)

    return wraped


def generate_exam_xml_file(size, directory_path):
    # a person element has 10 children elements including itself
    # the size of the whole element is the size + 1 (for root)
    person_info = ['0 p', '0 n', '0 f', '1 f', '0 g', '1 g', '1 n', '0 s', '1 s', '0 l', '0 r', '1 r',
                   '0 c', '1 c', '0 o', '1 o', '0 a', '1 a', '1 l', '1 p']
    nb_persons = size // 10
    file_name = str(size + 1) + "_nodes.xml"
    file_path = os.path.join(directory_path, file_name)
    open_root = '0 d'
    close_root = '\n1 d'
    file = open(file_path, "w")
    file.write(open_root)
    for _ in range(nb_persons):
        file.write("\n" + ("\n".join(person_info)))
    file.write(close_root)
    file.close()