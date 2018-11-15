import sys
# from IPython.display import HTML
from ortools.constraint_solver import pywrapcp

def us_map_coloring(colors, optimize=False):
    # US adjagency matrix
    us_adj = {
      'Alaska': [], 
      'Alabama': ['Mississippi', 'Tennessee', 'Georgia', 'Florida'], 
      'Arkansas': ['Missouri', 'Tennessee', 'Mississippi', 'Louisiana', 'Texas', 'Oklahoma'], 
      'Arizona': ['California', 'Nevada', 'Utah', 'Colorado', 'New Mexico'], 
      'California': ['Oregon', 'Nevada', 'Arizona'], 
      'Colorado': ['Wyoming', 'Nebraska', 'Kansas', 'Oklahoma', 'New Mexico', 'Arizona', 'Utah'], 
      'Connecticut': ['New York', 'Massachusetts', 'Rhode Island'], 
      'District of Columbia': ['Maryland', 'Virginia'], 
      'Delaware': ['Maryland', 'Pennsylvania', 'New Jersey'], 
      'Florida': ['Alabama', 'Georgia'], 
      'Georgia': ['Florida', 'Alabama', 'Tennessee', 'North Carolina', 'South Carolina'], 
      'Hawaii': [], 
      'Iowa': ['Minnesota', 'Wisconsin', 'Illinois', 'Missouri', 'Nebraska', 'South Dakota'], 
      'Idaho': ['Montana', 'Wyoming', 'Utah', 'Nevada', 'Oregon', 'Washington'], 
      'Illinois': ['Indiana', 'Kentucky', 'Missouri', 'Iowa', 'Wisconsin'], 
      'Indiana': ['Michigan', 'Ohio', 'Kentucky', 'Illinois'], 
      'Kansas': ['Nebraska', 'Missouri', 'Oklahoma', 'Colorado'], 
      'Kentucky': ['Indiana', 'Ohio', 'West Virginia', 'Virginia', 'Tennessee', 'Missouri', 'Illinois'], 
      'Louisiana': ['Texas', 'Arkansas', 'Mississippi'], 
      'Massachusetts': ['Rhode Island', 'Connecticut', 'New York', 'New Hampshire', 'Vermont'], 
      'Maryland': ['Virginia', 'West Virginia', 'Pennsylvania', 'District of Columbia', 'Delaware'], 
      'Maine': ['New Hampshire'],
      'Michigan': ['Wisconsin', 'Indiana', 'Ohio'], 
      'Minnesota': ['Wisconsin', 'Iowa', 'South Dakota', 'North Dakota'], 
      'Missouri': ['Iowa', 'Illinois', 'Kentucky', 'Tennessee', 'Arkansas', 'Oklahoma', 'Kansas', 'Nebraska'], 
      'Mississippi': ['Louisiana', 'Arkansas', 'Tennessee', 'Alabama'], 
      'Montana': ['North Dakota', 'South Dakota', 'Wyoming', 'Idaho'], 
      'North Carolina': ['Virginia', 'Tennessee', 'Georgia', 'South Carolina'], 
      'North Dakota': ['Minnesota', 'South Dakota', 'Montana'], 
      'Nebraska': ['South Dakota', 'Iowa', 'Missouri', 'Kansas', 'Colorado', 'Wyoming'], 
      'New Hampshire': ['Vermont', 'Maine', 'Massachusetts'], 
      'New Jersey': ['Delaware', 'Pennsylvania', 'New York'], 
      'New Mexico': ['Arizona', 'Utah', 'Colorado', 'Oklahoma', 'Texas'], 
      'Nevada': ['Idaho', 'Utah', 'Arizona', 'California', 'Oregon'], 
      'New York': ['New Jersey', 'Pennsylvania', 'Vermont', 'Massachusetts', 'Connecticut'], 
      'Ohio': ['Pennsylvania', 'West Virginia', 'Kentucky', 'Indiana', 'Michigan'], 
      'Oklahoma': ['Kansas', 'Missouri', 'Arkansas', 'Texas', 'New Mexico', 'Colorado'], 
      'Oregon': ['California', 'Nevada', 'Idaho', 'Washington'], 
      'Pennsylvania': ['New York', 'New Jersey', 'Delaware', 'Maryland', 'West Virginia', 'Ohio'], 
      'Rhode Island': ['Connecticut', 'Massachusetts'], 
      'South Carolina': ['Georgia', 'North Carolina'], 
      'South Dakota': ['North Dakota', 'Minnesota', 'Iowa', 'Nebraska', 'Wyoming', 'Montana'], 
      'Tennessee': ['Kentucky', 'Virginia', 'North Carolina', 'Georgia', 'Alabama', 'Mississippi', 'Arkansas', 'Missouri'], 
      'Texas': ['New Mexico', 'Oklahoma', 'Arkansas', 'Louisiana'], 
      'Utah': ['Idaho', 'Wyoming','Colorado', 'New Mexico', 'Arizona', 'Nevada'], 
      'Virginia': ['North Carolina', 'Tennessee', 'Kentucky', 'West Virginia', 'Maryland', 'District of Columbia'], 
      'Vermont': ['New York', 'New Hampshire', 'Massachusetts'], 
      'Washington': ['Idaho', 'Oregon'], 
      'Wisconsin': ['Michigan', 'Minnesota', 'Iowa', 'Illinois'], 
      'West Virginia': ['Ohio', 'Pennsylvania', 'Maryland', 'Virginia', 'Kentucky'], 
      'Wyoming': ['Montana', 'South Dakota', 'Nebraska', 'Colorado', 'Utah', 'Idaho']
    }
    # state -> index
    state_ids = dict(zip(us_adj.keys(), range(len(us_adj.keys()))))
    # index -> state
    state_names = list(us_adj.keys())
    # -----

    n = len(us_adj.keys())
    num_colors = len(colors)
    # set of nodes
    V = range(n)

    solver = pywrapcp.Solver('Map coloring')

    # Adj. matrix creation
    E = []
    num_edges = 0
    for src_idx in V:
      for dst_name in us_adj[state_names[src_idx]]:
        E.append([src_idx,state_ids[dst_name]])
        num_edges = num_edges + 1

    # Decision variables
    x = [solver.IntVar(0, num_colors - 1, 'x[%i]' % i) for i in V]
    max_color = solver.Max(x).Var()

    # Constraints
    # 1. Adjacent nodes cannot be assigned the same color
    #    (and adjust to 0-based)
    for i in range(num_edges):
        solver.Add(x[E[i][0]] != x[E[i][1]])
    # 2. Symmetry breaking
    # for i in range(num_colors):
    #   solver.Add(x[i] <= i+1)
    
    # Objective
    if optimize:
      objective = solver.Minimize(max_color, 1)

    # Solution
    solution = solver.Assignment()
    solution.Add(x)
    solution.Add(max_color)

    decision_builder = solver.Phase(x,
                      solver.INT_VAR_SIMPLE,
                      # assinging max values makes difference mode evident
                      solver.ASSIGN_MIN_VALUE)
    
    if optimize:
      collector = solver.LastSolutionCollector(solution)
      collector.AddObjective(max_color)
      solver.Solve(decision_builder, [objective, collector])
    else:
      collector = solver.FirstSolutionCollector(solution)
      solver.Solve(decision_builder, collector)

    if collector.SolutionCount() > 0:
      best_solution = collector.SolutionCount() - 1
      num_colors = collector.Value(best_solution, max_color) + 1
      print("Num. colors:", num_colors)
      # print("x:", [collector.Value(best_solution, x[i]) for i in V])
      # print()
      map_colors = dict()
      for i in V:
        map_colors[state_names[i]] = colors[collector.Value(best_solution, x[i])]
      return map_colors, num_colors
    else:
      return None, 0
      
def nqueens(n):
  solver = pywrapcp.Solver("n Queens")

  # declare variables
  q = [solver.IntVar(0, n - 1, "x%i" % i) for i in range(n)]

  # constraints
  solver.Add(solver.AllDifferent(q))
  for i in range(n):
      for j in range(i):
          solver.Add(q[i] != q[j])
          solver.Add(q[i] + i != q[j] + j)
          solver.Add(q[i] - i != q[j] - j)

  # solution and search
  solution = solver.Assignment()
  solution.Add([q[i] for i in range(n)])

  # Collector to get all solutions
  collector = solver.AllSolutionCollector(solution)

  solver.Solve(
    solver.Phase([q[i] for i in range(n)], solver.INT_VAR_SIMPLE,
                solver.ASSIGN_MIN_VALUE), [collector])

  if collector.SolutionCount()<1:
    return None

  solutions = []
  for i in range(collector.SolutionCount()):
    solutions.append([collector.Value(i, q[j]) for j in range(n)])
  return solutions

# def nqueens_matrix(n):
#   def var_idx(i, j):
#     return n*j+i
#   solver = pywrapcp.Solver("n Queens Matrix")

#   # declare variables
#   q = [solver.IntVar(0, 1, "x%i" % i) for i in range(n*n)]

#   # Constraints
#   for i in range(n):
#     solver.Add(solver.AllDifferent( [q[var_idx(i,j)] for j in range(n)] ))
#     solver.Add(solver.AllDifferent( [q[var_idx(j,i)] for j in range(n)] ))

#   for d in range(2, 2*n - 1):
#     solver.Add(solver.AllDifferent( [q[var_idx(i, d-i)]    for i in range(n) if d-i >= 0 and d-i <= n-1] ))
#     solver.Add(solver.AllDifferent( [q[var_idx(n-i, d-i)]  for i in range(n) if d-i >= 0 and d-i <= n-1] ))
    
#   # solution and search
#   solution = solver.Assignment()
#   solution.Add([q[i] for i in range(n)])

#   # Collector to get all solutions
#   collector = solver.AllSolutionCollector(solution)

#   solver.Solve(
#     solver.Phase([q[i] for i in range(n)], solver.INT_VAR_SIMPLE,
#                 solver.ASSIGN_MIN_VALUE), [collector])

#   if collector.SolutionCount()<1:
#     return None

#   solutions = []
#   for i in range(collector.SolutionCount()):
#     solutions.append([collector.Value(i, q[j]) for j in range(n)])
#   return solutions

if __name__ == '__main__':
  # colors = [
  # 'red', 
  # 'green', 
  # 'blue', 
  # '#6f2da8', #Grape
  # '#ffbf00', #Amber
  # '#01796f', #Pine
  # '#813f0b', #Clay
  # '#ff2000', #yellow
  # '#ff66cc', #pink
  # '#d21f3c' #raspberry
  # ]
  # map_colors = us_map_coloring(colors, optimize=True)

  sols = nqueens(4)
  print(sols)