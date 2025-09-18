""" Code to visualize 3D scalar and vector fields"""



################################################################################
######################## Import Libraries ######################################


import numpy as np # For numerical function

import matplotlib.pyplot as plt # For 2D plot
import matplotlib as mpl


import skvf as vf

import mayavi.mlab as mlab

import sys as sys





################################################################################

############################### Define parameters ##############################

c = 3e8 # velocity of ligh in meters/second 
mu_0 = 4*np.pi*1e-7
epsilon_0 = 8.854*1e-12

""" Set wave frequency"""
omega = 2*np.pi*1e9 


epsilon_r1 = 1.0  # Relative permittivity of medium-1
epsilon_r2 = 2.0  # Relative permittivity of medium-2

# sigma = 10
# epsilon_r2 = epsilon_r2 + sigma/(1j*omega*epsilon_0) 

mu_r1 = 1 # Relative permeability of medium-1
mu_r2 = 1 # Relative permeability of medium-2







theta_i = 1*np.pi/3 # Angle of incidence in medium-1. 

k0 = omega*np.sqrt(mu_0*epsilon_0)

k1 = k0*np.sqrt(mu_r1*epsilon_r1)
k2 = k0*np.sqrt(mu_r2*epsilon_r2)


kxi = k1*np.cos(theta_i)
kzi = k1*np.sin(theta_i)



kxr = -k1*np.cos(theta_i)
kzr = kzi

kzt = kzi
kxt = np.sqrt(k2**2 - kzt**2+0j)

kxt = np.real(kxt)-1j*np.abs(np.imag(kxt))

ki_vec = vf.entities.vector(kxi,0,kzi)
kr_vec = vf.entities.vector(kxr,0,kzr)
kt_vec = vf.entities.vector(kxt,0,kzt)


fig0 = plt.figure('Iso-frequency')
ax1_f0 = fig0.add_subplot(111)
theta_plot = np.linspace(0,2*np.pi,100)
ax1_f0.plot(k1*np.cos(theta_plot),k1*np.sin(theta_plot),'b',linewidth=3,label='#1')
ax1_f0.plot(k2*np.cos(theta_plot),k2*np.sin(theta_plot),'r',linewidth=3,label='#2')
# ax1_f0.annotate('\vec{k}_i',(0,0),(np.real(kxi),np.real(kzi)))


ax1_f0.plot([0,kzi],[0,kxi],'b-',linewidth=2,label='$\\vec{k}_i$')
ax1_f0.stem(kzi,kxi,'b')
ax1_f0.stem(kxi,kzi,'b',orientation='horizontal')

ax1_f0.plot([0,kzr],[0,kxr],'g-',linewidth=2,label='$\\vec{k}_r$')
ax1_f0.stem(kzr,kxr,'g')
ax1_f0.stem(kxr,kzr,'g',orientation='horizontal')


ax1_f0.plot([0,kzt],[0,kxt],'r-',linewidth=2,label='$\\vec{k}_t$')
ax1_f0.stem(kzt,kxt,'r')
ax1_f0.stem(kxt,kzt,'r',orientation='horizontal')

ax1_f0.set_xlabel('$k_z$')
ax1_f0.set_ylabel('$k_x$')


ax1_f0.legend()
ax1_f0.axis('equal')
ax1_f0.grid(1)





def R_T_TE(theta_i,omega=omega,mu_r1=mu_r1,mu_r2=mu_r2,epsilon_r1=epsilon_r1,epsilon_r2=epsilon_r2):
	# k0 = omega*np.sqrt(vf.MU_0*vf.EPSILON_0)

	k1 = k0*np.sqrt(mu_r1*epsilon_r1)
	k2 = k0*np.sqrt(mu_r2*epsilon_r2)
	
	mu_1 = mu_0*mu_r1
	mu_2 = mu_0*mu_r2
	
	

	kxi = k1*np.cos(theta_i)
	kzi = k1*np.sin(theta_i)


	kxr = -k1*np.cos(theta_i)
	kzr = kzi

	kzt = kzi
	kxt = np.sqrt(k2**2 - kzt**2 +0j)
	
	
	kxt = np.real(kxt)-1j*np.abs(np.imag(kxt))
	R_TE = (mu_2*kxi - mu_1*kxt)/(mu_2*kxi+mu_1*kxt)
	T_TE = 2*mu_2*kxi/(mu_2*kxi+mu_1*kxt)
	return R_TE, T_TE



''' Defining space'''
pts_x = 50 # Number of points along x axis
pts_y = 50 # Number of points along y axis
pts_z = 50 # Number of points along z axis

x = np.linspace(-0.25,0.25,pts_x) # Extent of x coordinates
y = np.linspace(-0.25,0.25,pts_y) # Extent of y coordinates
z = np.linspace(-0.5,0.5,pts_z) # Extent of z coordinates

x_interface = 0

# x_grid, y_grid, z_grid = np.meshgrid(x,y,z)

space = vf.entities.space(x,y,z)
R_vec = space.vec()


############################## Normalize the fields ############################

# """ Normalize the vector field with the maxmimum of all components """
# E_max = max([np.abs(Ex).max(),np.abs(Ey).max(), np.abs(Ez).max()])
# H_max = max([np.abs(Hx).max(),np.abs(Hy).max(), np.abs(Hz).max()])


def F_Fields_t(F_field,t,omega):
    
    Fx = F_field.field.x*np.exp(1j*omega*t)
    Fy = F_field.field.y*np.exp(1j*omega*t)
    Fz = F_field.field.z*np.exp(1j*omega*t)
    
    F_vec_t = vf.entities.vector(Fx,Fy,Fz)
    
    return vf.entities.field(F_vec_t,F_field.space)
    

# def H_Fields_t_TEM(t):
    
    # Hz = np.cos(m*np.pi*x_grid/a)*np.cos(n*np.pi*y_grid/b)*np.exp(-1j*beta*z_grid) * np.exp(1j*omega*t)

    # Hx= (+1j*beta/h**2)*(m*np.pi/a)*np.sin(m*np.pi*x_grid/a)*np.cos(n*np.pi*y_grid/b)*np.exp(-1j*beta*z_grid)*np.exp(1j*omega*t)
    # Hy= (+1j*beta/h**2)*(n*np.pi/b)*np.cos(m*np.pi*x_grid/a)*np.sin(n*np.pi*y_grid/b)*np.exp(-1j*beta*z_grid)*np.exp(1j*omega*t)
    # H_max = max([np.abs(Hx).max(),np.abs(Hy).max(), np.abs(Hz).max()])
    
    # return Hx/H_max,Hy/H_max,Hz/H_max 
    
########### Define fields #####################

# Ey = 5*np.exp(-1j*beta*space1.x_grid)
# Ex = np.zeros_like(Ey)
# Ez = 5*np.exp(-1j*beta*space1.x_grid+1j*np.pi/3)


# A1 = 5
# A2 = 5#*np.tan(np.pi/4)
# phi = 1*np.pi*0.1


# Ex = A1*np.exp(-1j*beta*space1.z_grid)
# Ey = A2*np.exp(-1j*beta*space1.z_grid+1j*phi)
# Ez = np.zeros_like(Ey)
# # Ez = 5*np.exp(-1j*beta*space1.x_grid)
# # Ez = np.zeros_like(Ey)


# E_vec = vf.entities.vector(Ex,Ey,Ez)

# E_field = vf.entities.field(E_vec,space1,'E')



# gamma = np.arctan(A2/A1)
# print('gamma, phi = ',gamma,phi)


# tau = 0.5*np.arctan(np.tan(2*gamma)*np.cos(phi))

# alpha = 0.5*np.arcsin(np.sin(2*gamma)*np.sin(phi))




'''TE Mode'''

############################# TE-mode ##########################################


R_TE, T_TE = R_T_TE(theta_i = theta_i,omega=omega)

E_y1 = np.zeros_like(space.x_grid)
E_y2 = np.zeros_like(space.x_grid)

index_x_1 = space.x_grid < x_interface
index_x_2 = space.x_grid >= x_interface

# print(index_x_1)
# print(index_x_2)

# ki_vec.print()
# kr_vec.print()
# kt_vec.print()

# temp = ki_vec*R_vec
# print(np.shape(temp))


E_y1 = 1*np.exp(-1j*ki_vec*R_vec) + R_TE*np.exp(-1j*kr_vec*R_vec)
E_y2 = T_TE*np.exp(-1j*kt_vec*R_vec)

# E_y1[index_x_2] = 0 
E_y2[index_x_1] = 0 


E1_vec = vf.entities.vector(np.zeros_like(E_y1),E_y1,np.zeros_like(E_y1))
E2_vec = vf.entities.vector(np.zeros_like(E_y2),E_y2,np.zeros_like(E_y2))

E_field_1 = vf.entities.field(E1_vec,space)
E_field_2 = vf.entities.field(E2_vec,space)


H_field_1 = -1/(1j*omega*mu_0*mu_r1)*E_field_1.curl()
H_field_2 = -1/(1j*omega*mu_0*mu_r2)*E_field_2.curl()

# E_vec = E1_vec + E2_vec

E_field  = E_field_1 + E_field_2
H_field  = H_field_1 + H_field_2


Pv_field = E_field^H_field.conjugate()


S_H_complex = H_field^H_field.conjugate()
S_H = S_H_complex.imag()



# print(E_y1)

# print(R_TE,T_TE)
# print('-------------')
# # print(1+R_TE)
# print(np.abs(R_TE))



################################################################################






''' Commands to Plot '''

fig1 = plt.figure('E_field')
ax1_f1 = fig1.add_subplot(121)
ax2_f1 = fig1.add_subplot(122)
# ax3_f1 = fig1.add_subplot(133)

fig2 = plt.figure('Ppynting_vector')
ax1_f2 = fig2.add_subplot(121)
ax2_f2 = fig2.add_subplot(122)


E_field.real().plot_contourf(ax=ax1_f1,plane='x-z')


S_H.plot_contourf(ax=ax2_f1,plane='x-z')
10*H_field.real().plot_quiver2d(ax=ax2_f1,plane='x-z')


Pv_field.real().plot_quiver2d(ax=ax1_f2,plane='x-z')
Pv_field.imag().plot_quiver2d(ax=ax2_f2,plane='x-z')




maya1 = mlab.figure('E-plot')
maya2 = mlab.figure('H-plot')
maya3 = mlab.figure('Pv-plot')
# mlab.clf(maya1)
# mlab.clf(maya2)
# mlab.clf(maya3)



E_field.real().plot_quiver3d(Fig=maya1)
H_field.real().plot_quiver3d(Fig=maya2)
Pv_field.real().plot_quiver3d(Fig=maya3)

# mlab.mesh(x_grid,y_grid,z_grid)
# mlab.quiver3d(x_grid,y_grid,z_grid,np.real(Ex)/E_max,np.real(Ey)/E_max,np.real(Ez)/E_max, line_width=2,scale_factor=0.02,scale_mode='vector')


# mlab.outline()
# mlab.axes()


# s =mlab.quiver3d(space1.x_grid,space1.y_grid,space1.z_grid,np.real(E_field.field.x),np.real(E_field.field.y),np.real(E_field.field.z), line_width=5,scale_factor=0.02,scale_mode='vector')





maya2 = mlab.figure('Vector-plot-animate')
mlab.clf(maya2)

# Hx_t, Hy_t, Hz_t = H_Fields_t_TE_mode(0e-9)


x_grid = space.x_grid
y_grid = space.y_grid
z_grid = space.z_grid


# F_field = E_field
F_field = 100*H_field
# F_field = 100*Pv_field

F_x = F_field.field.x
F_y = F_field.field.y
F_z = F_field.field.z

# # mlab.mesh(x_grid,y_grid,z_grid)
# mlab.quiver3d(x_grid,y_grid,z_grid,np.real(Ex)/E_max,np.real(Ey)/E_max,np.real(Ez)/E_max, line_width=2,scale_factor=0.02,scale_mode='vector')
s = mlab.quiver3d(x_grid,y_grid,z_grid,np.real(F_x),np.real(F_y),np.real(F_z), line_width=5,scale_factor=0.02,scale_mode='vector')




@mlab.animate
def anim():
    count = 0
    #for count in range(100):
    # E_field_t = E_field
    while 1:
        dt =0.01e-9
        # Ex_t_count, Ey_t_count, Ez_t_count = H_Fields_t_TE_mode(dt*count)
        F_field_t = F_Fields_t(F_field,dt*count,omega)
        
        Fx_t_count = F_field_t.field.x
        Fy_t_count = F_field_t.field.y
        Fz_t_count = F_field_t.field.z
        
        s.mlab_source.u = np.real(Fx_t_count)
        s.mlab_source.v = np.real(Fy_t_count)
        s.mlab_source.w = np.real(Fz_t_count)
        print(dt*count)
        count = count+1
        yield


# anim()

mlab.axes()

plt.show()

# mlab.show()

### Poincare sphere
# maya2 = mlab.figure('Poincare sphere')
# mlab.clf(maya2)

# def sphere_xyz(N):
    # """Generates a pretty set of lines."""
    # pi=np.pi;
    # #sin=np.sin
    # #cos=np.cos	
    # phi=np.linspace(0.0, 2*pi,N)
    # theta=np.linspace(0.0,pi,N)

    # [phi_m, theta_m]=np.meshgrid(phi, theta)

    # x=np.sin(theta_m)*np.cos(phi_m)
    # y=np.sin(theta_m)*np.sin(phi_m)
    # z=np.cos(theta_m)	
    # return x,y,z
    
    
# #test_plot3d()
# mlab.figure('Poincare Sphere', size=(400, 300))
# #clf()

# #pi=np.pi;

# N=36;
# [x,y,z]=sphere_xyz(N);

# #phi=np.linspace(0.0, 2*pi,N)
# #theta=np.linspace(0.0,pi,N)
# #sin=np.sin
# #cos=np.cos
# #
# #[phi_m, theta_m]=np.meshgrid(phi, theta)
# #
# #x=sin(theta_m)*cos(phi_m)
# #y=sin(theta_m)*sin(phi_m)
# #z=cos(theta_m)

# #surf(x,y,z)
# mlab.mesh(x,y,z,representation="surface",opacity=0.5)

# [x_line,y_line,z_line]=sphere_xyz(41)

# for count1 in range(8):
    # count=5*(count1);
    # l1=mlab.plot3d(x_line[:,count],y_line[:,count],z_line[:,count],tube_radius=0.005,color=(0,0,0))
    # l2=mlab.plot3d(x_line[count,:],y_line[count,:],z_line[count,:],tube_radius=0.005,color=(0,0,0))

# #points3d(0,0,0,scale_factor=.05)

# theta_pt1=np.radians([90,45]); 
# phi_pt1=np.radians([0,45]);
# #theta_pt2=np.radians(45); phi_pt2=np.radians(45);

# S1 = np.cos(2*alpha)*np.cos(2*tau)
# S2 = np.cos(2*alpha)*np.sin(2*tau)
# S3 = np.sin(2*alpha)

# # x_pt1=np.sin(theta_pt1)*np.cos(phi_pt1);
# # y_pt1=np.sin(theta_pt1)*np.sin(phi_pt1);
# # z_pt1=np.cos(theta_pt1)



# # x_pt=[x_pt1[0], 0, x_pt1[-1]];
# # y_pt=[y_pt1[0], 0, y_pt1[-1]];
# # z_pt=[z_pt1[0], 0, z_pt1[-1]];

# #
# #x_pt2=sin(theta_pt2)*cos(phi_pt2);
# #y_pt2=sin(theta_pt2)*sin(phi_pt2);
# #z_pt2=cos(theta_pt2)



# # mlab.points3d(S1,S2,S3,opacity=0.95,color=(0,0,0),scale_factor=.2)
# # # mlab.points3d(x_pt,y_pt,z_pt,opacity=0.9,color=(0,0,0),scale_factor=.05)
# # # mlab.plot3d(x_pt,y_pt,z_pt,opacity=0.75,tube_radius=0.01)
#contour3d(x,y,z,z)

# mlab.show()






# mlab.outline()



