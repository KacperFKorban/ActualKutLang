
x = 0;
y = zeros(5);
z = x + y; # ERROR

x = eye(5);
y = eye(8);
z = x + y; # ERROR

x = [ 1,2,3,4,5.5 ];
y = [ 1,2,3,4,5;
      1,2,3,4,5 ];
z = x + y; # ERROR

x = zeros(5);
y = zeros(5,7);
z = x + y; # ERROR

x = ones(3,5);