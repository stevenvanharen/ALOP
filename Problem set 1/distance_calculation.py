import math
m_vega = 0

def distance(m1, m2, distance2):
    return math.sqrt(math.pow(100,(m1-m2)/5)) * distance2    

m1 = 8.978 #mb of vega-like star
dinstance2 = 7.75 #vega distance

d_vega_like = distance(m1,0,dinstance2)
print(d_vega_like)

