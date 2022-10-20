OFFSET = 100
MULT_FACTOR=1000

def calc_point_id(x:int,y:int, z:int)->int:
    return (x+OFFSET) * MULT_FACTOR + (y + OFFSET) * MULT_FACTOR**2 + z