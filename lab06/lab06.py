from unittest import TestCase


################################################################################
# STACK IMPLEMENTATION (DO NOT MODIFY THIS CODE)
################################################################################
class Stack:
    class Node:
        def __init__(self, val, next=None):
            self.val = val
            self.next  = next

    def __init__(self):
        self.top = None

    def push(self, val):
        self.top = Stack.Node(val, self.top)

    def pop(self):
        assert self.top, 'Stack is empty'
        val = self.top.val
        self.top = self.top.next
        return val

    def peek(self):
        return self.top.val if self.top else None

    def empty(self):
        return self.top == None

    def __bool__(self):
        return not self.empty()

    def __repr__(self):
        if not self.top:
            return ''
        return '--> ' + ', '.join(str(x) for x in self)

    def __iter__(self):
        n = self.top
        while n:
            yield n.val
            n = n.next

################################################################################
# CHECK DELIMITERS
################################################################################
def check_delimiters(expr):
    """Returns True if and only if `expr` contains only correctly matched delimiters, else returns False."""
    delim_openers = '{([<'
    delim_closers = '})]>'

    ### BEGIN SOLUTION
    s = Stack()
    x = Stack()
    for c in expr:
        if c in delim_openers:
            x.push(delim_openers.index(c))
            s.push(c)
        if c in delim_closers and s.empty():
            return False
        if c in delim_closers:
            if x.pop() != delim_closers.index(c):
                return False
            s.pop()
    return s.empty()
    ### END SOLUTION

################################################################################
# CHECK DELIMITERS - TEST CASES
################################################################################
# points: 5
def test_check_delimiters_1():
    tc = TestCase()
    tc.assertTrue(check_delimiters('()'))
    tc.assertTrue(check_delimiters('[]'))
    tc.assertTrue(check_delimiters('{}'))
    tc.assertTrue(check_delimiters('<>'))

# points:5
def test_check_delimiters_2():
    tc = TestCase()
    tc.assertTrue(check_delimiters('([])'))
    tc.assertTrue(check_delimiters('[{}]'))
    tc.assertTrue(check_delimiters('{<()>}'))
    tc.assertTrue(check_delimiters('<({[]})>'))

# points: 5
def test_check_delimiters_3():
    tc = TestCase()
    tc.assertTrue(check_delimiters('([] () <> [])'))
    tc.assertTrue(check_delimiters('[{()} [] (<> <>) {}]'))
    tc.assertTrue(check_delimiters('{} <> () []'))
    tc.assertTrue(check_delimiters('<> ([] <()>) <[] [] <> <>>'))

# points: 5
def test_check_delimiters_4():
    tc = TestCase()
    tc.assertFalse(check_delimiters('('))
    tc.assertFalse(check_delimiters('['))
    tc.assertFalse(check_delimiters('{'))
    tc.assertFalse(check_delimiters('<'))
    tc.assertFalse(check_delimiters(')'))
    tc.assertFalse(check_delimiters(']'))
    tc.assertFalse(check_delimiters('}'))
    tc.assertFalse(check_delimiters('>'))

# points: 5
def test_check_delimiters_5():
    tc = TestCase()
    tc.assertFalse(check_delimiters('( ]'))
    tc.assertFalse(check_delimiters('[ )'))
    tc.assertFalse(check_delimiters('{ >'))
    tc.assertFalse(check_delimiters('< )'))

# points: 5
def test_check_delimiters_6():
    tc = TestCase()
    tc.assertFalse(check_delimiters('[ ( ] )'))
    tc.assertFalse(check_delimiters('((((((( ))))))'))
    tc.assertFalse(check_delimiters('< < > > >'))
    tc.assertFalse(check_delimiters('( [] < {} )'))

################################################################################
# INFIX -> POSTFIX CONVERSION
################################################################################

def infix_to_postfix(expr):
    """Returns the postfix form of the infix expression found in `expr`"""
    # you may find the following precedence dictionary useful
    prec = {'*': 2, '/': 2,
            '+': 1, '-': 1}
    ops = Stack()
    postfix = []
    toks = expr.split()
    ### BEGIN SOLUTION
    for tok in toks:
        if tok.isdigit():
            postfix.append(tok)
        else:
            #print(tok)
            if ops.empty() or ops.peek() == "(" or tok == "(":
                ops.push(tok)
            elif tok == ")":
                while ops:
                    if ops.peek() == "(":
                        ops.pop()
                        break
                    else:
                        postfix.append(ops.pop())
            elif prec[tok] > prec[ops.peek()]:
                    ops.push(tok)
            elif prec[tok] == prec[ops.peek()]:
                    postfix.append(ops.pop())
                    ops.push(tok)
            else:
                    postfix.append(ops.pop())
                    ops.push(tok)
    for x in ops:
        postfix.append(ops.pop())
    ### END SOLUTION
    return ' '.join(postfix)

################################################################################
# INFIX -> POSTFIX CONVERSION - TEST CASES
################################################################################

# points: 10
def test_infix_to_postfix_1():
    tc = TestCase()
    tc.assertEqual(infix_to_postfix('1'), '1')
    tc.assertEqual(infix_to_postfix('1 + 2'), '1 2 +')
    tc.assertEqual(infix_to_postfix('( 1 + 2 )'), '1 2 +')
    tc.assertEqual(infix_to_postfix('1 + 2 - 3'), '1 2 + 3 -')
    tc.assertEqual(infix_to_postfix('1 + ( 2 - 3 )'), '1 2 3 - +')

# points: 10
def test_infix_to_postfix_2():
    tc = TestCase()
    tc.assertEqual(infix_to_postfix('1 + 2 * 3'), '1 2 3 * +')
    tc.assertEqual(infix_to_postfix('1 / 2 + 3 * 4'), '1 2 / 3 4 * +')
    tc.assertEqual(infix_to_postfix('1 * 2 * 3 + 4'), '1 2 * 3 * 4 +')
    tc.assertEqual(infix_to_postfix('1 + 2 * 3 * 4'), '1 2 3 * 4 * +')

# points: 10
def test_infix_to_postfix_3():
    tc = TestCase()
    tc.assertEqual(infix_to_postfix('1 * ( 2 + 3 ) * 4'), '1 2 3 + * 4 *')
    tc.assertEqual(infix_to_postfix('1 * ( 2 + 3 * 4 ) + 5'), '1 2 3 4 * + * 5 +')
    tc.assertEqual(infix_to_postfix('1 * ( ( 2 + 3 ) * 4 ) * ( 5 - 6 )'), '1 2 3 + 4 * * 5 6 - *')

################################################################################
# QUEUE IMPLEMENTATION
################################################################################
class Queue:
    def __init__(self, limit=10):
        self.data = [None] * limit
        self.head = -1
        self.tail = -1

    ### BEGIN SOLUTION
    ### END SOLUTION

    def enqueue(self, val):
        ### BEGIN SOLUTION
        if self.tail + 1 >= len(self.data):
                self.tail = self.tail - len(self.data)
        if self.head == -1:
            self.data[0] = val
            self.tail = 0
            self.head = 0
        elif self.head - 1 == self.tail:
            if self.tail == -1:
                self.tail = len(self.data) - 1
            raise RuntimeError
        else:
            self.data[self.tail + 1] = val
            self.tail += 1
        ### END SOLUTION

    def dequeue(self):
        ### BEGIN SOLUTION
        if self.head == -1:
            raise RuntimeError
        elif self.head == self.tail:
            x = self.data[self.head]
            self.data[self.head] = None
            self.head = -1
            self.tail = -1
            return x
        else:
            if self.head >= len(self.data):
                self.head = self.head - len(self.data)
            x = self.data[self.head]
            self.data[self.head] = None
            self.head += 1
            return x
        ### END SOLUTION

    def resize(self, newsize):
        assert(len(self.data) < newsize)
        ### BEGIN SOLUTION
        start = list()
        end = list()
        m = self.tail - self.head
        if m < 0:
            m = m + len(self.data)
        for x in range(self.head):
            end.append(self.data[x])
        for y in range(self.head,len(self.data)):
            start.append(self.data[y])
        out = start + end
        for z in range(newsize - len(self.data)):
            out.append(None)
        self.head = 0
        self.tail = m
        self.data = out
        ### END SOLUTION

    def empty(self):
        ### BEGIN SOLUTION
        if self.head == -1:
            return True
        else:
            return False
        ### END SOLUTION

    def __bool__(self):
        return not self.empty()

    def __str__(self):
        if not(self):
            return ''
        return ', '.join(str(x) for x in self)

    def __repr__(self):
        return str(self)

    def __iter__(self):
        ### BEGIN SOLUTION
        m = self.tail
        if m < self.head:
            m = self.tail + len(self.data)
        for x in range(self.head,m+1):
            y = x
            if (x >= len(self.data)):
                y = x - len(self.data)
            yield self.data[y]
        ### END SOLUTION

################################################################################
# QUEUE IMPLEMENTATION - TEST CASES
################################################################################

# points: 13
def test_queue_implementation_1():
    tc = TestCase()

    q = Queue(5)
    tc.assertEqual(q.data, [None] * 5)

    for i in range(5):
        q.enqueue(i)

    with tc.assertRaises(RuntimeError):
        q.enqueue(5)

    for i in range(5):
        tc.assertEqual(q.dequeue(), i)

    tc.assertTrue(q.empty())

# points: 13
def test_queue_implementation_2():
    tc = TestCase()

    q = Queue(10)

    for i in range(6):
        q.enqueue(i)

    tc.assertEqual(q.data.count(None), 4)

    for i in range(5):
        q.dequeue()

    tc.assertFalse(q.empty())
    tc.assertEqual(q.data.count(None), 9)
    tc.assertEqual(q.head, q.tail)
    tc.assertEqual(q.head, 5)

    for i in range(9):
        q.enqueue(i)

    with tc.assertRaises(RuntimeError):
        q.enqueue(10)

    for x, y in zip(q, [5] + list(range(9))):
        tc.assertEqual(x, y)

    tc.assertEqual(q.dequeue(), 5)
    for i in range(9):
        tc.assertEqual(q.dequeue(), i)  

    tc.assertTrue(q.empty())

# points: 14
def test_queue_implementation_3():
    tc = TestCase()
	
    q = Queue(5)
    for i in range(5):
        q.enqueue(i)
    for i in range(4):
        q.dequeue()
    for i in range(5, 9):
        q.enqueue(i)

    with tc.assertRaises(RuntimeError):
        q.enqueue(10)

    q.resize(10)

    for x, y in zip(q, range(4, 9)):
        tc.assertEqual(x, y)

    for i in range(9, 14):
        q.enqueue(i)

    for i in range(4, 14):
        tc.assertEqual(q.dequeue(), i)

    tc.assertTrue(q.empty())
    tc.assertEqual(q.head, -1)

################################################################################
# TEST HELPERS
################################################################################
def say_test(f):
    print(80 * "*" + "\n" + f.__name__)

def say_success():
    print("SUCCESS")

################################################################################
# MAIN
################################################################################
def main():
    for t in [test_check_delimiters_1,
              test_check_delimiters_2,
              test_check_delimiters_3,
              test_check_delimiters_4,
              test_check_delimiters_5,
              test_check_delimiters_6,
              test_infix_to_postfix_1,
              test_infix_to_postfix_2,
              test_infix_to_postfix_3,
              test_queue_implementation_1,
              test_queue_implementation_2,
              test_queue_implementation_3]:
        say_test(t)
        t()
        say_success()


if __name__ == '__main__':
    main()
