from typing import Any, Iterable, TypeVar

NameType = TypeVar('NameType', str, Iterable[str])


def add(name: NameType, value: Any):
    if isinstance(name, Iterable) \
            and (not isinstance(value, Iterable)):
        raise TypeError("value should be Iterable when name is Iterable")
    if type(name) is str:
        name = [name]
        value = [value]

    for n, v in zip(name, value):
        exec('self.{}={}'.format(n, v))


class GlobalVariable:
    def __init__(self) -> None:
        pass

    def all(self):
        attrs = [i for i in dir(self)]
        attr = []
        for i in range(len(attrs)):
            if len(attrs[i]) > 1:
                if '__' == attrs[i][:2]:
                    continue
            if attrs[i] in ['all', 'add', 'rm', 'get']:
                continue

            attr.append(attrs[i])
        return attr

    def rm(self, name: NameType):
        if type(name) is str:
            name = [name]
        for n in name:
            self.__delattr__(n)

    def get(self, name: NameType):
        if type(name) is str:
            return self.__getattribute__(name)
        else:
            attrs = []
            for n in name:
                attrs.append(self.__getattribute__(n))
            return attrs


global globalVariables

try:
    tmp = globalVariables.all()
except NameError:
    globalVariables = GlobalVariable()
else:
    pass

'''
# 添加一个名为 newVariable 的变量
# 方法一
gbv.newVariable = 199
 
# 方法二
gbv.add('newVariable', 199)
 
 
# 添加一系列变量
nameList = ['a', 'b', 'c']
valueList = [100, 200, 300]
gbv.add(nameList, valueList)

----------
# 方法一
gbv.varName
 
#方法二
gbv.get('varName')
 
nameList = ['name1', 'name2', 'name3']
gbv.get(nameList)
-----------
gbv.rm('variableName')
----------
gbv.all()
'''