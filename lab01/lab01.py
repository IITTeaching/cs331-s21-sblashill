import unittest
import sys
from contextlib import contextmanager
from io import StringIO

#################################################################################
# TESTING OUTPUTS
#################################################################################
@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err

#################################################################################
# EXERCISE 1
#################################################################################

# implement this function
def is_perfect(n):
    fac = [1]
    sum1 = 0
    posFac = list(range(2,n))
    for x in posFac:
        if float(n/x).is_integer():
            fac.append(x)
    for y in fac:
        sum1 += y
    if n == 1:
        return False
    if sum1 == n:
        return True
    else:
        return False

# (3 points)
def test1():
    tc = unittest.TestCase()
    for n in (6, 28, 496):
        tc.assertTrue(is_perfect(n), '{} should be perfect'.format(n))
    for n in (1, 2, 3, 4, 5, 10, 20):
        tc.assertFalse(is_perfect(n), '{} should not be perfect'.format(n))
    for n in range(30, 450):
        tc.assertFalse(is_perfect(n), '{} should not be perfect'.format(n))

#################################################################################
# EXERCISE 2
#################################################################################

# implement this function
def multiples_of_3_and_5(n):
    msum = 0
    for i in range(1,n):
        if  i%3 == 0 or i%5 == 0:
            msum += i
    return msum
# (3 points)
def test2():
    tc = unittest.TestCase()
    tc.assertEqual(multiples_of_3_and_5(10), 23)
    tc.assertEqual(multiples_of_3_and_5(500), 57918)
    tc.assertEqual(multiples_of_3_and_5(1000), 233168)

#################################################################################
# EXERCISE 3
#################################################################################
def integer_right_triangles(p):
    output = list()
    msum = 0
    for a in range(1,p):
        for b in range(1,p):
            c = p - (a + b)
            if a**2 + b**2 == c**2 and a+b+c == p:
                output.append((a,b,c))
                msum += 1
    return msum/2
def test3():
    tc = unittest.TestCase()
    tc.assertEqual(integer_right_triangles(60), 2)
    tc.assertEqual(integer_right_triangles(100), 0)
    tc.assertEqual(integer_right_triangles(180), 3)

#################################################################################
# EXERCISE 4
#################################################################################

# implement this function
def gen_pattern(chars):
    l = len(chars)
    lg = len(chars)*2-1
    lg1 =  (len(chars)*2-1)*2-1
    tstr1 = ""
    tstr2 = ""
    asc = ""
    tasc = ""
    for y in range(lg):
        tasc = ""
        tstr1 = ""
        tstr2 = ""
        if y < l:
            for x in range(y):
                tstr1 += chars[l-y+x]
                tstr2 += chars[l-x-1]
            tasc = "".join((tstr2,chars[l-y-1],tstr1))
            tasc = ".".join(tasc)
        else:
            for x in range(lg-y -1):
                tstr1 += chars[l-lg+y+x+1]
                tstr2 += chars[l-x-1]
            tasc = "".join((tstr2,chars[l+y-lg],tstr1))
            tasc = ".".join(tasc)
        while len(tasc) < lg1:
            tasc = "".join((".",tasc))
            tasc = "".join((tasc,"."))
        asc += tasc
        asc += "\n"
    print(asc)

def test4():
    tc = unittest.TestCase()
    with captured_output() as (out,err):
        gen_pattern('@')
        tc.assertEqual(out.getvalue().strip(), '@')
    with captured_output() as (out,err):
        gen_pattern('@%')
        tc.assertEqual(out.getvalue().strip(),
        """
..%..
%.@.%
..%..
""".strip())
    with captured_output() as (out,err):
        gen_pattern('ABC')
        tc.assertEqual(out.getvalue().strip(),
        """
....C....
..C.B.C..
C.B.A.B.C
..C.B.C..
....C....
""".strip())
    with captured_output() as (out,err):
        gen_pattern('#####')
        tc.assertEqual(out.getvalue().strip(),
                             """
........#........
......#.#.#......
....#.#.#.#.#....
..#.#.#.#.#.#.#..
#.#.#.#.#.#.#.#.#
..#.#.#.#.#.#.#..
....#.#.#.#.#....
......#.#.#......
........#........
""".strip())
    with captured_output() as (out,err):
        gen_pattern('abcdefghijklmnop')
        tc.assertEqual(out.getvalue().strip(),
"""
..............................p..............................
............................p.o.p............................
..........................p.o.n.o.p..........................
........................p.o.n.m.n.o.p........................
......................p.o.n.m.l.m.n.o.p......................
....................p.o.n.m.l.k.l.m.n.o.p....................
..................p.o.n.m.l.k.j.k.l.m.n.o.p..................
................p.o.n.m.l.k.j.i.j.k.l.m.n.o.p................
..............p.o.n.m.l.k.j.i.h.i.j.k.l.m.n.o.p..............
............p.o.n.m.l.k.j.i.h.g.h.i.j.k.l.m.n.o.p............
..........p.o.n.m.l.k.j.i.h.g.f.g.h.i.j.k.l.m.n.o.p..........
........p.o.n.m.l.k.j.i.h.g.f.e.f.g.h.i.j.k.l.m.n.o.p........
......p.o.n.m.l.k.j.i.h.g.f.e.d.e.f.g.h.i.j.k.l.m.n.o.p......
....p.o.n.m.l.k.j.i.h.g.f.e.d.c.d.e.f.g.h.i.j.k.l.m.n.o.p....
..p.o.n.m.l.k.j.i.h.g.f.e.d.c.b.c.d.e.f.g.h.i.j.k.l.m.n.o.p..
p.o.n.m.l.k.j.i.h.g.f.e.d.c.b.a.b.c.d.e.f.g.h.i.j.k.l.m.n.o.p
..p.o.n.m.l.k.j.i.h.g.f.e.d.c.b.c.d.e.f.g.h.i.j.k.l.m.n.o.p..
....p.o.n.m.l.k.j.i.h.g.f.e.d.c.d.e.f.g.h.i.j.k.l.m.n.o.p....
......p.o.n.m.l.k.j.i.h.g.f.e.d.e.f.g.h.i.j.k.l.m.n.o.p......
........p.o.n.m.l.k.j.i.h.g.f.e.f.g.h.i.j.k.l.m.n.o.p........
..........p.o.n.m.l.k.j.i.h.g.f.g.h.i.j.k.l.m.n.o.p..........
............p.o.n.m.l.k.j.i.h.g.h.i.j.k.l.m.n.o.p............
..............p.o.n.m.l.k.j.i.h.i.j.k.l.m.n.o.p..............
................p.o.n.m.l.k.j.i.j.k.l.m.n.o.p................
..................p.o.n.m.l.k.j.k.l.m.n.o.p..................
....................p.o.n.m.l.k.l.m.n.o.p....................
......................p.o.n.m.l.m.n.o.p......................
........................p.o.n.m.n.o.p........................
..........................p.o.n.o.p..........................
............................p.o.p............................
..............................p..............................
""".strip()
)

#################################################################################
# RUN ALL TESTS
#################################################################################
def main():
   ## test1()
   ## test2()
   ## test3()
    test4()

if __name__ == '__main__':
    main()
