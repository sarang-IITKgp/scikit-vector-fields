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
x = np.linspace(-3,3,50)
y = np.linspace(-2,2,40)
# x = np.linspace(-1,1,50)
# y = np.linspace(-1,1,40)
z = np.linspace(-1,1,10)


space_xy = vf.entities.space(x=x,y=y)
space_yz = vf.entities.space(y=y,z=z)
space_xz = vf.entities.space(x=x,z=z)

space1 = vf.entities.space(x=x,y=y,z=z)


R_vec = space1.vec()


# dict1 = {'dI': vf.entites.vector(1,0,0), 'r0': vf.entities.vector(1,0,0) }
# # current_elements = [{'dI': vf.entites.vector(1,0,0), 'r0': vf.entities.vector(1,0,0)} ]

# current_elements.append({'dI':vf.entites.vector(1,0,0}, 'r0':vf.entities.vector(-1,0,0)})

# A_vec = 0

# for element in current_elements:
    # A_vec = A_vec+A_due_to_current(dI_vec=element['dI'],space=space1,r0=element['r0'])

A_vec1 = A_due_to_current(dI_vec=vf.entities.vector(0,0,1),space=space1,r0=vf.entities.vector(1,0,0))
A_vec2 = A_due_to_current(dI_vec=vf.entities.vector(0,0,-1),space=space1,r0=vf.entities.vector(-1,0,0))

# print('-------- Define Fields ---------')

A_field1 = vf.entities.field(A_vec1,space1,text_tag='A1')
A_field2 = vf.entities.field(A_vec2,space1,text_tag='A2')

A_field = A_field1 + A_field2

# V_field1 = vf.entities.field(V1,space1,text_tag='V1')
# V_field2 = vf.entities.field(V2,space1,text_tag='V2')
# # V_field = vf.entities.field(V,space1,text_tag='V1+V2')
# V_field = V_field1+V_field2

# E_field = -V_field.grad()

H_field = A_field.curl()*(1/vf.MU_0)

# dump_field = E_field^E_field
# print(dump_field.field.print())
# rho_field = E_field.div()

J_field = H_field.curl()



'''Plot commands '''
### Plot commands

print('--------------Testing plot module-------------')
H_field.field.text_tag = 'H_field'


loc=0

H_field.plot_quiver2d(plane='x-y',loc=loc)
H_field.plot_streamplot(plane='x-y',loc=loc)
J_field.plot_contourf(plane='x-y',loc=loc)
H_field.plot_quiver3d(1)


# ax, Fig = vf.plot.contourf(J_field.space,J_field.field.z,plane='x-y',loc=loc,text_tag='J')#,vmax=1,vmin=-1)#,flag_colorbar=False)

H_field.field.text_tag = 'Same'
ax, Fig = vf.plot.quiver2d(H_field.space,H_field.field,plane='x-y',loc=loc)
# ax, Fig = vf.plot.quiver2d(H_field.space,H_field.field,plane='y-z',loc=1.5)
# ax, Fig = vf.plot.quiver2d(H_field.space,H_field.field,plane='x-z',loc=0.5)
# print(Fig)

# ax, Fig = vf.plot.streamplot(H_field.space,H_field.field,plane='x-y',loc=loc,ax=ax)
# ax, Fig = vf.plot.streamplot(H_field.space,H_field.field,plane='y-z',loc=1,ax=ax)
# ax, Fig = vf.plot.streamplot(H_field.space,H_field.field,plane='x-z',loc=1)
# ax, Fig = vf.plot.streamplot(H_field.space,H_field.field,plane='x-z',loc=0)
# ax.set_xlabel('y')
# ax.set_ylabel('z')


'''Mayavi plot using library'''

# vf.plot.quiver3d(H_field.space,H_field.field,arrow_density=0.7)




# ax.set_aspect('equal')

# loc = -5.0
# index_of_plane = (abs(z-loc)).argmin()
# print('z= ',space1.z)

# print('from grid',space1.x_grid[0,:,0])
# print('from grid',space1.z_grid[0,0,:])
# print(index_of_plane)



# fig1 = plt.figure('2D plots')
# ax1_f1 = fig1.add_subplot(111)
pts_y, pts_x, pts_z = A_field.space.shape

# z_index_mid = int(pts_z/2)

# # ax.contour(J_field.space.x_grid[:,:,z_index_mid],J_field.space.y_grid[:,:,z_index_mid],J_field.field.z[:,:,z_index_mid])

# ax1_f1.contourf(J_field.space.x_grid[:,:,z_index_mid],J_field.space.y_grid[:,:,z_index_mid],J_field.field.z[:,:,z_index_mid])
# # ax1_f1.contour(A_field.space.x_grid[:,:,z_index_mid],A_field.space.y_grid[:,:,z_index_mid],A_field.field.z[:,:,z_index_mid])
# ax1_f1.set_aspect('equal')



# # print(pts_x,pts_y,pts_z)



# # ax1_f1.quiver(E_field.space.x_grid[:,:,z_index_mid],E_field.space.y_grid[:,:,z_index_mid],E_field.field.x[:,:,z_index_mid],E_field.field.y[:,:,z_index_mid],units='width')
# ax1_f1.quiver(H_field.space.x_grid[:,:,z_index_mid],H_field.space.y_grid[:,:,z_index_mid],H_field.field.x[:,:,z_index_mid],H_field.field.y[:,:,z_index_mid])
# ax1_f1.quiver(A_field.space.x_grid[:,:,z_index_mid],A_field.space.y_grid[:,:,z_index_mid],A_field.field.x[:,:,z_index_mid],A_field.field.y[:,:,z_index_mid])
# # ax.quiver(A_field.space.x_grid[:,:,z_index_mid],A_field.space.y_grid[:,:,z_index_mid],A_field.field.x[:,:,z_index_mid],A_field.field.y[:,:,z_index_mid])





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
# mlab.quiver3d(H_field.space.x_grid,H_field.space.y_grid,H_field.space.z_grid, H_field.field.x,H_field.field.y,H_field.field.z,scalars=H_field.field.magnitude(),scale_mode='none',mask_points=int(max([pts_x,pts_y,pts_z])/5))
mlab.quiver3d(H_field.space.x_grid,H_field.space.y_grid,H_field.space.z_grid, H_field.field.x,H_field.field.y,H_field.field.z,scale_mode='none',mask_points=int(max([pts_x,pts_y,pts_z])/5))

mlab.outline()
mlab.orientation_axes()
mlab.axes()
# # mlab.show()

plt.show()
