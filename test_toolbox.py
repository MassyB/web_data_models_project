""" functions for the benchmarking """
from time import time
import os
from main import parse


def getParseTime(file_path, dtd_path):
    t1 = time()
    parse(file_path, dtd_path, verbose=False)
    t2 = time()
    return t2 - t1


def generate_exam_xml_file(size):
    # a person element has 10 children elements including itself
    # the size of the whole element is the size + 1 (for root)
    person_info = ['0 p', '0 n', '0 f', '1 f', '0 g', '1 g', '1 n', '0 s', '1 s', '0 l', '0 r', '1 r',
                   '0 c', '1 c', '0 o', '1 o', '0 a', '1 a', '1 l', '1 p']
    nb_persons = size // 10
    directory_path = "test_files"
    file_name = str(size + 1) + "_nodes.xml"
    file_path = os.path.join(directory_path, file_name)
    open_root = '0 d'
    close_root = '\n1 d'
    file = open(file_path, "w")
    file.write(open_root)
    for _ in range(nb_persons):
        file.write("\n"+("\n".join(person_info)))
    file.write(close_root)
    file.close()
