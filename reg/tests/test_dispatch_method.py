from ..dispatch import dispatch_method
from ..predicate import match_instance


def test_dispatch_method_explicit_fallback():
    def get_obj(obj):
        return obj

    def obj_fallback(self, obj):
        return "Obj fallback"

    class Foo(object):
        @dispatch_method(match_instance('obj', get_obj, obj_fallback))
        def bar(self, obj):
            return "default"

    class Alpha(object):
        pass

    class Beta(object):
        pass

    foo = Foo()

    assert foo.bar(Alpha()) == "Obj fallback"

    Foo.bar.register(lambda self, obj: "Alpha", obj=Alpha)
    Foo.bar.register(lambda self, obj: "Beta", obj=Beta)

    assert foo.bar(Alpha()) == "Alpha"
    assert foo.bar(Beta()) == "Beta"
    assert foo.bar(None) == "Obj fallback"


def test_dispatch_method_without_fallback():
    def get_obj(obj):
        return obj

    def obj_fallback(self, obj):
        return "Obj fallback"

    class Foo(object):
        @dispatch_method(match_instance('obj', get_obj))
        def bar(self, obj):
            return "default"

    class Alpha(object):
        pass

    class Beta(object):
        pass

    foo = Foo()

    assert foo.bar(Alpha()) == "default"

    Foo.bar.register(lambda self, obj: "Alpha", obj=Alpha)
    Foo.bar.register(lambda self, obj: "Beta", obj=Beta)

    assert foo.bar(Alpha()) == "Alpha"
    assert foo.bar(Beta()) == "Beta"
    assert foo.bar(None) == "default"


def test_dispatch_method_register_function():
    def get_obj(obj):
        return obj

    def obj_fallback(self, obj):
        return "Obj fallback"

    class Foo(object):
        @dispatch_method(match_instance('obj', get_obj))
        def bar(self, obj):
            return "default"

    class Alpha(object):
        pass

    class Beta(object):
        pass

    foo = Foo()

    assert foo.bar(Alpha()) == "default"

    Foo.bar.register_function(lambda obj: "Alpha", obj=Alpha)
    Foo.bar.register_function(lambda obj: "Beta", obj=Beta)

    assert foo.bar(Alpha()) == "Alpha"
    assert foo.bar(Beta()) == "Beta"
    assert foo.bar(None) == "default"


def test_dispatch_method_register_auto():
    def get_obj(obj):
        return obj

    def obj_fallback(self, obj):
        return "Obj fallback"

    class Foo(object):
        x = 'X'

        @dispatch_method(match_instance('obj', get_obj))
        def bar(self, obj):
            return "default"

    class Alpha(object):
        pass

    class Beta(object):
        pass

    foo = Foo()

    assert foo.bar(Alpha()) == "default"

    Foo.bar.register_auto(lambda obj: "Alpha", obj=Alpha)
    Foo.bar.register_auto(lambda app, obj: "Beta %s" % app.x, obj=Beta)

    assert foo.bar(Alpha()) == "Alpha"
    assert foo.bar(Beta()) == "Beta X"
    assert foo.bar(None) == "default"


def test_dispatch_method_class_method_accessed_first():
    def get_obj(obj):
        return obj

    def obj_fallback(self, obj):
        return "Obj fallback"

    class Foo(object):
        @dispatch_method(match_instance('obj', get_obj))
        def bar(self, obj):
            return "default"

    class Alpha(object):
        pass

    class Beta(object):
        pass

    Foo.bar.register(lambda self, obj: "Alpha", obj=Alpha)
    Foo.bar.register(lambda self, obj: "Beta", obj=Beta)

    foo = Foo()

    assert foo.bar(Alpha()) == "Alpha"
    assert foo.bar(Beta()) == "Beta"
    assert foo.bar(None) == "default"


def test_dispatch_method_accesses_instance():
    def get_obj(obj):
        return obj

    def obj_fallback(self, obj):
        return "Obj fallback"

    class Foo(object):
        def __init__(self, x):
            self.x = x

        @dispatch_method(match_instance('obj', get_obj))
        def bar(self, obj):
            return "default %s" % self.x

    class Alpha(object):
        pass

    class Beta(object):
        pass

    Foo.bar.register(lambda self, obj: "Alpha %s" % self.x, obj=Alpha)
    Foo.bar.register(lambda self, obj: "Beta %s" % self.x, obj=Beta)

    foo = Foo('hello')

    assert foo.bar(Alpha()) == "Alpha hello"
    assert foo.bar(Beta()) == "Beta hello"
    assert foo.bar(None) == "default hello"


def test_dispatch_method_inheritance_register_on_subclass():
    def get_obj(obj):
        return obj

    def obj_fallback(self, obj):
        return "Obj fallback"

    class Foo(object):
        @dispatch_method(match_instance('obj', get_obj))
        def bar(self, obj):
            return "default"

    class Sub(Foo):
        pass

    class Alpha(object):
        pass

    class Beta(object):
        pass

    sub = Sub()

    assert sub.bar(Alpha()) == "default"

    Sub.bar.register(lambda self, obj: "Alpha", obj=Alpha)
    Sub.bar.register(lambda self, obj: "Beta", obj=Beta)

    assert sub.bar(Alpha()) == "Alpha"
    assert sub.bar(Beta()) == "Beta"
    assert sub.bar(None) == "default"


def test_dispatch_method_inheritance_separation():
    def get_obj(obj):
        return obj

    def obj_fallback(self, obj):
        return "Obj fallback"

    class Foo(object):
        @dispatch_method(match_instance('obj', get_obj))
        def bar(self, obj):
            return "default"

    class Sub(Foo):
        pass

    class Alpha(object):
        pass

    class Beta(object):
        pass

    Foo.bar.register(lambda self, obj: "Foo Alpha", obj=Alpha)
    Foo.bar.register(lambda self, obj: "Foo Beta", obj=Beta)
    Sub.bar.register(lambda self, obj: "Sub Alpha", obj=Alpha)
    Sub.bar.register(lambda self, obj: "Sub Beta", obj=Beta)

    foo = Foo()
    sub = Sub()

    assert foo.bar(Alpha()) == "Foo Alpha"
    assert foo.bar(Beta()) == "Foo Beta"
    assert foo.bar(None) == "default"

    assert sub.bar(Alpha()) == "Sub Alpha"
    assert sub.bar(Beta()) == "Sub Beta"
    assert sub.bar(None) == "default"


def test_dispatch_method_inheritance_separation_multiple():
    def get_obj(obj):
        return obj

    def obj_fallback(self, obj):
        return "Obj fallback"

    class Foo(object):
        @dispatch_method(match_instance('obj', get_obj))
        def bar(self, obj):
            return "bar default"

        @dispatch_method(match_instance('obj', get_obj))
        def qux(self, obj):
            return "qux default"

    class Sub(Foo):
        pass

    class Alpha(object):
        pass

    class Beta(object):
        pass

    Foo.bar.register(lambda self, obj: "Bar Foo Alpha", obj=Alpha)
    Foo.bar.register(lambda self, obj: "Bar Foo Beta", obj=Beta)
    Sub.bar.register(lambda self, obj: "Bar Sub Alpha", obj=Alpha)
    Sub.bar.register(lambda self, obj: "Bar Sub Beta", obj=Beta)

    Foo.qux.register(lambda self, obj: "Qux Foo Alpha", obj=Alpha)
    Foo.qux.register(lambda self, obj: "Qux Foo Beta", obj=Beta)
    Sub.qux.register(lambda self, obj: "Qux Sub Alpha", obj=Alpha)
    Sub.qux.register(lambda self, obj: "Qux Sub Beta", obj=Beta)

    foo = Foo()
    sub = Sub()

    assert foo.bar(Alpha()) == "Bar Foo Alpha"
    assert foo.bar(Beta()) == "Bar Foo Beta"
    assert foo.bar(None) == "bar default"

    assert sub.bar(Alpha()) == "Bar Sub Alpha"
    assert sub.bar(Beta()) == "Bar Sub Beta"
    assert sub.bar(None) == "bar default"

    assert foo.qux(Alpha()) == "Qux Foo Alpha"
    assert foo.qux(Beta()) == "Qux Foo Beta"
    assert foo.qux(None) == "qux default"

    assert sub.qux(Alpha()) == "Qux Sub Alpha"
    assert sub.qux(Beta()) == "Qux Sub Beta"
    assert sub.qux(None) == "qux default"
