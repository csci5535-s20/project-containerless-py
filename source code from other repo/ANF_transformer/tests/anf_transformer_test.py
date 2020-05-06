import ast
import astor

from ANF_transformer.transformer import normalize_to_ANF

def test_normalize_to_ANF():
    source_strings = []
    result_strings = []
    #test to see if variables are reinitilized correctly
    source_strings.append(
"""
c=5
def test():
	c = 5
	a=5
	if a == 5:
		b = 5
d=12
d += 12
"""
    )
    result_strings.append(
"""c = None
d = None
c = 5


def test():
    a = None
    b = None
    c = 5
    a = 5
    if a == 5:
        b = 5


d = 12
d += 12
"""
    )

    #test to see that for loops are converted to while loops correctly
    source_strings.append(
"""
def func():
    y = []
    x = [1, 2, 3]
    for index in range(len(x)):
        y[index] = x[index]
    return y
"""
    )
    result_strings.append(
"""def func():
    y = None
    loop_index0 = None
    x = None
    index = None
    y = []
    loop_index0 = 0
    x = [1, 2, 3]
    while loop_index0 < len(range(len(x))):
        index = range(len(x))[loop_index0]
        y[index] = x[index]
        loop_index0 += 1
    return y
"""
    )
    #test for naming applications
    source_strings.append(
"""
def func():
    def func1():
        if True:
            func()
    func1()
func()
"""
    )
    result_strings.append(
"""app0 = None


def func():
    app1 = None

    def func1():
        app2 = None
        if True:
            app2 = func()
    app1 = func1()


app0 = func()
"""
    )

    for source_string, result_string in zip(source_strings, result_strings):
        assert(normalize_to_ANF(source_string=source_string) == result_string)
