P = [[
   6, [], [],
   9, [],  3,
  [], [], []
], [
  [], [], [],
  [], [],  8,
   6,  5, []
], [
   3, [], [],
  [],  6, [],
   7, [], []
], [
  [],  1,  9,
  [], [], [],
  [], [],  5
], [
   4, [], [],
  [],  9, [],
  [], [],  7
], [
   6, [], [],
  [], [], [],
   1,  3, []
], [
  [], [],  1,
  [],  9, [],
  [], [],  6
], [
  [],  2,  4,
   7, [], [],
  [], [], []
], [
  [], [], [],
   4, [],  2,
  [], [],  3
]]

def get_row(P, row_num):
  row = []
  group_start = row_num / 3 * 3
  group_end = group_start + 3
  row_start = row_num % 3 * 3
  row_end = row_start + 3
  for group in P[group_start:group_end]:
    row += group[row_start:row_end]
  return row

def get_col(P, col_num):
  col = []
  groups = [ P[i] for i in range(col_num / 3, 9, 3) ]
  for group in groups:
    col += [ group[i] for i in range(col_num % 3, 9, 3) ]
  return col

def calc_possibilities(P):
  for group in P:
    for i in range(len(P)):
      row_num = i / 3
      col_num = i % 3
