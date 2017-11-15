# the name yax_parser stands for Yet Another XML Parser ...
import sys
from main import parse

xml_file_path = sys.argv[1]
dtd_file_path = sys.argv[2]

parse(xml_file_path, dtd_file_path)
