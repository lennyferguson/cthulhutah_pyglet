import unittest

class Option:
    def __init__(self, val):
        self.__val = val

    def get(self):
        return self.__val

    def isPresent(self):
        return self.__val is not None

    def ifPresent(self, fn):
        if self.isPresent():
            fn(self.get())

    def map(self, fn):
        if self.isPresent():
            return Option(fn(self.get()))
        else:
            return self
        
    def orElse(self, val):
        if self.isPresent():
            return self.get()
        else:
            return val

    def filter(self, fn):
        if self.isPresent() and fn(self.get()):
            return Option(self.get())
        else:
            return Option(None)


class Vector:
    def __init__(self, *args):
        self.__data = list(args)
    
    def __getitem__(self, index):
        return self.__data[index]

    def __setitem__(self, index, val):
        self.__data[index] = val

    @staticmethod
    def __getElementsAt(index, args):
        ans = []
        for arg in args:
            ans.append(arg[index])
        return ans

    @staticmethod
    def fromArray(array):
        return Vector(*array)

    def getList(self):
        return self.__data

    def forEach(self, fn, *args):
        for index, val in enumerate(self.__data):
            fn(val, *self.__getElementsAt(index, args))

    def map(self, fn, *args):
        ans = []
        for index, val in enumerate(self.__data):
            ans.append(fn(val, *self.__getElementsAt(index, args)))
        return Vector(*ans)

    def fold(self, fn, carry = 0, *args):
        for index, val in enumerate(self.__data):
            carry = fn(carry, val, *self.__getElementsAt(index, args))
        return carry

    def filter(self, fn, *args):
        ans = []
        for index, val in enumerate(self.__data):
            if fn(val, *self.__getElementsAt(index, args)):
                ans.append(val)
        return Vector(*ans)

    def toString(self):
        ans = ""
        for val in self.__data:
            ans += "{} ".format(val)
        return ans

class TestOptional(unittest.TestCase):
    def test_isPresent(self):
        o = Option(None)
        self.assertFalse(o.isPresent())
    
    def test_ifPresent(self):
        class TestPresent:
            def __init__(self, val):
                self.value = val

            def set(self,val):
                self.value = val

        test = TestPresent(False)
        Option(True).ifPresent(lambda v: test.set(v))
        self.assertTrue(test.value)

    def test_get(self):
        self.assertTrue(Option(True).get())

    def test_map(self):
        self.assertEqual(Option("1").map(lambda v: int(v)).get(), 1)

    def test_orElse(self):
        self.assertEqual(Option(None).orElse(1), 1)

    def test_filter(self):
        self.assertFalse(Option(5).filter(lambda v: v > 10).isPresent())


class TestVector(unittest.TestCase):
    def test_getitem(self):
        self.assertEqual(Vector(1,2,3)[0], 1)

    def test_setitem(self):
        v = Vector(1,1,1)
        v[0] = 100
        self.assertEqual(v[0], 100)

    def test_fromArray(self):
        self.assertListEqual(Vector.fromArray([1,2,3]).getList(), [1,2,3])

    def test_forEach(self):
        class Iter:
            def __init__(self):
                self.iter = 0

            def incr(self):
                self.iter += 1

        i = Iter()
        Vector(1,2,3,4).forEach(lambda _: i.incr())
        self.assertEqual(i.iter, 4)

    def test_map(self):
        self.assertListEqual(Vector(1,2,3).map(lambda v: v + 1).getList(), [2,3,4])

    def test_map2(self):
        self.assertListEqual(Vector(1,2,3).map(lambda v1, v2: v1 + v2, Vector(4,5,6)).getList(), [5,7,9])

    def test_map3(self):
        self.assertListEqual(Vector(1,1,1).map(lambda v1, v2, v3: v1 + v2 + v3, Vector(2,2,2), Vector(3,3,3)).getList(), [6,6,6])

    def test_fold(self):
        self.assertEqual(Vector(1,1,1).fold(lambda a, b: a + b, 0), 3)

    def test_fold2(self):
        self.assertEqual(Vector(1,1,1).fold(lambda a, b, c: a + b + c, 0, Vector(1,1,1)), 6)

    def test_fold3(self):
        self.assertEqual(Vector(1,1,1).fold(lambda a, b, c, d: a + b + c + d, 0, Vector(1,1,1), Vector(1,1,1)), 9)

    def test_filter(self):
        self.assertListEqual(Vector(0,10,20,30,40,50).filter(lambda v: v > 20).getList(), [30,40,50])

    def test_filter2(self):
        self.assertListEqual(Vector(1,2,3).filter(lambda v1, v2: v1 >=2 and v2, Vector(True,True,False)).getList(), [2])

if __name__ == '__main__':
    unittest.main()