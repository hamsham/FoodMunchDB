__author__ = 'hammy'

import types


def enum_type(cls):
    cls.__init__ = None
    cls.enum_keys = [key for key in cls.__dict__
                     if not key.startswith('_')
                     and not isinstance(cls.__dict__[key], types.FunctionType)
                     and not isinstance(cls.__dict__[key], types.MethodType)
                     and not isinstance(cls.__dict__[key], types.LambdaType)]
    cls.enum_values = [cls.__dict__[key] for key in cls.enum_keys]
    cls.enum_dict = {k: v for (k, v) in zip(cls.enum_keys, cls.enum_values)}

    @staticmethod
    def valueof(val):
        return cls.enum_dict[val]
    cls.valueof = valueof
    return cls


if __name__ == '__main__':
    @enum_type
    class EnumTest:
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = lambda x: x+1

    try:
        classtype = EnumTest()
        assert classtype is None
    except AssertionError as e:
        print 'Unable to prevent enum types from being instantiated.'
    except TypeError as e:
        print 'Successfully prevented enum types from being instantiated.'

    print EnumTest.enum_keys
    print EnumTest.enum_values
    print EnumTest.valueof('THREE')