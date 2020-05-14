1 + 2 * 3 / 1; # WARN
A = [];
B = A .+ [];
C = "abc";
X = 1;
X += 2;
zeros(1); # WARN

{
    x = 1;
    a = 2;
    5; # WARN
}

print 1, 2;

for i = 1:10 {
    print i;
    x = i;
}

for i = 1:N # ERROR
  for j = i:M # ERROR
    print i, j;