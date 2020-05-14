A = zeros(4);
B = ones(4);
if (A == B) {
  print "xd";
}

if (A <= B) # ERROR
  print zeros(2);

x = 1;
y = 2;

for z = 1:10
  print z;

i = 1;
d = 100;
while (i < d) {
  if (i == x){
    return 3;
  } else if (i == 25 - 3)
    print d;
  else {
    x += y;
    if (A != B) {
      break;
    }
  }
  i = i + x;
}

i -= d;
for j = 2:100 {
  if ((1 == 1) == (2 == 2)) {
    i = 2;
  } else i = 5;
  for i = 1:5 {
    print j, i;
    ones(5); # WARN
  }
  while(i>-5.2) {
    print i;
    i -= 19;
  }
}
