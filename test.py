def a(n):
    if n == 1:
        return 2
    else:
        return a(n-1) + n  

print(a(10))













def find(amount):
    n = 1
    sum = 0
    while True:
        sum += a(n)
        if sum >= amount:
            rest = sum - amount
            return n-1, rest
        n += 1

