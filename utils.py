import numpy as np

def byte_reader(path):
    '''
    Args:
        path - string
    Return:
    '''
    with open(path, 'rb') as f: return f.read()

def txt_reader(path):
    '''
    Args:
        path - string
    Return:
    '''
    with open(path, 'r') as f: return f.read()
