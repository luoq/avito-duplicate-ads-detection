import os
from util import with_cache

dir_here = os.path.dirname(os.path.realpath(__file__))
data_file_dir = os.path.join(dir_here, 'data_files')
cache_dir = os.path.join(dir_here, 'cache')

def get_data_file(p):
    return os.path.join(data_file_dir, p)

def get_cache_file(p):
    return os.path.join(cache_dir, p)

def generate_with_cache(name, g):
    return with_cache(os.path.join(cache_dir, name + '.pickle'), g)


def load_file_with_cache(name, reader, f):
    return with_cache(os.path.join(cache_dir, name + '.pickle'),
                      lambda: reader(os.path.join(data_file_dir, f)))