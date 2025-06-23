def bisection(f, a, b, tol=1e-6, max_iter=100):
    if f(a) * f(b) >= 0:
        raise ValueError("f(a) dan f(b) harus memiliki tanda yang berbeda.")
    
    for i in range(max_iter):
        c = (a + b) / 2
        if abs(f(c)) < tol:
            return c, i
        elif f(a) * f(c) < 0:
            b = c
        else:
            a = c
    return c, max_iter