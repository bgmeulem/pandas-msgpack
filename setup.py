#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from setuptools import setup
import importlib.resources, importlib.metadata
from distutils.extension import Extension
from distutils.command.build_ext import build_ext as build_ext

NAME = 'pandas-msgpack'

def is_platform_windows():
    return sys.platform == 'win32' or sys.platform == 'cygwin'

def is_platform_linux():
    return sys.platform == 'linux2'

def is_platform_mac():
    return sys.platform == 'darwin'

try:
    import Cython
    from Cython.Build import cythonize
except ImportError:
    raise ImportError("cython is required for building")

# args to ignore warnings
if is_platform_windows():
    extra_compile_args=[]
else:
    extra_compile_args=['-Wno-unused-function']


if sys.byteorder == 'big':
    macros = [('__BIG_ENDIAN__', '1')]
else:
    macros = [('__LITTLE_ENDIAN__', '1')]

extensions = []
packer_ext = Extension('isf_pandas_msgpack.msgpack._packer',
                        depends=['isf_pandas_msgpack/includes/pack.h',
                                 'isf_pandas_msgpack/includes/pack_template.h'],
                        sources = ['isf_pandas_msgpack/msgpack/_packer.pyx'],
                        language='c++',
                        include_dirs=['pandas_msgack/includes'],
                        define_macros=macros,
                        extra_compile_args=extra_compile_args)
unpacker_ext = Extension('isf_pandas_msgpack.msgpack._unpacker',
                        depends=['isf_pandas_msgpack/includes/unpack.h',
                                 'isf_pandas_msgpack/includes/unpack_define.h',
                                 'isf_pandas_msgpack/includes/unpack_template.h'],
                        sources = ['isf_pandas_msgpack/msgpack/_unpacker.pyx'],
                         language='c++',
                        include_dirs=['isf_pandas_msgpack/includes'],
                        define_macros=macros,
                        extra_compile_args=extra_compile_args)
extensions.append(packer_ext)
extensions.append(unpacker_ext)

#----------------------------------------------------------------------
# util
# extension for pseudo-safely moving bytes into mutable buffers
_move_ext = Extension('isf_pandas_msgpack._move',
                      depends=[],
                      sources=['isf_pandas_msgpack/move.c'])
extensions.append(_move_ext)

setup(
    name=NAME,
    description="Pandas interface to msgpack",
    ext_modules=cythonize(extensions),
    packages=['isf_pandas_msgpack',
              'isf_pandas_msgpack.includes',
              'isf_pandas_msgpack.msgpack',
              'isf_pandas_msgpack.tests'],
)
