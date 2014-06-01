# Tests using Python3-specific syntax
from unittest import TestCase, main

from typedecorator import typed, setup_typecheck


class TestPython3Annotations(TestCase):
    def setUp(self):
        setup_typecheck()

    def test_typed(self):

        @typed
        def foo(a: int, b: int) -> int:
            return a + b

        @typed
        def bar(a) -> bool:
            return a

        # should not raise exception
        foo(1, 1)
        bar(True)

        with self.assertRaises(TypeError):
            foo('a', 1)

        with self.assertRaises(TypeError):
            foo(1, 3.14)

        with self.assertRaises(TypeError):
            bar('x')


if __name__ == '__main__':
    main()
