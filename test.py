import os
import spc

tfile = 0
tpass = 0

dpath = os.path.join(os.path.dirname(__file__), 'test_data')
mfile = []
rfile = []
lfile = []
for i in os.listdir(dpath):
    if i[-3:].lower() == 'spc':
        try:
            tfile += 1
            f1 = spc.File(os.path.join(dpath, i))
            try:
                outfile = os.path.join(dpath, 'txt', i + '.txt')
                with open(outfile, 'r') as fin:
                    dat = fin.read()
                    if f1.data_txt() == dat:
                        print "-->Pass"
                        tpass += 1
                    else:
                        print "-->Fail"
                        mfile.append(i)
            except:
                print "--Failed reading reference data %s " % outfile
                rfile.append(i)
        except:
            print "-->Failed loading file: %s" % i
            lfile.append(i)
print "Passed %i of %i tests. " % (tpass, tfile)
print "Did not match ref file: ", mfile
print "Did not have ref file: ", rfile
print "Did not load file: ", lfile
