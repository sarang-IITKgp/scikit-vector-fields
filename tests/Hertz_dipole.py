import numpy as np
import skvf as vf

import copy as copy
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




def A_due_to_dI(dI,r0=0,R_vec=None,space=None,omega=0):
	'''Computes and returns the Magnetic vector potential of a current, located at r0'''
	
	if R_vec == None:
		if space ==  None:
			print('At least one of R-vector or space object must be defined')
		else:
			R_vec = space.vec()
	
	
	# V = q/(4*np.pi*vf.EPSILON_0*(R_vec-r0).magnitude())
	
	if isinstance(dI,vf.entities.source):
		
		dI_vec = dI.source
		r0 = dI.r0
	else: 
		dI_vec = dI
		r0 = r0
	
	beta = omega/vf.VELOCITY_OF_LIGHT
	lambda0 = 2*np.pi/beta
	
	dl = 0.1*lambda0
	
	R_minus_r0_mag = (R_vec-r0).magnitude()
	
	# Ax = vf.MU_0/(4*np.pi*(R_minus_r0_mag).magnitude())*dI_vec.x*np.exp(-1j*beta*R_minus_r0_mag)
	# Ay = vf.MU_0/(4*np.pi*(R_minus_r0_mag).magnitude())*dI_vec.y*np.
	# Az = vf.MU_0/(4*np.pi*(R_minus_r0_mag).magnitude())*dI_vec.z

	Ax = vf.MU_0/(4*np.pi*R_minus_r0_mag)*dI_vec.x*dl*np.exp(-1j*beta*R_minus_r0_mag)
	Ay = vf.MU_0/(4*np.pi*R_minus_r0_mag)*dI_vec.y*dl*np.exp(-1j*beta*R_minus_r0_mag)
	Az = vf.MU_0/(4*np.pi*R_minus_r0_mag)*dI_vec.z*dl*np.exp(-1j*beta*R_minus_r0_mag)
 

	# return A_vec
	return vf.entities.vector(Ax,Ay,Az)

##################### End function definitions #########################
########################################################################


freq = 1e9
omega = 2*np.pi*freq
c = vf.VELOCITY_OF_LIGHT

beta = omega/c
lambda0 = 2*np.pi/beta


'''Create space'''
x = np.linspace(-3*lambda0,3*lambda0,40)
y = np.linspace(-3*lambda0,3*lambda0,40)
# x = np.linspace(-1,1,50)
# y = np.linspace(-1,1,40)
z = np.linspace(-3*lambda0,3*lambda0,40)


space_xy = vf.entities.space(x=x,y=y)
space_yz = vf.entities.space(y=y,z=z)
space_xz = vf.entities.space(x=x,z=z)

space1 = vf.entities.space(x=x,y=y,z=z)

# space1.shift_x(3)

R_vec = space1.vec()



r0 = vf.entities.vector(0.25*lambda0,0,0)
dI_vec = vf.entities.vector(0,0,1)
phi = np.pi*90/180
dI_vec2 = vf.entities.vector(0,0,1*np.exp(1j*phi))


dI = vf.entities.source(dI_vec,r0)

dI2 = vf.entities.source(dI_vec2,-r0)

A_Hertz1 = A_due_to_dI(dI,space=space1,omega=omega)
A_Hertz2 = A_due_to_dI(dI2,space=space1,omega=omega)
A_Hertz = A_Hertz1+A_Hertz2
print(type(A_Hertz))
A_field = vf.entities.field(A_Hertz,space1,text_tag='$vec{A}$')

print(type(1j*omega*vf.EPSILON_0))
print(1/(1j*omega*vf.EPSILON_0))

H_field = (1/vf.MU_0)*A_field.curl()
E_field = (1/(1j*omega*vf.EPSILON_0))*H_field.curl()


# E_field.real().plot_quiver3d()
# E_field.real().plot_volume_slice()

Pv_field = E_field^H_field.conjugate()

Pv_field.real().plot_volume_slice()

fig =plt.figure('2D plot')
ax = fig.subplots(1,1)
# ax = fig.subplots(1,3)
# A_field.real().plot_quiver2d(plane='x-z',ax=ax)
# E_field.real().plot_quiver2d(plane='x-z',ax=ax)
print(type(Pv_field.field))
# Pv_field.real().plot_streamplot(plane='y-z',ax=ax)
Pv_field.real().plot_contourf(plane='x-y',ax=ax,cmap='jet')
Pv_field.real().plot_quiver2d(plane='x-y',ax=ax,cmap='hot')
# Pv_field.real().plot_quiver2d(plane='y-z',ax=ax,cmap='jet')
# Pv_field.real().plot_quiver2d(plane='y-z',ax=ax,cmap='jet')
# E_field.real().plot_quiver2d(plane='y-z',ax=ax,cmap='hot')
# E_field.real().plot_streamplot(plane='y-z',ax=ax,cmap='hot')
# A_field.real().plot_quiver2d(plane='x-z',ax=ax[0])
# H_field.real().plot_quiver2d(plane='x-y',ax=ax)
# H_field.real().plot_streamplot(plane='x-y',ax=ax)

plt.show()
