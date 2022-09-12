OFFSET = 1000
MULT_FACTOR=1000000

def calc_point_id(x:int, z:int)->int:
    return (x+OFFSET) * MULT_FACTOR + z