import numpy as np
import skvf as vf


import matplotlib.pyplot as plt
import mayavi.mlab as mlab

import sys as sys


########################################################################
################# Begin function definition ############################

def TE_mode(m,n,omega,space,a=0.1,b=0.1,epsilon_r=1,mu_r=1):
	mu = mu_r*vf.MU_0
	epsilon = epsilon_r*vf.EPSILON_0
	
	""" omega**2 mu*epslion - beta**2 = h**2"""
	h = np.sqrt( (m*np.pi/a)**2  + (n*np.pi/b)**2 )

	"""Cut-off frequency of the waveguide corresponds to beta = 0"""
  
	beta = np.sqrt(omega**2 * mu * epsilon - h**2 +0j)
	
	x_grid = space.x_grid
	y_grid = space.y_grid
	z_grid = space.z_grid
	
	Ez = np.zeros_like(x_grid) # Transverse eletric mode 

	Ex= (+1j*omega*mu/h**2)*(n*np.pi/b)*np.cos(m*np.pi*x_grid/a)*np.sin(n*np.pi*y_grid/b)*np.exp(-1j*beta*z_grid)
	Ey= (-1j*omega*mu/h**2)*(m*np.pi/a)*np.sin(m*np.pi*x_grid/a)*np.cos(n*np.pi*y_grid/b)*np.exp(-1j*beta*z_grid)



	Hz = np.cos(m*np.pi*x_grid/a)*np.cos(n*np.pi*y_grid/b)*np.exp(-1j*beta*z_grid)

	Hx= (+1j*beta/h**2)*(m*np.pi/a)*np.sin(m*np.pi*x_grid/a)*np.cos(n*np.pi*y_grid/b)*np.exp(-1j*beta*z_grid)
	Hy= (+1j*beta/h**2)*(n*np.pi/b)*np.cos(m*np.pi*x_grid/a)*np.sin(n*np.pi*y_grid/b)*np.exp(-1j*beta*z_grid)

	E_vec = vf.entities.vector(Ex,Ey,Ez)
	H_vec = vf.entities.vector(Hx,Hy,Hz)
	
	E_field = vf.entities.field(E_vec,space,'E_TE-'+str(m)+str(n))
	H_field = vf.entities.field(H_vec,space,'H_TE-'+str(m)+str(n))
	
	return E_field, H_field
	
# def TM_mode():
	
	
	# return
	

##################### End function definitions #########################
########################################################################


a = 0.5 # in meters.
b = 0.4 # in meters. 


pts_x = 50
pts_y = 50
pts_z = 100

'''Create space'''
x = np.linspace(0,a,pts_x)
y = np.linspace(0,b,pts_y)
# x = np.linspace(-1,1,50)
# y = np.linspace(-1,1,40)
z = np.linspace(0,1,pts_z)




space1 = vf.entities.space(x=x,y=y,z=z)


R_vec = space1.vec()


""" Rectangular waveguide  of cross-sectional dimensions a & b"""

epsilon_r = 1.0  # Relative dielectric constant of the medium inside waveguide. 



""" Select mode number """
m = 1 # mode number along 'a'
n = 0 # mode number along 'b'

h = np.sqrt( (m*np.pi/a)**2  + (n*np.pi/b)**2 )
omega_c = h/(np.sqrt(epsilon_r*vf.EPSILON_0*vf.MU_0)) # omega_c is in radians/s

omega = 1.5*omega_c

E_field, H_field = TE_mode(m=m,n=n,omega=omega,space=space1,a=a,b=b)

Fig_E = mlab.figure('E field')
# Fig_E = mlab.figure('E & H field')
Fig_E = E_field.real().plot_quiver3d(Fig=Fig_E,arrow_density=0.2,colormap='hot')

Fig_H = mlab.figure('H field')
Fig_H = H_field.real().plot_quiver3d(Fig=Fig_H,arrow_density=0.2,colormap='jet')
# fig_m = E_field.real().plot_quiver3d()

H_field.real().plot_volume_slice()

# ax_E_2d, Fig_E2d = E_field.

fig_2d = plt.figure('Waveguide')
ax_wg = fig_2d.subplots(1,3)

fig_2d_E_xy = E_field.real().plot_quiver2d(plane='x-y',loc=0.2,ax=ax_wg[0])
fig_2d_E_yz = E_field.real().plot_quiver2d(plane='y-z',loc=a/2,ax=ax_wg[1])
fig_2d_E_xz = E_field.real().plot_quiver2d(plane='y-z',loc=b/2,ax=ax_wg[2])

plt.show()
