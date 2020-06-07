A = zeros(5,7);
B = ones(7,5);
I = eye(10);
D1 = A.+B' ;
D2 = A.-B' ;
D3 = A.*B' ;
D3 = A*B' ; # ERROR
D3 = A*B ;
D4 = A./B' ;

x = 7.5;
A[1,2] += 2;
A[0,0] = x + 3;