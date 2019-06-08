#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pytest
import os
import sys

@pytest.fixture(scope='function')
def fixtrue_function():
    a = 10
    b = 10
    print('++++ fixtrue_function start to run...')
    return a + b

@pytest.fixture(scope='module')
def fixtrue_module():
    print('++++ fixtrue_module start to run...')

@pytest.fixture(scope='class')
def fixtrue_class():
    print('++++ fixtrue_class start to run...')


def test_function_1(fixtrue_function, fixtrue_module, fixtrue_class):
    print('>>> test_function_1 run1')
    ret = fixtrue_function
    print('>>> test_function_1 run2: %d' % ret)
    assert 1 == 2


def test_function_2(fixtrue_function, fixtrue_module, fixtrue_class):
    print('>>> test_function_2 run1')
    ret = fixtrue_function
    print('>>> test_function_2 run2: %d' % ret)
    assert 1 == 2
