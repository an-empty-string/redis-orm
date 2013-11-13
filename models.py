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
        if(hasattr(self, "_hashvalue")):
            for i in connection.keys("%s:*:%s" % (self.__name__,
                                                  self._hashvalue)):
                connection.delete(i)
        self._hashvalue = hash(self)
        fstr = self.__name__ + ":%s:%s"
        for i in self.fields:
            this_fstr = fstr % (i, self.__getattribute__(i))
            for j in [q for q in self.fields if q != i]:
                key = this_fstr + (":%s:%d" % (j, hash(self)))
                connection.set(key, self.__getattribute__(j))
        connection.save()

    def __repr__(self):
        return "%s: %s" % (self.__name__, repr(self.__dict__))

    @classmethod
    def get(self, **kwargs):
        key = kwargs.keys()[0]
        value = kwargs[key]
        o = [self._get_object_by_hash(i) for i in self._get_hashes(key, value)]
        return o

    @classmethod
    def get_fields(self, field, **kwargs):
        key = kwargs.keys()[0]
        keys = connection.keys(self.__name__ + ":%s:%s:%s*" % (key,
                                                               kwargs[key],
                                                               field))
        return [connection.get(i) for i in keys]

    @classmethod
    def _get_keys(self, field, key, value):
        keys = connection.keys(self.__name__ + ":%s:%s:%s*" % (key,
                                                               value,
                                                               field))
        return keys

    @classmethod
    def _get_hashes(self, key, value):
        hashes = [i.split(":")[-1] for i in self._get_keys("*", key, value)]
        return list(set(hashes))

    @classmethod
    def _get_object_by_hash(self, h):
        keys = connection.keys("%s:*:%s" % (self.__name__, h))
        keydict = {}
        keydict['_hashvalue'] = h
        for i in keys:
            keydict[i.split(":")[3]] = connection.get(i)
        return self(**keydict)

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
              "address":   "6560 Braddock Road",
              }
