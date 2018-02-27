import utils
import glob
import os


dir = '../../Data/'
session_threshold = 10000

for fullname in glob.iglob(dir + '*.pcap'):
    dir_n, filename = os.path.split(fullname)
    print('Currently saving file: ', filename)
    utils.save_pcap(dir, filename, session_threshold)


