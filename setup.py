from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import os.path
import subprocess
import sys


libpg_query = os.path.join('.', 'libpg_query')


class PSqlParseBuildExt(build_ext):

    def run(self):
        return_code = subprocess.call(['make', '-C', libpg_query, 'build'])
        if return_code:
            sys.stderr.write('''
An error occurred during extension building.
Make sure you have bison and flex installed on your system.
''')
            sys.exit(return_code)
        build_ext.run(self)


#USE_CYTHON = bool(os.environ.get('USE_CYTHON'))
USE_CYTHON=1

ext = '.pyx' if USE_CYTHON else '.c'

libraries = ['pg_query']

extensions = [
    Extension('psqlparse.parser',
              ['psqlparse/parser' + ext],
              libraries=libraries,
              include_dirs=[libpg_query],
              library_dirs=[libpg_query])
]

if USE_CYTHON:
    from Cython.Build import cythonize
    extensions = cythonize(extensions)

setup(name='psqlparse',
      version='1.0-rc7',
      url='https://github.com/alculquicondor/psqlparse',
      author='Aldo Culquicondor',
      author_email='aldo@amigocloud.com',
      description='Parse SQL queries using the PostgreSQL query parser',
      install_requires=['six', 'Cython'],
      license='BSD',
      cmdclass={'build_ext': PSqlParseBuildExt},
      packages=['psqlparse', 'psqlparse.nodes'],
      ext_modules=extensions)
