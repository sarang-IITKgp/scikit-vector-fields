import numpy as np
import skvf as vf


import matplotlib.pyplot as plt
import mayavi.mlab as mlab

import sys as sys


########################################################################
################# Begin function definition ############################

def potential_of_charge(q,R_vec=None,space=None,r0=vf.entities.vector(0,0,0)):
    '''Computes and returns the electric potential of a charge, located at space0'''
    
    if R_vec == None:
        if space ==  None:
            sys.exit('At least one of R-vector or space object must be defined')
        else:
            R_vec = space.vec()
            
    V = q/(4*np.pi*vf.EPSILON_0*(R_vec-r0).magnitude())
    
    
    return V




def A_due_to_current(dI_vec,R_vec=None,space=None,r0=vf.entities.vector(0,0,0)):
    '''Computes and returns the electric potential of a charge, located at space0'''
    
    if R_vec == None:
        if space ==  None:
            print('At least one of R-vector or space object must be defined')
        else:
            R_vec = space.vec()
            
    # V = q/(4*np.pi*vf.EPSILON_0*(R_vec-r0).magnitude())
    
    Ax = vf.MU_0/(4*np.pi*(R_vec-r0).magnitude())*dI_vec.x
    Ay = vf.MU_0/(4*np.pi*(R_vec-r0).magnitude())*dI_vec.y
    Az = vf.MU_0/(4*np.pi*(R_vec-r0).magnitude())*dI_vec.z

    
    return vf.entities.vector(Ax,Ay,Az)

##################### End function definitions #########################
########################################################################


'''Create space'''
x = np.linspace(-5,5,50)
y = np.linspace(-5,5,40)
# x = np.linspace(-1,1,50)
# y = np.linspace(-1,1,40)
z = np.linspace(-5,5,40)




space1 = vf.entities.space(x=x,y=y,z=z)


R_vec = space1.vec()



V1 = potential_of_charge(-1,space = space1,r0 = vf.entities.vector(0.5,0,0))
V2 = potential_of_charge(1,space = space1,r0 = vf.entities.vector(-0.5,0,0))
# V3 = potential_of_charge(1,space = space1,r0 = vf.entities.vector(-3,2,0))


V = V1+V2 #+V3

# print('-------- Define Fields ---------')

# V1_field = 

V_field1 = vf.entities.field(V1,space1,text_tag='V1')
V_field2 = vf.entities.field(V2,space1,text_tag='V2')
# V_field = vf.entities.field(V,space1,text_tag='V1+V2')
V_field = V_field1+V_field2

E_field = -V_field.grad()

dump_field = E_field^E_field
print(dump_field.field.print())
rho_field = E_field.div()



### Plot commands

fig1 = plt.figure('2D plots')
ax1_f1 = fig1.add_subplot(111)
pts_y, pts_x, pts_z = V_field.space.shape

z_index_mid = int(pts_z/2)

ax1_f1.contourf(rho_field.space.x_grid[:,:,z_index_mid],rho_field.space.y_grid[:,:,z_index_mid],rho_field.field[:,:,z_index_mid])
ax1_f1.contour(V_field.space.x_grid[:,:,1],V_field.space.y_grid[:,:,1],V_field.field[:,:,1])
ax1_f1.set_aspect('equal')



# print(pts_x,pts_y,pts_z)

# ax1_f1.quiver(E_field.space.x_grid[:,:,z_index_mid],E_field.space.y_grid[:,:,z_index_mid],E_field.field.x[:,:,z_index_mid],E_field.field.y[:,:,z_index_mid],units='width')
ax1_f1.streamplot(E_field.space.x_grid[:,:,z_index_mid],E_field.space.y_grid[:,:,z_index_mid],E_field.field.x[:,:,z_index_mid],E_field.field.y[:,:,z_index_mid])





# fig2 = plt.figure('3D plots-div')
# ax1_f2 = fig2.add_subplot(111,projection='3d')

# # ax1_f2.contour(space1.x_grid,space1.y_grid,div_E)
# ax1_f2.set_aspect('equal')

# # ax1_f1.quiver(space1.x_grid,space1.y_grid,E_x,E_y)
# # ax1_f1.quiver(space1.x_grid,space1.y_grid,E_vec.x,E_vec.y,units='width')
# # ax1_f2.streamplot(space1.x_grid,space1.y_grid,E_vec.x,E_vec.y)
# ax1_f2.quiver(space1.x_grid,space1.y_grid,space1.z_grid, H_vec.x,H_vec.y,H_vec.z,length=0.1, normalize=True)





### Mayavi plots

fig2_m = mlab.figure('Mayavi plot')
mlab.clf(fig2_m)
#mlab.quiver3d(x_grid,y_grid,z_grid,F_vector_solution.x,F_vector_solution.y,F_vector_solution.z)
mlab.quiver3d(E_field.space.x_grid,E_field.space.y_grid,E_field.space.z_grid, E_field.field.x,E_field.field.y,E_field.field.z,scalars=E_field.field.magnitude(),scale_mode='none',mask_points=int(max([pts_x,pts_y,pts_z])/5))

mlab.outline()
mlab.orientation_axes()
mlab.axes()
# mlab.show()

plt.show()
