# -*- coding: iso-8859-1 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Zip Tools
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------
import zipfile
import os
import os.path

class ziptools:
    def extract(self, file, dir):

        if not dir.endswith(':') and not os.path.exists(dir):
            os.mkdir(dir)

        zf = zipfile.ZipFile(file)
        self._createstructure(file, dir)
        num_files = len(zf.namelist())

        for name in zf.namelist():
            if not name.endswith('/'):
                content = zf.read(name)
                name = name.replace('-master', '')
                try:
                    (path, filename) = os.path.split(os.path.join(dir, name))
                    os.makedirs(path)
                except:
                    pass
                outfilename = os.path.join(dir, name)
                try:
                    outfile = open(outfilename, 'wb')
                    outfile.write(content)
                except:
                    pass

    def _createstructure(self, file, dir):
        self._makedirs(self._listdirs(file), dir)

    def _makedirs(self, directories, basedir):
        for dir in directories:
            curdir = os.path.join(basedir, dir)
            if not os.path.exists(curdir):
                os.mkdir(curdir)

    def _listdirs(self, file):
        zf = zipfile.ZipFile(file)
        dirs = []
        for name in zf.namelist():
            if name.endswith('/'):
                dirs.append(name.replace('-master', ''))

        dirs.sort()
        return dirs


