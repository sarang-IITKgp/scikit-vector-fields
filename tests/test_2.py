import numpy as np
import skvf as vf
import matplotlib.pyplot as plt


# import skvf.module



# print('hahha')

# vf.plot.field_scalar()

vec1 = vf.vector(1+3j,2+2j,3+1j)
# print(vec1.elements())

vec2 = vec1.conjugate()
print(vec1.elements())
print(vec2.elements())

dot_product = vec1.dot(vec2)

mag = vec1.magnitude()

cross_vec = vec1.cross(vec2)

vec_add = vec1 + vec2
vec_sub = vec1 - vec2

vec_mul = vec1*1.5j
vec_mul2 = 1.5*vec1
cross_vec2 = vec1^vec2


print(cross_vec2.elements())
vec1.print()

print('--------Next test---------')


x = np.linspace(-5,5,50)
y = np.linspace(-5,5,40)
# x = np.linspace(-1,1,50)
# y = np.linspace(-1,1,40)
z = np.linspace(-0.5,0.5,4)

a = None

print(not isinstance(x,type(None)))

space1 = vf.space(x=x,y=y)
# space1 = vf.space(z=z,x=x,y=y)

# print('x_grid = ',space1.x_grid)
# print('y_grid = ',space1.y_grid)
# print('z_grid = ',space1.z_grid)

# print(len(np.shape(space1.z_grid)))
# print(np.shape(space1.z_grid))
print(space1.dim)

print(space1.shape)
print('-------- Test gradient ----------')


# R = np.sqrt(space1.x_grid**2 + space1.y_grid**2)

# R_vec = vf.vector(space1.x_grid,space1.y_grid,space1.z_grid)

r0_vec = vf.vector(0,0,1)

R = space1.R

R_vec = space1.vec()

# V = 1/(2*np.pi*(R_vec-r0_vec).magnitude())

r1_vec = vf.vector(-3,2,0)

# V = V - 1/(2*np.pi*(R_vec-r1_vec).magnitude())


# V = space1.y_grid**2
# V = space1.x_grid*space1.y_grid**2

# print('V =', V)
# print(np.shape(V))

print(space1.x_grid-0.75)

def potential_of_charge(q,R_vec=None,space=None,r0=vf.vector(0,0,0)):
    '''Computes and returns the electric potential of a charge, located at space0'''
    
    if R_vec == None:
        if space ==  None:
            print('At least one of R-vector or space object must be defined')
        else:
            R_vec = space.vec()
            
    V = q/(4*np.pi*vf.EPSILON_0*(R_vec-r0).magnitude())
    
    
    return V


# [dV_y, dV_x ] = np.gradient(-V)

# [dxy_grid, dx_grid] = np.gradient(space1.x_grid) 

# [dy_grid, dyx_grid] = np.gradient(space1.y_grid) 

# E_x = - dV_x/dx_grid
# E_y = - dV_y/dx_grid 

V1 = potential_of_charge(-1,space = space1,r0 = vf.vector(1,1,0))
V2 = potential_of_charge(-1,space = space1,r0 = vf.vector(-1,-2,0))
V3 = potential_of_charge(1,space = space1,r0 = vf.vector(-3,2,0))


V = V1+V2+V3


dI_vec = vf.vector(0,1,0)


Ax = 1/(4*np.pi*(R_vec-r0_vec).magnitude())*dI_vec.x
Ay = 1/(4*np.pi*(R_vec-r0_vec).magnitude())*dI_vec.y
Az = 1/(4*np.pi*(R_vec-r0_vec).magnitude())*dI_vec.z

# A_vec = 1/(4*np.pi*(R_vec-r0_vec).magnitude())*dI_vec

print('----------A_vec---------')
print(Az)
print(np.shape(Ay))

A_vec = vf.vector(Ax,Ay,Az)

H_vec = vf.curl(A_vec,space1)

# E_vec = -1*gradient_2d(V,space1)
E_vec = -vf.gradient(V,space1)

# E_x, E_y ,E_z = vf.partial_derivative(V,space1)
# E_vec_x = vf.partial_derivative(V,space1)
# E_vec_x = vf.partial_derivative(V,space1)

# E_vec = vf.vector(E_x,E_y,E_z)



div_E = vf.divergence(E_vec,space1)




# print('Ex =', E_vec.x)
# print('Ey =', E_vec.y)
# print(np.shape(E_vec.x))



# print('x = ',space1.x_grid)
# print('dx_grid = ',dx_grid)
# print('dx_y = ',dxy_grid)

# print('y = ',space1.y_grid)
# print('dy_grid = ',dy_grid)
# print('dyx_grid = ',dyx_grid)



### Plot commands

fig1 = plt.figure('2D plots')
ax1_f1 = fig1.add_subplot(111)

# ax1_f1.contour(space1.x_grid,space1.y_grid,V)
ax1_f1.set_aspect('equal')

# ax1_f1.quiver(space1.x_grid,space1.y_grid,E_x,E_y)
ax1_f1.quiver(space1.x_grid,space1.y_grid,A_vec.x,A_vec.y,units='width')
# ax1_f1.streamplot(space1.x_grid,space1.y_grid,H_vec.x,H_vec.y)
ax1_f1.streamplot(space1.x_grid,space1.y_grid,H_vec.x,H_vec.y)


fig2 = plt.figure('2D plots-div')
ax1_f2 = fig2.add_subplot(111)

ax1_f2.contour(space1.x_grid,space1.y_grid,div_E)
ax1_f2.set_aspect('equal')

# ax1_f1.quiver(space1.x_grid,space1.y_grid,E_x,E_y)
# ax1_f1.quiver(space1.x_grid,space1.y_grid,E_vec.x,E_vec.y,units='width')
ax1_f2.streamplot(space1.x_grid,space1.y_grid,E_vec.x,E_vec.y)





plt.show()


