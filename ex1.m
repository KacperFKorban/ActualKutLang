a = 1;
m = eye(3);
print m;
print m[1, 1], 2;
m[1, 1] = 3;
print m[1, 1];

i = 2137;
print i;
for i = 1:10 {
  print i;
}

print i;

j = 1;

while(j < 10) {
  if(j != 3)
    print j;
  j += 2;
}

if (i != 2137) {
  print "Kawabanga";
} else print "XD";

print -i;

print -m;

j = 1;
# return 5;
while(j < 10) {
  j += 2;
  if(j == 5)
    continue;
  print j;
}

m1 = ones(3);
print m+m1;

print m*m1;

# print m/m1;

print 1 != 1;
print 1 == 1;

print [1] != [1];
y = 1;
for i = 1:10 {

  c=100;
  add = (a, b) -> {
    return a+b+c;
  };
  for c = 1:100 {
    print y, add(c,100);
    if(add(c, 100) == 244){
        return 2137;
    }
        
    y = y + 1;
  }
  print y;
}

print y;