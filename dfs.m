adj = [
    [0, 1, 1, 0],
    [1, 0, 0, 1],
    [1, 0, 0, 0],
    [0, 1, 0, 0]
];

dfs = (m, n, u, vs) -> {
  if (vs[0, u] == 0) {
    vs[0, u] = 1;
    print u;
    for i = 0:(n-1) {
      if(m[u, i] == 1) {
        if(vs[0, i] == 0) {
          n_vs = dfs(m, n, i, vs);
          vs = n_vs;
        }
      }
    }
    print "Exitting", u;
    return vs;
  }
};

dfs(adj, 4, 0, [0,0,0,0]);
print "PROGRESS";
