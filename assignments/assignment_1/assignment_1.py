def colorGraph(N, E, C):
  import mip
  model = mip.Model("GraphColouring")
  model.verbose = 0 # turn off Cbc console logs
  x=[[model.add_var(var_type=mip.BINARY, name=f"x_{i}_{c}") for c in range(len(C))] for i in range(N)]
  for i in range(N):
    model += mip.xsum(x[i]) == 1
  for e in E:
    for c in range(len(C)):
      model += x[e[0]][c] + x[e[1]][c] <= 1
  model.objective = mip.minimize(mip.xsum([C[c] * x[i][c] for c in range(len(C)) for i in range(N)]))
  model.optimize()
  model.write("graph_colouring.lp")
  if model.status == mip.OptimizationStatus.OPTIMAL:
    return [c for i in range(N) for c in range(len(C)) if x[i][c].x >= 0.9]
  return []

def mds(N, E):
    import mip
    model = mip.Model("MinimumDominatingSet")
    model.verbose = 0  # turn off solver logs

    # x[i] = 1 if vertex i is in the dominating set
    x = [model.add_var(var_type=mip.BINARY,
                       name=f"x_{i}") for i in range(N)]

    # minimize number of dominating vertices
    model.objective = mip.minimize(mip.xsum(x))

    # build neighbor list
    nbr = [[] for _ in range(N)]
    for (u, v) in E:
        nbr[u].append(v)
        nbr[v].append(u)

    # domination constraints
    for i in range(N):
        model += x[i] + mip.xsum(x[j] for j in nbr[i]) >= 1

    model.optimize()
    model.write("dominating_vertex.lp")

    if model.status == mip.OptimizationStatus.OPTIMAL:
        return [i for i in range(N) if x[i].x > 0.9]

    return []

def mwis(N, E, W):
    import mip
    model = mip.Model("MWIS")
    model.verbose = 0  # turn off solver logs

    # x[i] = 1 if vertex i is selected
    x = [model.add_var(var_type=mip.BINARY,
                       name=f"x_{i}") for i in range(N)]

    # maximize total weight
    model.objective = mip.maximize(
        mip.xsum(W[i] * x[i] for i in range(N))
    )

    # independence constraints: no adjacent vertices together
    for (u, v) in E:
        model += x[u] + x[v] <= 1

    model.optimize()
    model.write("independent_set.lp")

    if model.status == mip.OptimizationStatus.OPTIMAL:
        return [i for i in range(N) if x[i].x > 0.9]

    return []