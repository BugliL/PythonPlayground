import math


def optimize1(Y, P, fn, eps=0.01, ):
    d = lambda x, y: abs(x - y)

    S = 100
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
    d = lambda x, y: abs(x - y)

    S = 100
    c = 0
    old_distance = 10000
    STEP = 2

    progress = True
    while d(fn(P), Y) > eps and progress:
        c += 1
        P += S
        current_distance = d(fn(P), Y)

        if current_distance > old_distance:
            S /= -STEP

        progress = d(old_distance, current_distance)
        old_distance = current_distance

    return c, round(P, 3)


def search_interval_zero(P, fn):
    c = 0
    x0, x1 = P, P
    Y0, Y1 = fn(x0), fn(x1)
    V0, V1 = sorted((Y0, Y1))
    while not (V0 <= 0 <= V1):
        c += 1
        x0, x1 = x0 - (P * 0.1), x1 + (P * 0.1)
        Y0, Y1 = fn(x0), fn(x1)
        V0, V1 = sorted((Y0, Y1))

        # print("(x0, x1) = ", (x0, x1))
    return c, sorted((x0, x1))


def secants(Y, P, fn, eps=0.01, ):
    d = lambda x, y: abs(x - y)
    fn_ = lambda x: Y - fn(x)

    value = P * 0.1
    x0, x1 = P - value, P + value
    x = x0
    den = (fn_(x1) - fn_(x0))
    c = 0

    while d(fn_(x), Y) >= eps and abs(den) > eps:  # and is_iterating(x, x1):
        x = x1 - fn_(x1) * (x1 - x0) / den
        x0, x1 = x1, x

        c += 1
        den = (fn_(x1) - fn_(x0))

    return c, round(x, 3)


def bisection_method(Y, P, fn, eps=0.01, ):
    fn_ = lambda x: Y - fn(x)
    sign = lambda x: math.copysign(1, x)
    d = lambda x, y: abs(x - y)
    c, (a, b) = search_interval_zero(P, fn_)

    x = a + b / 2
    while d(fn_(x), Y) >= eps and d(a, b) > eps:
        c += 1
        x = (a + b) * 0.5
        a, b = (x, b) if sign(fn_(x)) == sign(fn_(a)) else (a, x)
        # print(locals())

    return c, round(x, 3)


if __name__ == '__main__':

    def run_optiomize(algoritm):
        TPL = "{:>4}{:>15}{:>15}{:>15}{:>15}{:>10}{:>10}"

        print(TPL.format("index", "iter", "result", "fn(result)", "Y", "gap", "x0"))

        function_list = {
            1: lambda x: x ** 2,
            2: lambda x: x * 2,
            3: lambda x: x * 0.0031,
            4: lambda x: x ** 3,
            # 5: lambda x: 4 * (x ** (1 / 3)),
            # 6: lambda x: math.log(x),
            # 7: lambda x: math.exp(x),
        }

        Y = 127
        x0 = 20
        for index, fn in function_list.items():
            try:
                iterations, result = algoritm(
                    Y=Y,
                    P=x0,
                    fn=fn
                )
            except Exception as e:
                # raise (e)
                error_string = 'ERR'
                print(TPL.format(index, error_string, error_string, error_string))
            else:
                print(TPL.format(
                    index,
                    iterations,
                    result,
                    round(fn(result), 6),
                    Y,
                    abs(round(fn(result) - Y, 1)),
                    x0,
                ))


    functions_dict = {
        "First": optimize1,
        "Second": optimize2,
        "Secants": secants,
        "Bisection": bisection_method,
    }

    for name, function in functions_dict.items():
        print(name)
        run_optiomize(function)
        print("\n\n")
