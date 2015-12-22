import os #, sys
#sys.path.append('spc')
import spc

for i in os.listdir(os.path.join(os.getcwd(), 'spc', 'test_data')):
    print i
