# ActualKutLang

Created in cooperation with [Filip Zybała](https://github.com/pikinier20)

Usage:
```python main.py program_path```
ex. ```python main.py example.m```

Small example of valid program:
```
N = 10;
M = 20;
for i = 1:N {
    for j = i:M {
        print i, j;
    }
}

k = 20
while(k>0) {
    if(k<5)
        i = 1;
    else if(k<10)
        break;   
    else
        i = 3;
    
    k = k - 1;
}

A = zeros(5,7);
B = ones(7,5);
D1 = A .+ B';
D2 = A .- B';
D3 = A .* B';
D3 = A * B;
D4 = A ./ B';

```
