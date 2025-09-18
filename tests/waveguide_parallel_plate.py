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
	

def TE_mode_parallel_plate(n,omega,space,d,epsilon_r=1,mu_r=1):
	'''Plane of propagation is assumed to be x-y. Direction of propagation is 
	in x-direction. For TE mode the direction of electric field is in the z-direction'''
	mu = mu_r*vf.MU_0
	epsilon = epsilon_r*vf.EPSILON_0
	
	""" omega**2 mu*epslion - beta**2 = h**2"""
	
	# ky = n*np.pi/d
	kx = n*np.pi/d
	
	
	"""Cut-off frequency of the waveguide corresponds to beta = 0"""
  
	# kx = np.sqrt(omega**2 * mu * epsilon - ky**2 +0j)
	kz = np.sqrt(omega**2 * mu * epsilon - kx**2 +0j)
	
	# kx = np.conjugate(kx)
	kz = np.conjugate(kx)
	
	x_grid = space.x_grid
	y_grid = space.y_grid
	z_grid = space.z_grid
	
	# Ez = np.zeros_like(x_grid) # Transverse eletric mode 

	# Ez = 1*np.sin(ky*y_grid)*np.exp(-1j*(kx*x_grid))
	Ey = 1*np.sin(kx*x_grid)*np.exp(-1j*(kz*z_grid))
	
	Ex = np.zeros_like(Ey)
	Ez = np.zeros_like(Ey)
	# Ey = np.zeros_like(Ez)
	
	
	# Ex= (+1j*omega*mu/h**2)*(n*np.pi/b)*np.cos(m*np.pi*x_grid/a)*np.sin(n*np.pi*y_grid/b)*np.exp(-1j*beta*z_grid)
	# Ey= (-1j*omega*mu/h**2)*(m*np.pi/a)*np.sin(m*np.pi*x_grid/a)*np.cos(n*np.pi*y_grid/b)*np.exp(-1j*beta*z_grid)



	# Hz = np.cos(m*np.pi*x_grid/a)*np.cos(n*np.pi*y_grid/b)*np.exp(-1j*beta*z_grid)

	# Hx= (+1j*beta/h**2)*(m*np.pi/a)*np.sin(m*np.pi*x_grid/a)*np.cos(n*np.pi*y_grid/b)*np.exp(-1j*beta*z_grid)
	# Hy= (+1j*beta/h**2)*(n*np.pi/b)*np.cos(m*np.pi*x_grid/a)*np.sin(n*np.pi*y_grid/b)*np.exp(-1j*beta*z_grid)

	E_vec = vf.entities.vector(Ex,Ey,Ez)
	E_field = vf.entities.field(E_vec,space,'E_TE-'+str(n))
	
	H_field = 1j/(omega*mu)*E_field.curl()
	
	# H_vec = vf.entities.vector(Hx,Hy,Hz)
	# H_field = vf.entities.field(H_vec,space,'H_TE-'+str(m)+str(n))
	H_field.text_tag = 'H_TE'+str(n)
	return E_field, H_field
	
# def TM_mode():
	
	
	# return
	


def F_Field_t(F_field,t,omega):
    
    Fx = F_field.field.x*np.exp(1j*omega*t)
    Fy = F_field.field.y*np.exp(1j*omega*t)
    Fz = F_field.field.z*np.exp(1j*omega*t)
    
    F_vec_t = vf.entities.vector(Fx,Fy,Fz)
    
    return vf.entities.field(F_vec_t,F_field.space)
    


##################### End function definitions #########################
########################################################################


a = 0.5 # in meters.
b = 0.4 # in meters. 

d = a

pts_x = 10
pts_y = 10
pts_z = 100

'''Create space'''
x = np.linspace(0,d,pts_x)
y = np.linspace(0,d,pts_y)
# x = np.linspace(-1,1,50)
# y = np.linspace(-1,1,40)
z = np.linspace(0,5*d,pts_z)




space1 = vf.entities.space(x=x,y=y,z=z)


R_vec = space1.vec()


""" Parallel plate waveguide of cross-sectional dimension d"""

epsilon_r = 1.0  # Relative dielectric constant of the medium inside waveguide. 



""" Select mode number """
# m = 1 # mode number along 'a'
n = 1 # mode number along 'b'

kc = n*np.pi/d
omega_c = kc/(np.sqrt(epsilon_r*vf.EPSILON_0*vf.MU_0)) # omega_c is in radians/s

omega = 1.05*omega_c
omega2 = 1.01*omega

E_field1, H_field1 = TE_mode_parallel_plate(n=n,omega=omega,space=space1,d=d)
E_field2, H_field2 = TE_mode_parallel_plate(n=n,omega=omega2,space=space1,d=d)

E_field = E_field1 #+ E_field2
H_field = H_field1 #+ H_field2

Spin_H_comp = H_field^H_field.conjugate()
Spin_H = Spin_H_comp.imag()
# print('Text tag',Spin_H.text_tag)
## Plot commands.

Spin_H.plot_contourf(plane='x-z',flag_colorbar=False)

fig_2d = plt.figure('Waveguide')
ax_wg = fig_2d.subplots(1,2)

# fig_2d_E_xy = E_field.real().plot_contourf(plane='x-y',loc=d/2,ax=ax_wg[0])
fig_2d_E_xy = E_field.real().plot_contourf(plane='x-z',loc=d/2,ax=ax_wg[0])
# fig_2d_E_xy = E_field.real().plot_quiver2d(plane='x-y',loc=d/2,ax=ax_wg[0])
# fig_2d_E_xy = H_field.real().plot_quiver2d(plane='x-y',loc=d/2,ax=ax_wg[1])
fig_2d_E_xy = H_field.real().plot_quiver2d(plane='x-z',loc=d/2,ax=ax_wg[1])
# fig_2d_E_yz = E_field.real().plot_quiver2d(plane='y-z',loc=a/2,ax=ax_wg[1])
# fig_2d_E_xz = E_field.real().plot_quiver2d(plane='y-z',loc=b/2,ax=ax_wg[2])
# Fig_E = mlab.figure('E & H field')

## 3D plots

Fig_E = mlab.figure('E field')
# Fig_E = E_field.real().plot_quiver3d(Fig=Fig_E,arrow_density=0.2,colormap='jet')

s = mlab.quiver3d(space1.x_grid,space1.y_grid,space1.z_grid,np.real(E_field.field.x),np.real(E_field.field.y),np.real(E_field.field.z), line_width=5,scale_factor=0.2,scale_mode='vector')



Fig_H = mlab.figure('H field')
# Fig_H = H_field.real().plot_quiver3d(Fig=Fig_H,arrow_density=1,colormap='jet')

# fig_m = E_field.real().plot_quiver3d()

s_h = mlab.quiver3d(space1.x_grid,space1.y_grid,space1.z_grid,np.real(H_field.field.x),np.real(H_field.field.y),np.real(H_field.field.z), line_width=5,scale_factor=50,scale_mode='vector')




# H_field.real().plot_volume_slice()

# ax_E_2d, Fig_E2d = E_field.



@mlab.animate
def anim():
    count = 0
    #for count in range(100):
    # E_field_t = E_field
    while 1:
        dt =0.1e-9
        # Ex_t_count, Ey_t_count, Ez_t_count = H_Fields_t_TE_mode(dt*count)
        E_field_t1 = F_Field_t(E_field1,dt*count,omega)
        E_field_t2 = F_Field_t(E_field2,dt*count,omega2)
        
        E_field_t = E_field_t1 #+E_field_t2
        
        Ex_t_count = E_field_t.field.x
        Ey_t_count = E_field_t.field.y
        Ez_t_count = E_field_t.field.z
        
        s.mlab_source.u = np.real(Ex_t_count)
        s.mlab_source.v = np.real(Ey_t_count)
        s.mlab_source.w = np.real(Ez_t_count)
        print(dt*count)
        count = count+1
        yield
        
        
@mlab.animate
def anim_h():
    count = 0
    #for count in range(100):
    # E_field_t = E_field
    while 1:
        dt =0.1e-9
        # Ex_t_count, Ey_t_count, Ez_t_count = H_Fields_t_TE_mode(dt*count)
        H_field_t1 = F_Field_t(H_field1,dt*count,omega)
        H_field_t2 = F_Field_t(H_field2,dt*count,omega2)
        
        H_field_t = H_field_t1 #+H_field_t2
        
        Hx_t_count = H_field_t.field.x
        Hy_t_count = H_field_t.field.y
        Hz_t_count = H_field_t.field.z
        
        s_h.mlab_source.u = np.real(Hx_t_count)
        s_h.mlab_source.v = np.real(Hy_t_count)
        s_h.mlab_source.w = np.real(Hz_t_count)
        print(dt*count)
        count = count+1
        yield


# anim()
# anim_h()



plt.show()
