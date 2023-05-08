import os
import numpy as np
from itertools import chain

def get_desktop_path():
    return os.path.join(os.path.expanduser("~"), 'Desktop')

def get_one_dimensional_list(raw_list):
    return list(chain(*raw_list))
