from unittest import TestCase
import random

class AVLTree:
    class Node:
        def __init__(self, val, left=None, right=None):
            self.val = val
            self.left = left
            self.right = right
            self.bf = 0

        def rotate_right(self):
            n = self.left
            self.val, n.val = n.val, self.val
            self.left, n.left, self.right, n.right = n.left, n.right, n, self.right

        def rotate_left(self):
            ### BEGIN SOLUTION
            n = self.right
            self.val, n.val = n.val, self.val
            self.right, n.right, self.left, n.left = n.right, n.left, n, self.left
            ### END SOLUTION

        @staticmethod
        def height(n):
            if not n:
                return 0
            else:
                return max(1+AVLTree.Node.height(n.left), 1+AVLTree.Node.height(n.right))

    def __init__(self):
        self.size = 0
        self.root = None

    @staticmethod
    def helpdel(t):
        ### BEGIN SOLUTION
        path = []
        if t.bl == -1:
            cur = t.left
            if cur.right:         
                while True:
                    if cur.right:
                        path.append((cur,False))
                        cur.right
                    else:
                        break
                t.val = cur.val
                return path
            else:
                m = cur
                t.val = m.val
                t.left = m.left
                return [(m, True)]
        else:
            cur = t.right
            if cur.left:         
                while True:
                    if cur.left:
                        path.append((cur,True))
                        cur.left
                    else:
                        break
                t.val = cur.val
                return path
            else:
                m = cur
                t.val = m.val
                t.right = m.right
                return [(m,False)]
        ### END SOLUTION

    def add(self, val):
        assert(val not in self)
        ### BEGIN SOLUTION
        # check not first
        if self.root == None:
            self.root = self.Node(val,None,None)
            pass
        else:

            path = []
            cur = self.root

            # create path to node and add node
            while True:
                if cur == None:
                    if path[-1][1] == True:
                        path[-1][0].left = self.Node(val,None,None)
                    else:
                        path[-1][0].right = self.Node(val,None,None)
                    break
                elif val < cur.val:
                    path.append((cur, True))
                    cur = cur.left
                else:
                    path.append((cur, False))
                    cur = cur.right

            # modify then check balance
            for x in range(len(path)-1,-1,-1):
                cur = path[x]
                path[x][0].bl = path[x][0].height(cur[0].right) - path[x][0].height(cur[0].left)
                # right heavy
                if path[x][0].bl > 1:
                    # if added node was added to the right nodes right tree
                    if path[x+1][1] == False:
                        path[x][0].rotate_left()
                    else: # right nodes left tree
                        path[x+1][0].rotate_right()
                        path[x][0].rotate_left()
                elif path[x][0].bl < -1:
                    if path[x+1][1] == True:
                        path[x][0].rotate_right()
                    else: 
                        path[x+1][0].rotate_left()
                        path[x][0].rotate_right()

        ### END SOLUTION

    def __delitem__(self, val):
        assert(val in self)
        ### BEGIN SOLUTION
        if self.root.left == None and self.root.right == None:
            self.root = None
        elif self.root.val == val:
            if self.root.bf == -1:
                n = self.root.left
                self.root.val, n.val = n.val, self.root.val
                self.root.left, n.left, self.root.right, n.right = n.left, n.right, n, self.root.right
            else:
                n = self.root.right
                self.root.val, n.val = n.val, self.root.val
                self.root.right, n.right, self.root.left, n.left = n.right, n.left, n, self.root.left
        else:
            path = []
            cur = self.root

            # create path to node
            while True:
                if cur.val == val:
                    break
                elif val < cur.val:
                    path.append((cur, True))
                    cur = cur.left
                else:
                    path.append((cur, False))
                    cur = cur.right
                
            # down the chain
            path2 = []
            pre = None
            if path[-1][1] == True:
                cur = path[-1][0].left
                if cur.left == None:
                    if cur.right == None:
                        path[-1][0].left = None
                    else:
                        path[-1][0].left = cur.right
                elif cur.right == None:
                    path[-1][0].left = cur.left
                else:
                    path = path + self.helpdel(path[-1][0].left)
                        
            else:
                cur = path[-1][0].right
                if cur.left == None:
                    if cur.right == None:
                        path[-1][0].right = None
                    else:
                        path[-1][0].right = cur.right
                elif cur.right == None:
                    path[-1][0].right = cur.left
                else:
                    path = path + self.helpdel(path[-1][0].right)


            # modify then check balance up
            for x in range(len(path)-1,-1,-1):
                cur = path[x]
                path[x][0].bl = path[x][0].height(cur[0].right) - path[x][0].height(cur[0].left)

                # right heavy
                if path[x][0].bl > 1:
                    path[x][0].rotate_left()
                elif path[x][0].bl < -1:
                    path[x][0].rotate_right()
        ### END SOLUTION
 
    def __contains__(self, val):
        def contains_rec(node):
            if not node:
                return False
            elif val < node.val:
                return contains_rec(node.left)
            elif val > node.val:
                return contains_rec(node.right)
            else:
                return True
        return contains_rec(self.root)

    def __len__(self):
        return self.size

    def __iter__(self):
        def iter_rec(node):
            if node:
                yield from iter_rec(node.left)
                yield node.val
                yield from iter_rec(node.right)
        yield from iter_rec(self.root)

    def pprint(self, width=64):
        """Attempts to pretty-print this tree's contents."""
        height = self.height()
        nodes  = [(self.root, 0)]
        prev_level = 0
        repr_str = ''
        while nodes:
            n,level = nodes.pop(0)
            if prev_level != level:
                prev_level = level
                repr_str += '\n'
            if not n:
                if level < height-1:
                    nodes.extend([(None, level+1), (None, level+1)])
                repr_str += '{val:^{width}}'.format(val='-', width=width//2**level)
            elif n:
                if n.left or level < height-1:
                    nodes.append((n.left, level+1))
                if n.right or level < height-1:
                    nodes.append((n.right, level+1))
                repr_str += '{val:^{width}}'.format(val=n.val, width=width//2**level)
        print(repr_str)

    def height(self):
        """Returns the height of the longest branch of the tree."""
        def height_rec(t):
            if not t:
                return 0
            else:
                return max(1+height_rec(t.left), 1+height_rec(t.right))
        return height_rec(self.root)

################################################################################
# TEST CASES
################################################################################
def height(t):
    if not t:
        return 0
    else:
        return max(1+height(t.left), 1+height(t.right))

def traverse(t, fn):
    if t:
        fn(t)
        traverse(t.left, fn)
        traverse(t.right, fn)

# LL-fix (simple) test
# 10 points
def test_ll_fix_simple():
    tc = TestCase()
    t = AVLTree()

    for x in [3, 2, 1]:
        t.add(x)

    tc.assertEqual(height(t.root), 2)
    tc.assertEqual([t.root.left.val, t.root.val, t.root.right.val], [1, 2, 3])

# RR-fix (simple) test
# 10 points
def test_rr_fix_simple():
    tc = TestCase()
    t = AVLTree()

    for x in [1, 2, 3]:
        t.add(x)

    tc.assertEqual(height(t.root), 2)
    tc.assertEqual([t.root.left.val, t.root.val, t.root.right.val], [1, 2, 3])

# LR-fix (simple) test
# 10 points
def test_lr_fix_simple():
    tc = TestCase()
    t = AVLTree()

    for x in [3, 1, 2]:
        t.add(x)

    tc.assertEqual(height(t.root), 2)
    tc.assertEqual([t.root.left.val, t.root.val, t.root.right.val], [1, 2, 3])

# RL-fix (simple) test
# 10 points
def test_rl_fix_simple():
    tc = TestCase()
    t = AVLTree()

    for x in [1, 3, 2]:
        t.add(x)

    tc.assertEqual(height(t.root), 2)
    tc.assertEqual([t.root.left.val, t.root.val, t.root.right.val], [1, 2, 3])

# ensure key order is maintained after insertions and removals
# 30 points
def test_key_order_after_ops():
    tc = TestCase()
    vals = list(range(0, 100000000, 333333))
    random.shuffle(vals)

    t = AVLTree()
    for x in vals:
        t.add(x)

    for _ in range(len(vals) // 3):
        #print("dek")
        to_rem = vals.pop(random.randrange(len(vals)))
        del t[to_rem]
        

    vals.sort()

    for i,val in enumerate(t):
        tc.assertEqual(val, vals[i])

# stress testing
# 30 points
def test_stress_testing():
    tc = TestCase()

    def check_balance(t):
        tc.assertLess(abs(height(t.left) - height(t.right)), 2, 'Tree is out of balance')

    t = AVLTree()
    vals = list(range(1000))
    random.shuffle(vals)
    for i in range(len(vals)):
        t.add(vals[i])
        for x in vals[:i+1]:
            tc.assertIn(x, t, 'Element added not in tree')
        traverse(t.root, check_balance)

    random.shuffle(vals)
    for i in range(len(vals)):
        del t[vals[i]]
        for x in vals[i+1:]:
            tc.assertIn(x, t, 'Incorrect element removed from tree')
        for x in vals[:i+1]:
            tc.assertNotIn(x, t, 'Element removed still in tree')
        traverse(t.root, check_balance)



################################################################################
# TEST HELPERS
################################################################################
def say_test(f):
    print(80 * "#" + "\n" + f.__name__ + "\n" + 80 * "#" + "\n")

def say_success():
    print("----> SUCCESS")

################################################################################
# MAIN
################################################################################
def main():
    m = AVLTree()

    for x in range(23):
        m.add(x)
    m.pprint()
    del m[11]
    m.pprint()
    

    #for t in [test_ll_fix_simple,
    #          test_rr_fix_simple,
     #         test_lr_fix_simple,
     #         test_rl_fix_simple,
     #         test_key_order_after_ops,
     #         test_stress_testing]:
    #    say_test(t)
      #  t()
     #   say_success()
    #print(80 * "#" + "\nALL TEST CASES FINISHED SUCCESSFULLY!\n" + 80 * "#")

if __name__ == '__main__':
    main()
