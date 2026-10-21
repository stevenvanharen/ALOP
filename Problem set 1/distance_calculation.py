import math
m_vega = 0

def distance(m1, m2, distance2):
    return math.sqrt(math.pow(100,(m1-m2)/5)) * distance2    

def uncert(m1, m2):    
    return (2*math.log(10)/5) * math.pow(100,(m1-m2)/5)

def distance_absolute_magnitude(m, M):
    return math.pow(10, (m-M+5)/5)

m1 = 8.978 #mb of vega-like star
sigmam1 = 0.018 
dinstance2 = 7.75 #vega distance

d_vega_like = distance(m1,0,dinstance2)
print(d_vega_like)
sigma_d = uncert(m1,0)*sigmam1
print(sigma_d)

M_V = 1.05
d_vega_like_M = distance_absolute_magnitude(m1, M_V)
print(d_vega_like_M)

