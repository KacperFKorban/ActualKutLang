fib = (x) -> {
  if(x <= 2){
    return 1;
  } 
  else{
    return fib(x-1) + fib(x-2);
  }
};

print 1, fib(1);

print 4, fib(4);

print 5, fib(5);

print 6, fib(6);