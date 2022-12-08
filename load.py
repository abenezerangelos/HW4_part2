import sys
from psparser import read
from psbuiltins import Stacks
from colors import *

testinput1 = """
    /x 4 def
    /g { x stack } def
    /f { /x 7 def g } def
    f
    """

testinput2 = """
    /x 4 def
    (static_y) dup 7 120 put /x exch def
    /g { x stack } def
    /f { /x (dynamic_x) def g } def
    f
    """

testinput3 = """
    /m 50 def
    /n 100 def
    /egg1 {/m 25 def n} def
    /chic
    	{ /n 1 def
	      /egg2 { (egg2) n stack} def
	      n m
	      egg1
          m
	      egg2
	    } def
    n
    chic
        """

testinput4 = """
    /x 10 def
    /A { x } def
    /C { /x 40 def A stack } def
    /B { /x 30 def /A { x 2 mul } def C } def
    B
    """

testinput5 = """
    /x 2 def
    /n 5  def
    /A { 1  n -1 1 {pop x mul} for} def
    /C { /n 3 def /x 40 def A stack } def
    /B { /x 30 def /A { x } def C } def
    B
    """

testinput6 = """
    /out true def 
    /xand { true eq {pop false} {pop true} ifelse dup /x exch def stack} def 
    /myput { out dup /x exch def xand } def 
    /f { /out false def myput } def 
    false  f
    """

testinput7 = """
    /x  1 dict def 
    x /i 22 put 
    /A { (global)  x /i get } def
    /C { /x 1 dict def x /i 33 put A stack } def
    /B { /x 1 dict def x /i 11 put /A { (function B) x /i get  } def C } def
    B
    """

testinput8 = """
    /x 1 dict def
    /a 10 def  
    /A { x /m 0 put } def
    /C { /x 1 dict def  x /m 9 put A  a x /m get stack } def
    /B { /x 1 dict def /A { x /m 99 put } def /a 5 def C } def
    B
    """
testinput9= """
/a 50 def
/b 100 def
/F1 { /b 5 def a } def
/G { /a 1 def F1 /F1 { a } def /F3 { /a 10 def F1 a stack } def a F3 } def
G
"""
testinput10 = """
/x 10 def
/func3 {/func1 { x 2 stack } def /func4 {/x 50 def func1} def func4} def
/func2 { /x 30 def func3} def
func2
"""
testinput11 = """
/V 20000 def
/D 1400 def
/F1 { /D 1 def D V stack} def
F1
"""


tests = [testinput1, testinput2, testinput3, testinput4, testinput5, testinput6, testinput7, testinput8,testinput9,testinput10,testinput11]

# program start
if __name__ == '__main__':

    psstacks_s = Stacks("static")
    psstacks_d = Stacks("dynamic")
    testnum = 1
    for testcase in tests:
        try:
            print("\n-- TEST {} --".format(testnum))
            expr_list = read(testcase)
            print("\nSTATIC")
            # interpret using static scoping rule
            for expr in expr_list:
                expr.eval(psstacks_s)
            print("\nDYNAMIC")
            # interpret using dynamic scoping rule
            for expr in expr_list:
                expr.eval(psstacks_d)
                # clear the Stack objects
        except (SyntaxError, NameError, TypeError, Exception) as err:
            print(type(err).__name__ + ':', err)
        testnum += 1
        # clear the Stack objects
        psstacks_s.clearBoth()
        psstacks_d.clearBoth()