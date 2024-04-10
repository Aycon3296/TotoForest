'''This module contains some convenient binary search functions for an element in a list'''

from bisect import bisect_left, bisect_right

__all__ = [
    'find_left_lt', 'find_left_le', 'find_left_eq', 'find_left_ge', 'find_left_gt',
    'find_right_lt', 'find_right_le', 'find_right_eq', 'find_right_ge', 'find_right_gt'
]
        
def find_left_lt(a, x, lo=0, hi=None, key=None):
    '''Finds the index of the leftmost (among duplicates) element that is strictly less than X.'''
    
    index = bisect_left(a, x, lo=lo, hi=hi, key=key)
    if len(a) > 0 and index < len(a) + 1 and a[index - 1] < x:
        return bisect_left(a, a[index - 1], lo=lo, hi=index-1, key=key)
    
    raise ValueError(f'No elements less than {x} found.')

def find_left_le(a, x, lo=0, hi=None, key=None):
    '''Finds the index of the leftmost (among duplicates) element that is less than or equal to X.'''
    
    index = bisect_right(a, x, lo=lo, hi=hi, key=key)
    if len(a) > 0 and index < len(a) + 1 and a[index - 1] <= x:
        return bisect_left(a, a[index - 1], lo=lo, hi=index-1, key=key)
    
    raise ValueError(f'No elements less than or equal to {x} found.')

def find_left_eq(a, x, lo=0, hi=None, key=None):
    '''Finds the index of the leftmost (among duplicates) element that is equal to X.'''
    
    index = bisect_left(a, x, lo=lo, hi=hi, key=key)
    if index != len(a) and a[index] == x:
        return index
    
    raise ValueError(f'No elements equal to {x} found.')

def find_left_ge(a, x, lo=0, hi=None, key=None):
    '''Finds the index of the leftmost (among duplicates) element that is greater than or equal to X.'''
    
    index = bisect_left(a, x, lo=lo, hi=hi, key=key)
    if index != len(a):
        return index
    
    raise ValueError(f'No elements greater than or equal to {x} found.')

def find_left_gt(a, x, lo=0, hi=None, key=None):
    '''Finds the index of the leftmost (among duplicates) element that is strictly greater than X.'''
    
    index = bisect_right(a, x, lo=lo, hi=hi, key=key)
    if index != len(a):
        return index
    
    raise ValueError(f'No elements greater than {x} found.')

def find_right_lt(a, x, lo=0, hi=None, key=None):
    '''Finds the index of the rightmost (among duplicates) element that is strictly less than X.'''
    
    index = bisect_left(a, x, lo=lo, hi=hi, key=key)
    if index:
        return index-1
    
    raise ValueError(f'No elements less than {x} found.')

def find_right_le(a, x, lo=0, hi=None, key=None):
    '''Finds the index of the rightmost (among duplicates) element that is less than or equal to X.'''
    
    index = bisect_right(a, x, lo=lo, hi=hi, key=key)
    if index:
        return index-1
    
    raise ValueError(f'No elements less than or equal to {x} found.')

def find_right_eq(a, x, lo=0, hi=None, key=None):
    '''Finds the index of the rightmost (among duplicates) element that is equal to X.'''
    
    index = bisect_left(a, x, lo=lo, hi=hi, key=key)
    if index != len(a) and a[index] == x:
        return bisect_right(a, a[index], lo=index, hi=hi, key=key) - 1
    
    raise ValueError(f'No elements equal to {x} found.')

def find_right_ge(a, x, lo=0, hi=None, key=None):
    '''Finds the index of the rightmost (among duplicates) element that is greater than or equal to X.'''
    
    index = bisect_left(a, x, lo=lo, hi=hi, key=key)
    if index != len(a):
        return bisect_right(a, a[index], lo=index, hi=hi, key=key) - 1
    
    raise ValueError(f'No elements greater than or equal to {x} found.')

def find_right_gt(a, x, lo=0, hi=None, key=None):
    '''Finds the index of the rightmost (among duplicates) element that is strictly greater than X.'''
    
    index = bisect_right(a, x, lo=lo, hi=hi, key=key)
    if index != len(a):
        return bisect_right(a, a[index], lo=index, hi=hi, key=key) - 1

    raise ValueError(f'No elements greater than {x} found.')
```
