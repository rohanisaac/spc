import os #, sys
#sys.path.append('spc')
import spc

tfile = 0
tpass = 0

dpath = os.path.join(os.getcwd(), 'spc', 'test_data')
for i in os.listdir(dpath):
    tfile += 1
    try:
        f1 = spc.File(os.path.join(dpath, i))
        try:
            outfile = os.path.join(dpath, 'csv', i[:-4] + '.csv')
            with open(outfile, 'r') as fin:
                dat = fin.read()
                if f1.data_txt() == dat:
                    print "-->Pass"
                    tpass += 1
                else:
                    print "-->Fail"
        except:
            print "--Fail"
    except:
        print "-->Fail"
print "Passed %i of %i tests " % (tpass, tfile)
