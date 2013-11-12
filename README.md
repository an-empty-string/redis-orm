Redis-ORM
===

(aka when fwilson went crazy)

Redis-ORM is kind of like SQLAlchemy for Redis. It works like this:
```
>>> s = Student(firstname="John", lastname="Doe", address="123 Main St.")
>>> s.save()
>>> Student.get("address", lastname="Doe")
['123 Main St.']
```
