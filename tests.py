import pickle
from sys import version_info
from unittest import TestCase, TestLoader, TextTestRunner

from typedecorator import (params, returns, void, setup_typecheck, Union,
    Nullable)


class TestTypeSignatures(TestCase):

    def setUp(self):
        setup_typecheck()

    def test_params_builtin_type(self):
        @params(a=int)
        def foo(a):
            pass

        # should not raise anything
        foo(1)

        self.assertRaises(TypeError, lambda: foo('a'))

    def test_params_custom_type(self):
        class MyType(object):
            pass

        @params(a=MyType)
        def foo(a):
            pass

        # should not raise anything
        foo(MyType())

        self.assertRaises(TypeError, lambda: foo(1))

    def test_params_list(self):
        @params(a=[int])
        def foo(a):
            pass

        # should not raise anything
        foo([])
        foo([1, 2, 3])

        self.assertRaises(TypeError, lambda: foo(1))
        self.assertRaises(TypeError, lambda: foo(['a']))
        self.assertRaises(TypeError, lambda: foo([1, 2, 'a', 3]))

    def test_params_dict(self):
        @params(a={str: int})
        def foo(a):
            pass

        # should not raise anything
        foo({})
        foo({'a': 1, 'b': 2})

        self.assertRaises(TypeError, lambda: foo(set()))
        self.assertRaises(TypeError, lambda: foo({'a': 'b'}))
        self.assertRaises(TypeError, lambda: foo({1: 1}))

    def test_params_set(self):
        @params(a=set([int]))  # 2.6 compat
        def foo(a):
            pass

        # should not raise anything
        foo(set())
        foo(set([1, 2, 3]))  # 2.6 compat

        self.assertRaises(TypeError, lambda: foo({}))
        self.assertRaises(TypeError, lambda: foo(set([1, 2, 'a'])))

    def test_params_xrange(self):
        try:
            range_type = xrange
        except NameError:
            range_type = range

        @params(a=range_type)
        def foo(a):
            pass

        # should not raise anything
        foo(range_type(10))
        foo(i for i in [1, 2])
        foo(iter([1, 2]))
        foo([])  # works because list supports the iterator protocol

    def test_params_tuple(self):
        @params(a=(int, bool))
        def foo(a):
            pass

        # should not raise anything
        foo((1, True))
        foo((0, False))

        self.assertRaises(TypeError, lambda: foo(1, True, None))
        self.assertRaises(TypeError, lambda: foo(True, 1))

    def test_params_union_types(self):
        @params(a=Union(int, str))
        def foo(a):
            pass

        # should not raise anything
        foo(42)
        foo('hello')

        self.assertRaises(TypeError, lambda: foo(3.14))
        self.assertRaises(TypeError, lambda: foo(None))

    def test_params_nullable_type(self):
        @params(a=Nullable(int))
        def foo(a=None):
            pass

        # should not raise anything
        foo(0)
        foo(None)

        self.assertRaises(TypeError, lambda: foo('a'))

    def test_params_variadic(self):
        @params(a=int, b=str)
        def foo(a, b=None, *args, **kwargs):
            pass

        foo(0)
        foo(0, 'b', 1, 2)
        foo(0, c='a')

        self.assertRaises(TypeError, lambda: foo('a'))
        self.assertRaises(TypeError, lambda: foo(0, 1, 2, 3))
        self.assertRaises(TypeError, lambda: foo(b=2, a=1))

    def test_invalid_signatures_throw_error(self):
        def foo(a):
            pass

        self.assertRaises(TypeError, lambda: params(a=int, b=int)(foo))
        self.assertRaises(TypeError, lambda: params(a=[int, int]))
        self.assertRaises(TypeError, lambda: params(a=None))


class TestParams(TestCase):

    def setUp(self):
        setup_typecheck()

    def test_params_args_kwargs(self):
        @params(a=int, b=str)
        def foo(a, b):
            pass

        # should not raise anything
        foo(1, 'test')
        foo(0, '')
        foo(b='foo', a=2)

        self.assertRaises(TypeError, lambda: foo(1, 1))
        self.assertRaises(TypeError, lambda: foo(b=0, a='x'))

    def test_invalid_signatures_throw_error(self):
        def foo(a):
            pass

        # sanity check that params() works
        params(a=int)(foo)

        self.assertRaises(TypeError, lambda: params()(foo))
        self.assertRaises(TypeError, lambda: params(int)(foo))


class TestReturns(TestCase):

    def setUp(self):
        setup_typecheck()

    def test_returns(self):
        @returns(int)
        def foo(x):
            return x

        # should not raise anything
        foo(1)

        self.assertRaises(TypeError, lambda: foo('a'))
        self.assertRaises(TypeError, lambda: foo(None))

    def test_void(self):
        @void
        def foo(x):
            return x

        # shoud not raise anything
        foo(None)

        self.assertRaises(TypeError, lambda: foo(1))

    def test_returns_nullable(self):
        @returns(Nullable(int))
        def foo(x):
            return x

        # should not raise anything
        foo(1)
        foo(None)

        self.assertRaises(TypeError, lambda: foo('a'))


class TestSetup(TestCase):

    def test_custom_exceptions(self):
        class MyError(Exception):
            pass

        setup_typecheck(exception=MyError)

        @returns(int)
        def foo():
            pass

        self.assertRaises(MyError, lambda: foo())

    def test_disabled_exception(self):
        setup_typecheck()

        @returns(int)
        def foo():
            pass

        self.assertRaises(TypeError, lambda: foo())

        setup_typecheck(exception=None)

        # should not raise anything any more
        foo()


class TestMethodAnnotation(TestCase):

    def setUp(self):
        setup_typecheck()

    def test_class_instance_methods(self):

        class Accumulator(object):
            sum = 0

            @void
            @params(self=object, a=int)
            def add(self, a):
                self.sum = self.sum + a

            @classmethod
            @returns(int)
            @params(cls=type, a=int, b=int)
            def add2(cls, a, b):
                return a + b

            @property
            @returns(int)
            def total(self):
                return self.sum

        a = Accumulator()

        # should not raise anything
        Accumulator.add2(1, 2)
        a.add(1)
        self.assertEqual(a.total, 1)

        self.assertRaises(TypeError, lambda: Accumulator.add2(1, 'a'))
        self.assertRaises(TypeError, lambda: a.add(None))


@returns(int)
@params(a=int, b=int)
def pickle_test_function(a, b):
    """Used for TestWrapping.test_wrapped_function_remains_pickleable"""
    return a + b


class TestWrapping(TestCase):

    def test_wrapped_function_remains_pickleable(self):
        dump = pickle.dumps(pickle_test_function)
        fn = pickle.loads(dump)
        self.assertEqual(fn(1, 1), 2)


def main():
    test_mods = [__name__]
    if version_info[0] == 3:
        test_mods.append('tests3')
    suite = TestLoader().loadTestsFromNames(test_mods)

    TextTestRunner().run(suite)


if __name__ == '__main__':
    main()
