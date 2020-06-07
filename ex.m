x = zeros(2);
y = zeros(2);
x[0,0] = 1;
z = x + y;

w = x*y;

add = (a, b) -> {
  return a + b;
};

print(add(1,2));
