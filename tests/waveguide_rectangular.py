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
	
def TM_mode(m,n,omega,space,a=0.1,b=0.1,epsilon_r=1,mu_r=1):
	mu = mu_r*vf.MU_0
	epsilon = epsilon_r*vf.EPSILON_0
	
	""" omega**2 mu*epslion - beta**2 = h**2"""
	h = np.sqrt( (m*np.pi/a)**2  + (n*np.pi/b)**2 )

	"""Cut-off frequency of the waveguide corresponds to beta = 0"""
  
	beta = np.sqrt(omega**2 * mu * epsilon - h**2 +0j)
	
	x_grid = space.x_grid
	y_grid = space.y_grid
	z_grid = space.z_grid
	
	Ez = np.sin(m*np.pi*x_grid/a)*np.sin(n*np.pi*y_grid/b)*np.exp(-1j*beta*z_grid) # Transverse magnetic mode 

	Ex= (-1j*beta/h**2)*(m*np.pi/a)*np.cos(m*np.pi*x_grid/a)*np.sin(n*np.pi*y_grid/b)*np.exp(-1j*beta*z_grid)
	Ey= (-1j*beta/h**2)*(n*np.pi/b)*np.sin(m*np.pi*x_grid/a)*np.cos(n*np.pi*y_grid/b)*np.exp(-1j*beta*z_grid)



	Hz = np.zeros_like(x_grid)

	Hx= (+1j*omega*epsilon/h**2)*(n*np.pi/b)*np.sin(m*np.pi*x_grid/a)*np.cos(n*np.pi*y_grid/b)*np.exp(-1j*beta*z_grid)
	Hy= (-1j*omega*epsilon/h**2)*(m*np.pi/a)*np.cos(m*np.pi*x_grid/a)*np.sin(n*np.pi*y_grid/b)*np.exp(-1j*beta*z_grid)

	E_vec = vf.entities.vector(Ex,Ey,Ez)
	H_vec = vf.entities.vector(Hx,Hy,Hz)
	
	E_field = vf.entities.field(E_vec,space,'E_TE-'+str(m)+str(n))
	H_field = vf.entities.field(H_vec,space,'H_TE-'+str(m)+str(n))
	
	return E_field, H_field




##################### End function definitions #########################
########################################################################


a = 0.5 # in meters.
b = 0.1 # in meters. 


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


Spin_H = (H_field^H_field.conjugate()).imag()

Spin_H.plot_quiver3d()


'''Field at a point '''

r0 = vf.entities.vector(a/2,b/2,0.5)
H_value, at_r = H_field.real().return_field_at_point(r0)

print(H_value.x,H_value.y,H_value.z)
print('at')
at_r.print()




'''Computation of surface current and charge'''



delta_a = 0.01*a




# E_vec_x_a, plane_x_a = return_field_in_plane(E_field,plane='y-z',loc=a-delta_a)
# E_vec_x_0, plane_x_0 = return_field_in_plane(E_field,plane='y-z',loc=delta_a)

# H_vec_x_a, plane_x_a = return_field_in_plane(H_field,plane='y-z',loc=a-delta_a)
# H_vec_x_0, plane_x_0 = return_field_in_plane(H_field,plane='y-z',loc=delta_a)

E_vec_x_a, plane_x_a = E_field.return_field_in_plane(plane='y-z',loc=a-delta_a)
E_vec_x_0, plane_x_0 = E_field.return_field_in_plane(plane='y-z',loc=delta_a)

H_vec_x_a, plane_x_a = H_field.return_field_in_plane(plane='y-z',loc=a-delta_a)
H_vec_x_0, plane_x_0 = H_field.return_field_in_plane(plane='y-z',loc=delta_a)

x_hat = vf.entities.vector(1,0,0)
y_hat = vf.entities.vector(0,1,0)



rho_x_a= -x_hat*E_vec_x_a
rho_x_0 = x_hat*E_vec_x_0

J_x_a = -x_hat^H_vec_x_a
J_x_0 = x_hat^H_vec_x_0


rho_field_x_a = vf.entities.field(rho_x_a,plane_x_a)
rho_field_x_0 = vf.entities.field(rho_x_0,plane_x_0)

J_field_x_a = vf.entities.field(J_x_a,plane_x_a)
J_field_x_0 = vf.entities.field(J_x_0,plane_x_0)



delta_b = 0.01*b

E_vec_y_b, plane_y_b = E_field.return_field_in_plane(plane='x-z',loc=b-delta_b)
E_vec_y_0, plane_y_0 = E_field.return_field_in_plane(plane='x-z',loc=delta_b)

H_vec_y_b, plane_y_b = H_field.return_field_in_plane(plane='x-z',loc=b-delta_b)
H_vec_y_0, plane_y_0 = H_field.return_field_in_plane(plane='x-z',loc=delta_b)

x_hat = vf.entities.vector(1,0,0)
y_hat = vf.entities.vector(0,1,0)



rho_y_b= -y_hat*E_vec_y_b
rho_y_0 = y_hat*E_vec_y_0

J_y_b = -y_hat^H_vec_y_b
J_y_0 = y_hat^H_vec_y_0


rho_field_y_b = vf.entities.field(rho_y_b,plane_y_b)
rho_field_y_0 = vf.entities.field(rho_y_0,plane_y_0)

J_field_y_b = vf.entities.field(J_y_b,plane_y_b)
J_field_y_0 = vf.entities.field(J_y_0,plane_y_0)


Fig_J = mlab.figure('Current_density')

scale_mode = 'vector'
s_h_J_y_0, Fig_J = J_field_y_0.real().plot_quiver3d(Fig=Fig_J,arrow_density=1,scale_mode=scale_mode)
s_h_J_y_b, Fig_J = J_field_y_b.real().plot_quiver3d(Fig=Fig_J,arrow_density=1,scale_mode=scale_mode)
s_h_J_x_0, Fig_J = J_field_x_0.real().plot_quiver3d(Fig=Fig_J,arrow_density=1,scale_mode=scale_mode)
s_h_J_x_a, Fig_J = J_field_x_a.real().plot_quiver3d(Fig=Fig_J,arrow_density=1,scale_mode=scale_mode)




Fig_E = mlab.figure('E field')
# Fig_E = mlab.figure('E & H field')
Fig_E = E_field.real().plot_quiver3d(Fig=Fig_E,arrow_density=0.2,colormap='hot')

Fig_H = mlab.figure('H field')
Fig_H = H_field.real().plot_quiver3d(Fig=Fig_H,arrow_density=0.2,colormap='jet')
# fig_m = E_field.real().plot_quiver3d()

H_field.real().plot_volume_slice(normal_plot=True)









# ax_E_2d, Fig_E2d = E_field.



fig_2d = plt.figure('Waveguide')
ax_wg = fig_2d.subplots(2,1)


# E_field_line1, line_space1 = E_field.return_field_on_line(along='x',y0=b/2,z0=0.25*b)
# E_field_line2, line_space2 = E_field.return_field_on_line(along='y',x0=a/2,z0=0.25*b)
# E_field_line3, line_space3 = E_field.return_field_on_line(along='z',x0=a/2,y0=0.5*b)

Spin_H_along_x,line_space1 = Spin_H.return_field_on_line(along='x',y0=b/2,z0=0.25*b)




# print(line_space.x)
# print(line_space.y)
# print(line_space.z)
# print(line_space.shape)
# print(E_field_line1)
# print(E_field_line1.x)
# print(E_field_line1.real().x)
# print(E_field_line1.real().y)
# print(E_field_line1.real().z)
# fig_1D_Ex = ax_wg[0].plot(line_space1.x,np.real(E_field_line1.y),linewidth='3')
# fig_1D_Ex = ax_wg[1].plot(line_space2.y,np.real(E_field_line2.y),linewidth='3')
# fig_1D_Ex = ax_wg[2].plot(line_space3.z,np.real(E_field_line3.y),linewidth='3')

# fig_2d_E_xy = E_field.real().plot_quiver2d(plane='x-y',loc=0.2,ax=ax_wg[0])
# fig_2d_E_yz = E_field.real().plot_quiver2d(plane='y-z',loc=a/2,ax=ax_wg[1])
fig_2d_H_xz = H_field.real().plot_quiver2d(plane='y-z',loc=b/2,ax=ax_wg[0])
fig_1D_Sh_y = ax_wg[1].plot(line_space1.x,np.real(Spin_H_along_x.y),linewidth='3')







''' Animate 3D '''


Fig_ani = mlab.figure('Field-animate',bgcolor=(0,0,0))
mlab.clf(Fig_ani)

# s = mlab.quiver3d(space1.x_grid,space1.y_grid,space1.z_grid,np.real(E_field.field.x),np.real(E_field.field.y),np.real(E_field.field.z), line_width=1,scale_factor=0.1,scale_mode='scalar')

# s = plot

F_field2 = H_field
# F_field = E_field

# s_field = plot_mayavi_quiver(F_field.real(),figure=Fig_ani,scale_mode='vector',arrow_density=0.7,colormap='jet')
s_field2 = vf.plot.plot_mayavi_quiver(F_field2.real(),figure=Fig_ani,scale_mode='vector',arrow_density=0.1,colormap='autumn')
# s_field = None

s_J_x_a = vf.plot.plot_mayavi_quiver(J_field_x_a.real(),figure=Fig_ani,scale_mode='vector',colormap='winter',arrow_density=1)
s_J_x_0 = vf.plot.plot_mayavi_quiver(J_field_x_0.real(),figure=Fig_ani,scale_mode='vector',colormap='winter',arrow_density=1)

s_J_y_b = vf.plot.plot_mayavi_quiver(J_field_y_b.real(),figure=Fig_ani,scale_mode='vector',colormap='winter',arrow_density=1)
s_J_y_0 = vf.plot.plot_mayavi_quiver(J_field_y_0.real(),figure=Fig_ani,scale_mode='vector',colormap='winter',arrow_density=1)

# s_h_rho_x_a_ani = plot_mayavi_charge(rho_field_x_a.real(),figure=Fig_ani,opacity=0.2)
# s_h_rho_x_0_ani= plot_mayavi_charge(rho_field_x_0.real(),figure=Fig_ani,opacity=0.2)

# s_h_rho_y_b_ani = plot_mayavi_charge(rho_field_y_b.real(),figure=Fig_ani,opacity=0.2)
# s_h_rho_y_0_ani = plot_mayavi_charge(rho_field_y_0.real(),figure=Fig_ani,opacity=0.2)

rho_max = np.max([np.max(rho_field_x_0.real().field), np.max(rho_field_y_0.real().field)])
# rho_min = np.max([np.min(rho_field_x_0.real().field), np.min(rho_field_y_0.real().field)])
rho_min = -rho_max


s_h_rho_x_a_ani = vf.plot.plot_mayavi_points3d(rho_field_x_a.real(),figure=Fig_ani,opacity=0.3,scale_mode='none',vmax=rho_max,vmin=rho_min)
s_h_rho_x_0_ani= vf.plot.plot_mayavi_points3d(rho_field_x_0.real(),figure=Fig_ani,opacity=0.3,scale_mode='none',vmax=rho_max,vmin=rho_min)

s_h_rho_y_b_ani = vf.plot.plot_mayavi_points3d(rho_field_y_b.real(),figure=Fig_ani,opacity=0.3,scale_mode='none',vmax=rho_max,vmin=rho_min)
s_h_rho_y_0_ani = vf.plot.plot_mayavi_points3d(rho_field_y_0.real(),figure=Fig_ani,opacity=0.3,scale_mode='none',vmax=rho_max,vmin=rho_min)


print('rho_max=',rho_max)
print('rho_min=',rho_min)

def fun_update_ani_quiver_data(s_handle,F_field_new):
	
	Fx_t_count = F_field_new.field.x
	Fy_t_count = F_field_new.field.y
	Fz_t_count = F_field_new.field.z
	
	s_handle.mlab_source.u = np.real(Fx_t_count)
	s_handle.mlab_source.v = np.real(Fy_t_count)
	s_handle.mlab_source.w = np.real(Fz_t_count)
	return s_handle

@mlab.animate
def anim():
    count = 0
    #for count in range(100):
    dt = (2*np.pi/omega)*0.02
    # global s_field
    global s_field2
    global s_J_x_0, s_J_x_a, s_J_y_0, s_J_y_b
    global s_h_rho_x_0_ani, s_h_rho_x_a_ani, s_h_rho_y_0_ani, s_h_rho_y_b_ani
    
    
    while 1:
        
        # F_field_t = fun_F_Field_t(F_field,dt*count,omega)
        F_field2_t = fun_F_Field_t(F_field2,dt*count,omega)
        
        # s_field_count = fun_update_ani_quiver_data(s_field,F_field_t)
        
        
        # Fx_t_count = F_field_t.field.x
        # Fy_t_count = F_field_t.field.y
        # Fz_t_count = F_field_t.field.z
        
        
        J_field_x_0_t = fun_F_Field_t(J_field_x_0,dt*count,omega)
        J_field_x_a_t = fun_F_Field_t(J_field_x_a,dt*count,omega)
        J_field_y_0_t = fun_F_Field_t(J_field_y_0,dt*count,omega)
        J_field_y_b_t = fun_F_Field_t(J_field_y_b,dt*count,omega)
        
        
        rho_field_x_0_t = fun_F_Field_scalar_t(rho_field_x_0,dt*count,omega)
        rho_field_x_a_t = fun_F_Field_scalar_t(rho_field_x_a,dt*count,omega)
        rho_field_y_0_t = fun_F_Field_scalar_t(rho_field_y_0,dt*count,omega)
        rho_field_y_b_t = fun_F_Field_scalar_t(rho_field_y_b,dt*count,omega)
        
     
        
        # J_bottom_t = F_Fields_t(J_field_top,dt*count,omega)
        
        # rho_top_t = F_Fields_scalar_t(rho_field_top,dt*count,omega)
        # rho_bottom_t = F_Fields_scalar_t(rho_field_bottom,dt*count,omega)
        
        
        # Jx_top_t_count = J_top_t.field.x
        # Jy_top_t_count = J_top_t.field.y
        # Jz_top_t_count = J_top_t.field.z
        
        # Jx_bottom_t_count = J_top_t.field.x
        # Jy_bottom_t_count = J_top_t.field.y
        # Jz_bottom_t_count = J_top_t.field.z
        
        # s_field.mlab_source.u = np.real(Fx_t_count)
        # s_field.mlab_source.v = np.real(Fy_t_count)
        # s_field.mlab_source.w = np.real(Fz_t_count)
        
        
        
        s_field2 = fun_update_ani_quiver_data(s_field2,F_field2_t)
        
        
        s_J_x_0 = fun_update_ani_quiver_data(s_J_x_0,J_field_x_0_t)
        s_J_x_a = fun_update_ani_quiver_data(s_J_x_a,J_field_x_a_t)
        s_J_y_0 = fun_update_ani_quiver_data(s_J_y_0,J_field_y_0_t)
        s_J_y_b = fun_update_ani_quiver_data(s_J_y_b,J_field_y_b_t)
        
        s_h_rho_x_0_ani.mlab_source.scalars = np.real(rho_field_x_0_t.field)
        s_h_rho_x_a_ani.mlab_source.scalars = np.real(rho_field_x_a_t.field)
        s_h_rho_y_0_ani.mlab_source.scalars = np.real(rho_field_y_0_t.field)
        s_h_rho_y_b_ani.mlab_source.scalars = np.real(rho_field_y_b_t.field)
        
        # s_J_top.mlab_source.u = np.real(Jx_top_t_count)
        # s_J_top.mlab_source.v = np.real(Jy_top_t_count)
        # s_J_top.mlab_source.w = np.real(Jz_top_t_count)
        
        # s_J_bottom.mlab_source.u = np.real(Jx_bottom_t_count)
        # s_J_bottom.mlab_source.v = np.real(Jy_bottom_t_count)
        # s_J_bottom.mlab_source.w = np.real(Jz_bottom_t_count)
        
        # s_rho_top.mlab_source.s = np.real(rho_top_t.field)
		
		

        
        print(count*dt/1e-9)
        count = count+1
        yield


# anim()


# mlab.axes()


# mlab.show()
# plt.show()



plt.show()
