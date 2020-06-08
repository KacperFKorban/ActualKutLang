is_palindrome = (arr, n) -> {
  res = 1;
  for i = 0:(n-1) {
    if(arr[i] != arr[n-i-1]) {
      res = 0;
    }
  }
  return res;
};

a1 = [1,2,3,4];
a2 = [1,2,2,1];
a3 = [1,2,1];

print is_palindrome(a1, 4);
print is_palindrome(a2, 4);
print is_palindrome(a3, 3);
