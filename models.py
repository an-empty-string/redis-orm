from db import connection


class Base(object):
    def __init__(self, **kwargs):
        self.__name__ = self.__class__.__name__
        for i in kwargs:
            self.__setattr__(i, kwargs[i])
        for i in self.fields:
            if i not in self.__dict__:
                self.__setattr__(i, self.fields[i])

    def save(self):
        """Saves things like User:username:fwilson:uid"""
        fstr = self.__name__ + ":%s:%s"
        for i in self.fields:
            this_fstr = fstr % (i, self.__getattribute__(i))
            for j in self.fields:
                key = this_fstr + (":%s:%d" % (j, hash(self)))
                connection.set(key, self.__getattribute__(j))
        connection.save()

    @classmethod
    def get(self, field, **kwargs):
        key = kwargs.keys()[0]
        keys = connection.keys(self.__name__ + ":%s:%s:%s*" % (key,
                                                               kwargs[key],
                                                               field))
        return [connection.get(i) for i in keys]

    @classmethod
    def delete(self, **kwargs):
        key = kwargs.keys()[0]
        value = kwargs[key]
        keys = [i for i in connection.keys(self.__name__ + ("*%s*" % key))
                if connection.get(i) == value]
        if keys == []:
            return
        connection.delete(*keys)
        connection.save()


class Student(Base):
    fields = {"firstname": "John",
              "lastname":  "Doe",
              "address":   "6560 Braddock Road"}
