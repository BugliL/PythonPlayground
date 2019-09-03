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
    STEP = 100

    progress = True
    while d(fn(P), Y) > eps and progress:
        c += 1
        P += S
        current_distance = d(fn(P), Y)

        if current_distance > old_distance:
            S = -STEP
            STEP /= c

        progress = d(old_distance, current_distance)
        old_distance = current_distance

    return c, round(P, 3)


if __name__ == '__main__':

    def run_optiomize(algoritm):
        TPL = "{:>4}{:>15}{:>15}{:>15}"

        print(TPL.format("index", "iter", "result", "fn(result)"))

        function_list = {
            1: lambda x: x ** 2,
            2: lambda x: x * 2,
            3: lambda x: x * 0.0031,
        }

        for index, fn in function_list.items():
            iterations, result = algoritm(
                Y=61,
                P=2,
                fn=fn
            )

            print(TPL.format(
                index,
                iterations,
                result,
                round(fn(result), 6)
            ))

        print("\n\n")


    run_optiomize(optimize1)
    run_optiomize(optimize2)
