from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import sys
import setuptools
class get_pybind_include(object):
    # Helper class to determine the pybind11 include path.
    def __str__(self):
        import pybind11
        return pybind11.get_include()
ext_modules = [
    Extension(
        'your_module_name',  # Name of the module.
        ['your_module.cpp'],  # C++ source files.
        include_dirs=[
            get_pybind_include(),  # Path to pybind11 includes.
            '/path/to/other/includes',  # Additional include paths.
        ],
        language='c++'
    ),
]

setup(
    name='your_module_name',
    version='0.1',
    author='Sara Serafino',
    author_email='serafinos1999@gmail.com',
    description='A Python module using pybind11',
    long_description='',
    ext_modules=ext_modules,
    install_requires=['pybind11>=2.5.0'],  # pybind11 requirement.
    cmdclass={'build_ext': build_ext},
    zip_safe=False,
)