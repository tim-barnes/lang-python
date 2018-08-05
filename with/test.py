


class A:

    def get():
        return B()

class B:
    def __enter__(self):
        print("Entering block")
        return self

    def __exit__(self, type, value, traceback):
        print("Exiting block")
        return False

    def foo(self):
        print("Foo")



with A.get() as b:
    b.foo()
