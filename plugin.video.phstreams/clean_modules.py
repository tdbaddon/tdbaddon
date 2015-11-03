
import os

def gen_files(dir, pattern):
   for dirname, subdirs, files in os.walk(dir):
      for f in files:
         if f.endswith(pattern):
            yield os.path.join(dirname, f)

for f in gen_files('.', '.pyc'):
   os.remove(f)
for f in gen_files('.', '.pyo'):
   os.remove(f)
