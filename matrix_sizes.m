A = [1,2,3,4; 1,2,3,4;];
B = [5,6,7,8.5; 9,10,11,12];
C = A + B;
C = A - B;
D = A;
D += B;
E = A;
E -= B;
F = A * B; # ERROR
G = [1,2];
H = [1;2;];
I = G * H;
J = [1,2,3;1,2,3;1,2,3;];
K = [1,2,3];
K / J; # WARN
L = [1;2;3];
J / L; # ERROR
M = [1,2,3;1,2,3;1,2,3,4;]; # ERROR
N = [1,2,3;1,2,3;1,2,3;];
O = [1];
P = [2];
N = 4;
A .+ N; # WARN
A .- N; # WARN
A .* N; # WARN
A ./ N; # WARN
N .+ A; # WARN
N .- A; # WARN
N .* A; # WARN
N ./ A; # WARN
G .+ O; # ERROR
G .* O; # ERROR
G ./ O; # ERROR
G .- O; # ERROR
P .+ O; # WARN
P .* O; # WARN
P ./ O; # WARN
P .- O; # WARN
