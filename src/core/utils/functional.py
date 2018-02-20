import unittest

"""
A Library containing Functional utilis and types
"""

class Option:
    """
    A functional interface for performing operations on values that may or may not be present.
    """

    def __init__(self, val):
        """
        Construct an Option type that contains methods that operate on the value if present or not.
        :param val: The value to construct the Option around.
        """
        self.__val = val

    def get(self):
        """
        Get the underlying value of the Option. 
        :return: A value that may or may not be present.
        """
        return self.__val

    def isPresent(self):
        """
        Query if the Option contains a Value.
        :return: True if the Options value is not 'None'.
        """
        return self.__val is not None

    def ifPresent(self, fn):
        """
        Invoke a function on the Option if the value is present.
        :param fn: A fuction that accepts the present value.
        :return: Void
        """
        if self.isPresent():
            fn(self.get())

    def map(self, fn):
        """
        Maps the element of the source Option using the argument function.
        :param fn: A function that maps the source vaue if present to a value.
        :return: An Option that either contains the mapped value, or is empty.
        """
        if self.isPresent():
            return Option(fn(self.get()))
        else:
            return self
        
    def orElse(self, val):
        """
        Coerces the Option to a value if it is present, or returns the default supplied value.
        :param val: The default value to use if the Option does not contain a value.
        :return: The optional value if it is present, or else the default value.
        """
        if self.isPresent():
            return self.get()
        else:
            return val

    def filter(self, fn):
        """
        Filters the Option using the argument function, retaining the value if the function returns true.
        :param fn: A Function that filtesr the Option (assigns a boolean value).
        :return: An option that either contains the Option value or contains None
        """
        if self.isPresent() and fn(self.get()):
            return Option(self.get())
        else:
            return Option(None)


class Vector:
    """
    Functional interface for a list.
    """

    def __init__(self, *args):
        self.__data = list(args)
    
    def __getitem__(self, index):
        return self.__data[index]

    def __setitem__(self, index, val):
        self.__data[index] = val

    def __len__(self):
        return len(self.__data)

    @staticmethod
    def __getElementsAt(index, args):
        ans = []
        for arg in args:
            ans.append(arg[index])
        return ans

    @staticmethod
    def fromList(list):
        """
        Constructs a Vector from an argument list.
        :param list: The list to construct the Vector from.
        """
        return Vector(*list)

    def getList(self):
        """
        Get the list underlying the Vector.
        :return: The Vector's underlying list.
        """
        return self.__data

    def forEach(self, fn, *args):
        """
        Perform the argument consumer function on each element in the Vector, and any additional argument Vectors.
        :param fn: A function that uses a/an element/s from this Vector and any additional supplied Vectors.
        :param *args: A variable number of additional Vectors to supply to the argument function for each enumeration.
        :return: Void
        """
        for index, val in enumerate(self.__data):
            fn(val, *self.__getElementsAt(index, args))

    def map(self, fn, *args):
        """
        Map the element/s from the source Vector and/or additional supplied Vectors using the argument consumer function.
        :param fn: A Function that maps elements from the source Vector and/or additional argument Vectors.
        :param *args: A variable number of additional Vectors to supply to the argument function for each enumeration.
        """
        ans = []
        for index, val in enumerate(self.__data):
            ans.append(fn(val, *self.__getElementsAt(index, args)))
        return Vector(*ans)

    def fold(self, fn, carry = 0, *args):
        """
        Applies the argument function to each element in the source (and/or additional supplied vectors) and supplies the result to the next element.
        :param fn: A function that accepts a 'carried' value from the prior evaluation of the function, and elements from the source vector and any additional vectors
        :param carry: The initial value to invoke the argument function with.
        :param *args: Any additional Vectors to apply the fold to.
        :return: The final value calculated by the argument function.
        """
        for index, val in enumerate(self.__data):
            carry = fn(carry, val, *self.__getElementsAt(index, args))
        return carry

    def filter(self, fn, *args):
        """
        Filters the elements of the source Vector (and/or additional supplied vectors)
        :param fn: A function to use to filter the vector with parameters corresponding to the elements from the source Vector and/or additional vectors
        :param *args: Any additional Vectors to use when applying the filter.
        :return: A Vector that filtesr the elements from the source vector.
        """
        ans = []
        for index, val in enumerate(self.__data):
            if fn(val, *self.__getElementsAt(index, args)):
                ans.append(val)
        return Vector(*ans)

    def toString(self):
        """
        :return: A String representation of the Vector.
        """
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

    def test_fromList(self):
        self.assertListEqual(Vector.fromList([1,2,3]).getList(), [1,2,3])

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