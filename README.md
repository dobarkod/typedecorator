A decorator-based implementation of type checks.

Provides `@params`, `@returns` and `@void` decorators for describing
the type of the function arguments and return values. If the types mismatch,
an exception can be thrown, the mismatch can be logged, or it can be ignored.

Example:

    @returns({str: int})
    @params(data={str: int}, key=str, val=int)
    def add_to_data(data, key, val):
        data[key] = val
        return data

## Quickstart

To start using it, just install the package using pip:

    pip install typedecorator

You can now start using it in your code

    # import the decorators and the typecheck setup function
    from typedecorator import params, returns, setup_typecheck

    # decorate your functions
    @returns(int)
    @params(a=int, b=int)
    def add(a, b):
        return a + b

    # set up the type checking
    setup_typecheck()

    add(1, 2)  # works fine
    add('one', 2)  # will raise a TypeError

You ony need to call `setup_typecheck` once to enable it and optionally
# configure exceptions thrown and logging level. You can use it multiple
time to change, disable, or re-enable typechecks at runtime. See the
Setup section for more information.

## Type Signatures

Both @params and @returns take type signatures that can describe both simple
and complex types. The @void decorator is a shorthand for @returns(type(None)),
describing a function returning nothing.

A type signature can be:

1. A type, such as `int`, `str`, `bool`, `object`, `dict`, `list`, or a
custom class, requiring that the value be of specified type or a subclass of
the specified type. Since every type is a subclass of `object`, `object`
matches any type.

2. A list containing a single element, requiring that the value be a list of
values, all matching the type signature of that element. For example, a type
signature specifying a list of integers would be `[int]`.

3. A tuple containing one or more elements, requiring that the value be a tuple
whose elements match the type signatures of each element of the tuple. For
eample, type signature `(int, str, bool)` matches tuples whose first element
is an integer, second a string and third a boolean value.

4. A dictionary containing a single element, requiring that the value be a
dictionary with keys of type matching the dict key, and values of type
matching the dict value. For example, `{str:object}` describes a dictionary
with string keys, and anything as values.

5. A set containing a single element, requiring that the value be a set
with elements of type matching the set element. For example, `{str}` matches
any set consisting solely of strings.

6. `xrange`, matching any iterator.

These rules are recursive, so it is possible to construct arbitrarily
complex type signatures. Here are a few examples:

* `{str: (int, [MyClass])}` - dictionary with string keys, where values are
    tuples with first element being an integer, and a second being a list
    of instances of MyClass

* `{str: types.FunctionType}` - dictionary mapping strings to functions

* `{xrange}` - set of iterators

Note that `[object]` is the same as `list`, `{object:object}` is the same
as `dict` and `{object}` is the same as  `set`.

## Setup

The function `setup_typecheck` takes care of enabling, disabling, and
configuring type checks at "compile" (parse) time and at runtime.

The function takes three optional arguments:

* `enabled` - whether to enable checks of any kind (default: True)
* `exception` - which exception to raise if type check fails (default:
  TypeError), or None to disable raising the exception
* `loglevel` - the log level at which to log the type error (see the
  standard `logging` module for possible levels), or None to disable type
  error logging.

By default, the type checking system is inactive unless activated through
this function. However, the type-checking wrappers are in place, so the
type checking can be enabled or disabled at runtime (multiple times).
These wrappers do incur a very small but real performance cost. If you
want to disable the checks at "compile" time, call this function with
`enabled=False` *before* defining any functions or methods using the
typecheck decorator.

For example, if you have a `config.py` file with `USE_TYPECHECK` constant
specifying whether you want the type checks enabled:

    #!/usr/bin/env python

    from typecheck import setup_typecheck, params
    import config

    setup_typecheck(enabled=config.USE_TYPECHECK)

    @params(a=int, b=int):
    def add(a, b):
        return a + b

Note that in this case, the checks cannot be enabled at runtime.

## Mocking

Since the type signatures compare the actual value types, the parameters
can't be mocked. To minimize the problem, `Mock` type from `mock` library
(the most used mocking library in Python, and part of Python 3 standard
library) is special cased - an instance of `Mock` (or any of its subclasses,
such as `MagicMock`) will pass any check.

## License

Copyright (C) 2014. Senko Rasic <senko.rasic@goodcode.io>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
