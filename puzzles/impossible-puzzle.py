import json
from collections import OrderedDict

# Set initial vars
MIN_X = 2
MAX_SUM = 100
MAX_X = MAX_SUM/2 - 1  # since y > x, x < MAX_SUM/2
X_RANGE = range(MIN_X, MAX_X+1)  # 2 to 49, inclusive

# Build possible_products and impossible_products with products that cannot and can be reached uniquely
product_range = range(MIN_X*(MIN_X+1), MAX_X*(MAX_X+1))
possible_products = OrderedDict()
impossible_products = OrderedDict()
for p in product_range:
  factor_pairs = []
  for x in X_RANGE:
    for y in range(x+1, MAX_SUM-x+1):
      if x*y == p:
        factor_pairs.append((x, y))
  if len(factor_pairs) > 1:
    possible_products[p] = factor_pairs
  elif len(factor_pairs) == 1:
    impossible_products[p] = factor_pairs[0]

print("Possible Products:")
print(json.dumps(possible_products, indent=2))

# Build possible_sums, remove sums of impossible product factor pairs
possible_sums = range(MIN_X+MIN_X+1, MAX_SUM+1)
for x,y in impossible_products.values():
  if x+y in possible_sums:
    possible_sums.remove(x+y)

print("Possible Sums:")
print(sorted(possible_sums))

# Only keep products in possible_products that can be reached from possible_sums
for p, pairs in possible_products.items():
  i = 0
  while i < len(pairs):
    if pairs[i][0] + pairs[i][1] not in possible_sums:
      del pairs[i]
      i -= 1
    i += 1
  if len(pairs) != 1:
    del possible_products[p]

print("Possible Products:")
print(json.dumps(possible_products, indent=2))

# Find occurrences of each sum
sum_occurs = OrderedDict()
for p, pairs in possible_products.items():
  for x, y in pairs:
    s = x + y
    if s in sum_occurs:
      sum_occurs[s].append((x, y))
    else:
      sum_occurs[s] = [(x, y)]

print("Sum Occurrences:")
print(json.dumps(sum_occurs, indent=2))

# The answer: the components of the sum that has only one occurrence
print("The Answer:")
try:
  print([components for s, components in sum_occurs.items() if len(sum_occurs[s]) == 1][0][0])
except:
  print "No unique answer found"
