def my_generator():
    yield 1
    yield 2
    return [1, 2, 3, 4, 5]


a = my_generator()
try:
    while True:
        print(next(a))
except StopIteration as e:
    print(e.value)
