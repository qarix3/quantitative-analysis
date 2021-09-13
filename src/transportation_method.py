import numpy as np
from collections import Counter


def transport(supply, demand, costs, init_method="LCM"):

    # Only solves balanced problem
    assert sum(supply) == sum(demand)
    assert init_method in ["LCM", "NCM", "VOGEL"]

    s = np.copy(supply)
    d = np.copy(demand)
    C = np.copy(costs)
    has_degenerated_init_solution = False
    has_degenerated_mid_solution = True
    has_unique_solution = True

    n, m = C.shape

    # Finding initial solution
    X = np.full((n, m), np.nan)
    allow_fill_X = np.ones((n, m), dtype=bool)
    indices = [(i, j) for i in range(n) for j in range(m)]

    def _fill_zero_indice(i, j):
        allow_fill_X[i, j] = False
        allowed_indices_i = [
            (i, jj) for jj in range(m)
            if allow_fill_X[i, jj]]
        allowed_indices_j = [
            (ii, j) for ii in range(n)
            if allow_fill_X[ii, j]]
        allowed_indices = allowed_indices_i + allowed_indices_j
        if allowed_indices:
            return allowed_indices[0]
        else:
            return None

    if init_method == "VOGEL":
        # vogel
        n_iter = 0
        while n_iter < m + n - 1:
            row_diff = np.array([np.nan]*n)
            col_diff = np.array([np.nan]*m)
            for i in range(n):
                row_allowed = []
                for j in range(m):
                    if allow_fill_X[i, j]:
                        row_allowed.append(C[i, j])
                row_allowed_sorted = sorted(row_allowed)
                try:
                    row_diff[i] = abs(
                        row_allowed_sorted[0] - row_allowed_sorted[1])
                except:
                    # only one element in row_allowed_sorted
                    row_diff[i] = np.nan
            for j in range(m):
                col_allowed = []
                for i in range(n):
                    if allow_fill_X[i, j]:
                        col_allowed.append(C[i, j])
                col_allowed_sorted = sorted(col_allowed)
                try:
                    col_diff[j] = abs(
                        col_allowed_sorted[0] - col_allowed_sorted[1])
                except:
                    # only one element in row_allowed_sorted
                    col_diff[j] = np.nan

            try:
                diff = np.concatenate((row_diff, col_diff))
                max_diff_index = np.nanargmax(diff)
                max_diff = diff[max_diff_index]
            except:
                max_diff = None

            if max_diff:
                located = False
                while not located:
                    for i in range(n):
                        if row_diff[i] == max_diff:
                            located = True
                            located_type = "row"
                            located_index = i
                            break
                    for j in range(m):
                        if col_diff[j] == max_diff:
                            located = True
                            located_type = "col"
                            located_index = j
                            break

                assert isinstance(located_index, int)
                assert located_type in ["row", "col"]

                if located_type == "row":
                    row_indices = [(located_index, j) for j in range(
                        m) if allow_fill_X[located_index, j]]
                    row_values = [C[located_index, j]
                                  for j in range(m) if allow_fill_X[located_index, j]]
                    xs = sorted(zip(row_indices, row_values), key=lambda (a, b): b)
                else:
                    col_indices = [(i, located_index) for i in range(
                        n) if allow_fill_X[i, located_index]]
                    col_values = [C[i, located_index]
                                  for i in range(n) if allow_fill_X[i, located_index]]
                    xs = sorted(zip(col_indices, col_values), key=lambda (a, b): b)

                (i, j), _ = xs[0]

            # there's the last cell needed to be filled.
            else:
                xs = [(i, j) for i in range(n)
                      for j in range(m) if allow_fill_X[i, j]]
                (i, j) = xs[0]

            #(i, j), _ = xs[0]
            assert allow_fill_X[i, j]
            grabbed = min([s[i], d[j]])
            X[i, j] = grabbed

            # *both* supply i and demand j is met
            if s[i] == grabbed and d[j] == grabbed:
                fill_zero_indices = _fill_zero_indice(i, j)
                if fill_zero_indices:
                    # fill a 0 in X with allowed_indices
                    X[fill_zero_indices] = 0
                    allow_fill_X[fill_zero_indices] = False
                    n_iter += 1
                    has_degenerated_init_solution = True

            s[i] -= grabbed
            d[j] -= grabbed

            if d[j] == 0:
                allow_fill_X[:, j] = False
            if s[i] == 0:
                allow_fill_X[i, :] = False

            n_iter += 1

    else:

        if init_method == "LCM":
            # Least-Cost method
            xs = sorted(zip(indices, C.flatten()), key=lambda (a, b): b)
        elif init_method == "NCM":
            # Northwest Corner Method
            xs = sorted(zip(indices, C.flatten()), key=lambda (a, b): (a[0], a[1]))

        # Iterating C elements in increasing order
        for (i, j), _ in xs:
            grabbed = min([s[i], d[j]])

            # supply i or demand j has been met
            if grabbed == 0:
                continue

            # X[i,j] is has been filled
            elif not np.isnan(X[i, j]):
                continue
            else:
                X[i, j] = grabbed

                # *both* supply i and demand j is met
                if s[i] == grabbed and d[j] == grabbed:
                    fill_zero_indices = _fill_zero_indice(i, j)
                    if fill_zero_indices:
                        # fill a 0 in X with allowed_indices
                        X[fill_zero_indices] = 0
                        allow_fill_X[fill_zero_indices] = False
                        has_degenerated_init_solution = True

                s[i] -= grabbed
                d[j] -= grabbed

            if d[j] == 0:
                allow_fill_X[:, j] = False
            if s[i] == 0:
                allow_fill_X[i, :] = False

    # Finding optimal solution
    while True:
        u = np.array([np.nan]*n)
        v = np.array([np.nan]*m)
        S = np.full((n, m), np.nan)

        _x, _y = np.where(~np.isnan(X))
        basis = zip(_x, _y)
        f = basis[0][0]
        u[f] = 0

        # Finding u, v potentials
        while any(np.isnan(u)) or any(np.isnan(v)):
            for i, j in basis:
                if np.isnan(u[i]) and not np.isnan(v[j]):
                    u[i] = C[i, j] - v[j]
                elif not np.isnan(u[i]) and np.isnan(v[j]):
                    v[j] = C[i, j] - u[i]
                else:
                    continue

        # Finding S-matrix
        for i in range(n):
            for j in range(m):
                if np.isnan(X[i, j]):
                    S[i, j] = C[i, j] - u[i] - v[j]

        # Stop condition
        s = np.nanmin(S)
        print S
        if s > 0:
            break
        elif s == 0:
            has_unique_solution = False
            break

        i, j = np.argwhere(S == s)[0]
        start = (i, j)

        # Finding cycle elements
        T = np.zeros((n, m))

        # Element with non-nan value are set as 1
        for i in range(0, n):
            for j in range(0, m):
                if not np.isnan(X[i, j]):
                    T[i, j] = 1

        T[start] = 1
        while True:
            _xs, _ys = np.nonzero(T)
            xcount, ycount = Counter(_xs), Counter(_ys)

            for x, count in xcount.items():
                if count <= 1:
                    T[x, :] = 0
            for y, count in ycount.items():
                if count <= 1:
                    T[:, y] = 0

            if all(x > 1 for x in xcount.values()) \
                    and all(y > 1 for y in ycount.values()):
                break

        # Finding cycle chain order
        def dist((x1, y1), (x2, y2)): return (abs(x1-x2) + abs(y1-y2)) \
            if ((x1 == x2 or y1 == y2) and not (x1 == x2 and y1 == y2)) else np.inf
        fringe = set(tuple(p) for p in np.argwhere(T > 0))

        size = len(fringe)

        path = [start]
        while len(path) < size:
            last = path[-1]
            if last in fringe:
                fringe.remove(last)
            next = min(fringe, key=lambda (x, y): dist(last, (x, y)))
            path.append(next)

        # Improving solution on cycle elements
        neg = path[1::2]
        pos = path[::2]
        q = min(X[zip(*neg)])
        if q == 0:
            has_degenerated_mid_solution = True
        X[start] = 0
        X[zip(*neg)] -= q
        X[zip(*pos)] += q

        # set the first element with value 0 as nan
        for ne in neg:
            if X[ne] == 0:
                X[ne] = np.nan
                break

    # for calculation of total cost
    X_final = np.copy(X)
    for i in range(0, n):
        for j in range(0, m):
            if np.isnan(X_final[i, j]):
                X_final[i, j] = 0

    return X, np.sum(X_final*C), has_degenerated_init_solution,\
        has_degenerated_mid_solution, has_unique_solution


if __name__ == '__main__':
    supply = np.array([105, 125, 70])
    demand = np.array([80, 65, 70, 85])

    costs = np.array([[9., 10., 13., 17.],
                      [7., 8., 14., 16.],
                      [20., 14., 8., 14.]])

    routes, z, \
        has_degenerated_init_solution, \
        has_degenerated_mid_solution, \
        has_unique_solution = transport(
            supply, demand, costs, init_method="VOGEL")
    # print routes, z, has_degenerated_init_solution, has_degenerated_mid_solution, has_unique_solution
    assert z == 3125
    assert has_degenerated_init_solution, has_degenerated_mid_solution
    assert not has_unique_solution
