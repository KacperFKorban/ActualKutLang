apply = (f, x) -> {
  return f(x);
};

inc = (a) -> {
  return a+1;
};

b = apply(inc, 1);

print b;

m = [1,2,3,4];

print m[2];