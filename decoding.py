from main import decode_wrapper, genalphabet
from utils import MeasureTime
import sys

if __name__=='__main__':
    alpha_dict = genalphabet()
    inputpath = sys.argv[1]
    outputpath = sys.argv[2]
    decode_wrapper(inputpath=inputpath, outputpath=outputpath, alphabet=alpha_dict)
