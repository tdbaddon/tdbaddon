import zipfile

def all(_in, _out, dialogprocess=None):
    if dialogprocess:
        return allWithProgress(_in, _out, dialogprocess)

    return allNoProgress(_in, _out)
        

def allNoProgress(_in, _out):
    try:
        zin = zipfile.ZipFile(_in, 'r')
        zin.extractall(_out)
    except Exception, e:
        print str(e)
        return False

    return True


def allWithProgress(_in, _out, dialogprocess):

    zin = zipfile.ZipFile(_in,  'r')

    nFiles = float(len(zin.infolist()))
    count  = 0

    try:
        for item in zin.infolist():
            count += 1
            update = count / nFiles * 100
            dialogprocess.update(int(update))
            zin.extract(item, _out)
    except Exception, e:
        print str(e)
        return False

    return True