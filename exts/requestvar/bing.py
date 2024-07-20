def bind_contextvar(contextvar):
    class ContextVarBind:
        __slots__ = ()

        def __getattr__(self, name):
            # request.some_attr
            return getattr(contextvar.get(), name)

        def __setattr__(self, name, value):
            # request.some_attr = value
            setattr(contextvar.get(), name, value)

        def __delattr__(self, name):
            # del request.some_attr
            delattr(contextvar.get(), name)

        def __getitem__(self, index):
            # request[index]
            return contextvar.get()[index]

        def __setitem__(self, index, value):
            # request[index] = value
            contextvar.get()[index] = value

        def __delitem__(self, index):
            # del request[index]
            del contextvar.get()[index]

    return ContextVarBind()
