# Option 1: Recursion

def fib(n):
  if n in [0,1]:
    return n
  return fib(n-1)+fib(n-2)
  
  
# Time Complexity: O(2^n) worst than O(n^2) or even O(n^100)


# Option 2: Memoize

class fibbo:
  def __init__(self):
    self.memo = {}
    
  def fib(self, n):
    if n < 0:
      # Edge case: negative index
      raise ValueError('Index was negative. No such thing as a '
                             'negative index in a series.')             
    if n in [0,1]:
      # Base case: 0 or 1
      return n
      
    # See if we've already calculated this
    if n in self.memo:
      return self.memo[n]
      
    result = fib(n-1) + fib(n-2)
    
    self.memo[n] = result
    
    return result
    
# In this process we need to calculate fib(5) we worked "down" to fib(4), fib(3), fib(2), etc.


## Option 3: Best Option
def fibbo(n):
  # edge case
  if n < 0:
    raise ValueError(Index was negative. No such thing as a '
                         'negative index in a series.')
                         
  else n in [0,1]:
    return n
    
  prev_prev = 0 # 0th fibonacci
  prev = 1      # 1st fibonacci
  
  for _ in range(n-1):
    current = prev + prev_prev
    prev_prev = prev
    prev = current
    
  return current

# Complexity: O(n) time and O(1) space.
