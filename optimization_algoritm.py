def optimize1(Y, P, fn, eps=0.01, ):
    S = 0.1
    d = lambda x, y: abs(x - y)
    z = 1  # last is increment
    c = 0
    while d(fn(P), Y) > eps:
        c += 1
        a, b = P + S, P - S
        if d(fn(a), Y) < d(fn(b), Y):
            P = a
            if z == -1:
                z = 1
                S /= 2
        else:
            P = b
            if z == 1:
                z = -1
                S /= 2

    return c, round(P, 3)


def optimize2(Y, P, fn, eps=0.01, ):
    pass


if __name__ == '__main__':

    function_list = [
        lambda x: x ** 2,
        lambda x: x * 2,
        lambda x: x * 0.0031,
    ]

    for fn in function_list:
        iterations, result = optimize1(
            Y=61,
            P=2,
            fn=fn
        )

        print(iterations, result, fn(result))
