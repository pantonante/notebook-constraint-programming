import time
from constraints import all_different


class nqueens():
    def __init__(self, N):
        self.N = N
        self.assignment = [None] * self.N
        self.domain = [set(range(N))] * N
        self.consistency_checks = 0

    def is_solution(self):
        """ Check that the current instance is a solution """
        return (self.get_unassigned() is None) and self.is_feasible()

    def get_domain(self, var):
        """ Get domain of variable var """
        return self.domain[var]

    def get_unassigned(self):
        """ Return the first unassigned variable, None otherwise """
        return next((var for var in range(self.N) if self.assignment[var] is None), None)

    def is_feasible(self):
        """ Check that the current instance satisfy all constraints """
        diag_1 = [(self.assignment[i] + i) if (self.assignment[i] is not None) else None for i in range(self.N)]
        diag_2 = [(self.assignment[i] - i) if (self.assignment[i] is not None) else None for i in range(self.N)]
        return self.is_consistent() and \
            all_different(self.assignment) and \
            all_different(diag_1) and \
            all_different(diag_2)

    def assign(self, var, value, with_pruning=False):
        """
        Assign value to var and optionally apply arc concistency
        """
        self.assignment[var] = value
        if with_pruning:
            return self.prune_domain(var, value)
        return self.domain

    def is_consistent(self):
        """ Check that all domains are non-empty """
        return all([len(dom) > 0 for dom in self.domain])

    def prune_domain(self, var, val):
        """ Apply arc-consistency.
        Return
            - old_domain: domain before arc-consistency
        """
        old_domain = self.domain.copy()
        self.domain[var] = {val}
        for x in range(self.N):
            if x == var:
                continue
            for v in self.domain[x]:
                # Constraint: alldifferent(q)
                if v == val:
                    self.domain[x] = self.domain[x] - {v}
                    self.consistency_checks = self.consistency_checks + 1
                    if len(self.domain[x]) == 0:
                        return old_domain
                # Constraint: alldifferent(q[i] + i)
                if v + x == val + var:
                    self.domain[x] = self.domain[x] - {v}
                    self.consistency_checks = self.consistency_checks + 1
                    if len(self.domain[x]) == 0:
                        return old_domain
                # Constraint: alldifferent(q[i] - i)
                if v - x == val - var:
                    self.domain[x] = self.domain[x] - {v}
                    self.consistency_checks = self.consistency_checks + 1
                    if len(self.domain[x]) == 0:
                        return old_domain
        return old_domain

    def restore_domain(self, domain):
        self.domain = domain.copy()

    def print(self):
        for col in range(self.N):
            for row in range(self.N):
                if self.assignment[col] == row:
                    print('Q', end=' ')
                else:
                    print('-', end=' ')
            print('')


def backtrack(csp, with_forward_checking=False):
    if csp.is_solution():
        return csp

    var = csp.get_unassigned()
    for val in csp.get_domain(var):
        pruned = csp.assign(var, val, with_forward_checking)
        if csp.is_feasible():
            bt = backtrack(csp, with_forward_checking)
            if bt is not None:
                return bt
        csp.restore_domain(pruned)
    csp.assign(var, None)
    return None

def nqueens_backtracking(N):
    start_time = time.time()
    queens = backtrack(nqueens(N))
    end_time = time.time()
    return queens, (end_time - start_time)


def nqueens_backtracking_fc(N):
    start_time = time.time()
    queens = backtrack(nqueens(N), True)
    end_time = time.time()
    return queens, (end_time - start_time)


def main():
    N = 12

    queens, exec_time = nqueens_backtracking(N)
    if queens is not None:
        queens.print()
        print("Solution found in %.2f seconds. Used %d consistency checks." \
              % (exec_time, queens.consistency_checks))
    else:
        print("Inconsistent problem")

    print('===============================================================')

    queens, exec_time = nqueens_backtracking_fc(N)
    if queens is not None:
        queens.print()
        print("Solution found in %.2f seconds. Used %d consistency checks." \
              % (exec_time, queens.consistency_checks))
    else:
        print("Inconsistent problem")


if __name__ == "__main__":
    main()
