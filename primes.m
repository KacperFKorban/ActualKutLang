mod = (a, b) -> {
  while(a - b >= 0) {
    a = a-b;
  }
  return a;
};

is_prime = (n) -> {
  if(n <= 1) return 0;
  else {
    for i = 2:(n-1) {
      if (mod(n, i) == 0) return 0;
    }
    return 1;
  }
};

for i = 1:100 {
  print i, is_prime(i);
}