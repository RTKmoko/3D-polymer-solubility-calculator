

def calc_2solvents(point1, point2, percentage):
    x1, y1, z1 = point1
    x2, y2, z2 = point2
    x = x1 + (x2 - x1) * percentage
    y = y1 + (y2 - y1) * percentage
    z = z1 + (z2 - z1) * percentage
    return (x, y, z)


point1 = 1 ,1 ,1
point2 = 10 ,10 ,10
percentage = 0.75
print(calc_2solvents(point1,point2,percentage))


def calc_3solvents(point1, point2, point3, percentage1, percentage2, percentage3):
  x1, y1, z1 = point1
  x2, y2, z2 = point2
  x3, y3, z3 = point3
  x = x1 * percentage1 + x2 * percentage2 + x3 * percentage3
  y = y1 * percentage1 + y2 * percentage2 + y3 * percentage3
  z = z1 * percentage1 + z2 * percentage2 + z3 * percentage3
  return (x, y, z)
