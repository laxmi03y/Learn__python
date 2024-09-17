def genrator():
    i=1
    while i<=10:
        yield i
        i+=1

x=genrator()

print(next(x))
print(list(x))

