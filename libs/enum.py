from enum import unique


def first_value_unique(enumeration):
    """ 装饰器：序列的第一个元素唯一 """
    unique(enumeration)
    number_set = set()
    for elem in enumeration:
        first_value = elem.value[0]
        if first_value in number_set:
            raise ValueError('duplicate first value found in %r' % elem)
        number_set.add(first_value)
    return enumeration
