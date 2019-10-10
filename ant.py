# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Created on Wed Oct  9 10:48:07 2019

URL: https://github.com/278Mt/taniguchi/blob/master/ant.py
@author: n_toba
"""
from socket import gethostname as gh
if 'ouka' not in gh(): raise ImportError('someting wrong')


if __name__ == '__main__':

    print('succeed!!')
