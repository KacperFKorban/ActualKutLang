abs = (a) -> {
  if (a >= 0) return a;
  else return -a;
};

min = (a, b) -> {
  if(a > b) return b;
  else return a;
};

apply = (f, x) -> {
  return f(x);
};

inc = (a) -> {
  return a+1;
};

add = (a, b) -> {
  return a+b;
};

map = (f, m, n1, n2) -> {
  m1 = m;
  for i = 0:(n1-1) {
    for j = 0:(n2-1) {
      m1[i, j] = f(m[i, j]);
    }
  }
  return m1;
};

uncurry = (f) -> {
  return (a) -> {
    return (b) -> {
      return f(a, b);
    };
  };
};

m = eye(3);
print m;

print map(inc, m, 3, 3);

print m;

print apply(inc, 1);

print add(1, 2);

uncurried = uncurry(add);
partiallyApplied = uncurried(1);
print partiallyApplied(2);

m1 = eye(3, 4);
print m1;
m2 = ones(4,3);
print m2;
print m1*m2;