'''
IN eclipse: Use ctrl-F9
'''

"""
Note: for this to work with nose you have to select the nose test runner in the
preferences (window > preferences > pydev > pyunit) --
and the same is true if you're using the py.test runner
(but note that if you're using regular unittest tests, the default runner should work fine).
"""

from unnecessary_math import multiply

def test_numbers_3_4():
    assert multiply(3,4) == 12

def test_strings_a_3():
    assert multiply('a',3) == 'aaa'