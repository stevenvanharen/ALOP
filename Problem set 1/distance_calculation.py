import math
m_vega = 0

def distance(m1, m2, distance2):
    return math.sqrt(math.pow(100,(m1-m2)/5)) * distance2    

m1 = 7.230 #mb of vega-like star
dinstance2 = 7.75 #vega distance

d_vega_like = distance(m1,0,dinstance2)
print(d_vega_like)

#M_V determination using appendix G in Carroll and Ostlie
BminusVs = [0.341,0.542,-0.030,0.425,-0.013] 
# for main sequence
M_v = [3.4, 4.3, 1.1, 3.9, 1.3]