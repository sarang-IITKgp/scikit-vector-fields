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




def A_due_to_dI(dI,r0=None,R_vec=None,space=None):
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
	
	Ax = vf.MU_0/(4*np.pi*(R_vec-r0).magnitude())*dI_vec.x
	Ay = vf.MU_0/(4*np.pi*(R_vec-r0).magnitude())*dI_vec.y
	Az = vf.MU_0/(4*np.pi*(R_vec-r0).magnitude())*dI_vec.z


	return vf.entities.vector(Ax,Ay,Az)

##################### End function definitions #########################
########################################################################


'''Create space'''
x = np.linspace(-5,5,80)
y = np.linspace(-5,5,80)
# x = np.linspace(-1,1,50)
# y = np.linspace(-1,1,40)
z = np.linspace(-4,4,80)


space_xy = vf.entities.space(x=x,y=y)
space_yz = vf.entities.space(y=y,z=z)
space_xz = vf.entities.space(x=x,z=z)

space1 = vf.entities.space(x=x,y=y,z=z)

# space1.shift_x(3)

R_vec = space1.vec()


'''Define current loop'''

pts_theta = 100
N=3
theta = np.linspace(0,N*2*np.pi,pts_theta)
theta=theta[0:-1]
dI_vec_list = []

a = 0.5
p = 0.5*1/(2*np.pi)


for theta_count in theta:
	# dI_vec_list.append((np.cos(theta_count),np.sin(theta_count)))
	dI_count = vf.entities.vector(np.cos(np.pi/2+theta_count),np.sin(np.pi/2+theta_count),0)
	
	position_count = vf.entities.vector(a*np.cos(theta_count),a*np.sin(theta_count),p*theta_count)
	 
	# dI_vec_list.append((dI_count,position_count))
	dI_vec_list.append(vf.entities.source(dI_count,position_count))

dI_vec = vf.entities.vector(np.cos(np.pi/2+theta),np.sin(np.pi/2+theta),0)
r0_vec = vf.entities.vector(a*np.cos(theta),a*np.sin(theta),p*theta)


# dI_vec_list2 = dI_vec_list.copy()
dI_vec_list2 = copy.deepcopy(dI_vec_list)

r_s = vf.entities.vector(1.5,0,0)

for dI_vec_count in dI_vec_list:
	dI_vec_count.shift_r(-r_s)

for dI_vec_count in dI_vec_list2:
	dI_vec_count.shift_r(r_s)
	dI_vec_count.source = -dI_vec_count.source
	# dI_vec_list2.append(dI_vec_count.shift_r(r_s))
	# dI_vec_list2.append(dI_vec_count.shift_r(-2*r_s))

# print(dI_vec_list2)

dI_vec_list3 = dI_vec_list+dI_vec_list2
# current1 = vf.entities.source(dI_vec,r0_vec,'dI loop')
# print(current1.source.dim)
# print(R_vec.dim)
# print(R_vec.


# for count_dim  in current1.source.shape:
	# print(count_dim)


# print(type(dI_vec))
# print(dI_vec.shape)
# print(type(r0_vec))
# print(r0_vec.shape)
# print(R_vec.shape)

# print(dI_vec.shape == r0_vec.shape)
# A_field = 0

# print(dI_vec_list)

A_vec = vf.entities.vector(0,0,0)
A_field = vf.entities.zero_field_vector_like(space1)

# print(len(dI_vec_list3))
print(A_field.field_type)
for dI_count in dI_vec_list3:
	# dI_count.shift_x(-1.5)
	# A_count = A_due_to_current(dI_vec = dI_count[0],space=space1,r0=dI_count[1])
	A_count = A_due_to_dI(dI_count,space=space1)
	# A_field  = A_field + A_due_to_current(dI_vec = dI_count[0],space=space1,r0=dI_count[1])
	A_field = A_field+vf.entities.field(A_count,space1,'A_dI')
A_field.text_tag = 'A total'


# def A_total(current,space):
	# # A_field = vf.entities.zero_field_vector_like(space)
	# list_of_source = []
	
	# if current.source.dim == 1:
		# # current_count
		# for count in range(current.source.shape[0]):
			
			# # A_field = A_field + A_due_to_dI(current.source[count],current.r0[count],space)
			# # print(count)
			
			# dI_count = vf.entities.vector(current.source.x[cout],current.source.y[cout],current.source.z[cout])
			
			# r0_count = vf.entities.vector(current.r0.x[count],current.r0.y[count],current.r0.z[count])
			
			# source_count = vf.entities.source(dI_count,r0_count)
			# list_of_source.append(source_count)
			# # print(count,current.source.x[count])
			
	# return list_of_source

# current1 = 
# A_total(current1,space1)
	


# A_field.space.shift_x(3)
# charge

V = potential_of_charge(1,space=space1,r0=vf.entities.vector(0.75,0,0))
# V2 = potential_of_charge(1,space=space1,r0=vf.entities.vector(0,0,0))

V_field = vf.entities.field(V,space1,text_tag='Potential')

E_field = -V_field.gradient()
rho_field = vf.EPSILON_0*E_field.div()

# dict1 = {'dI': vf.entites.vector(1,0,0), 'r0': vf.entities.vector(1,0,0) }
# # current_elements = [{'dI': vf.entites.vector(1,0,0), 'r0': vf.entities.vector(1,0,0)} ]

# current_elements.append({'dI':vf.entites.vector(1,0,0}, 'r0':vf.entities.vector(-1,0,0)})

# A_vec = 0

# for element in current_elements:
    # A_vec = A_vec+A_due_to_current(dI_vec=element['dI'],space=space1,r0=element['r0'])

# A_vec1 = A_due_to_current(dI_vec=vf.entities.vector(0,0,1),space=space1,r0=vf.entities.vector(1,0,0))
# A_vec2 = A_due_to_current(dI_vec=vf.entities.vector(0,0,-1),space=space1,r0=vf.entities.vector(-1,0,0))


# A_vec = 0
# A_vec = A_vec + A_vec1
# print('hahah',A_vec.shape)
# print('-------- Define Fields ---------')

# A_field1 = vf.entities.field(A_vec1,space1,text_tag='A1')
# A_field2 = vf.entities.field(A_vec2,space1,text_tag='A2')

# A_field = A_field1 + A_field2 #+ A_field
# A_field3 =  A_field 
# V_field1 = vf.entities.field(V1,space1,text_tag='V1')
# V_field2 = vf.entities.field(V2,space1,text_tag='V2')
# # V_field = vf.entities.field(V,space1,text_tag='V1+V2')
# V_field = V_field1+V_field2

# E_field = -V_field.grad()

H_field = A_field.curl()*(1/vf.MU_0)

Poynting = E_field^H_field

J_field = H_field.curl()
J_field.text_tag ='Current'


'''Plot commands '''
### Plot commands

print('--------------Testing plot module-------------')
# H_field.field.text_tag = 'H_field'
H_field.text_tag = 'H_field'

# Fig_m = E_field.plot_quiver3d()
# H_field.plot_quiver3d()
# H_field.plot_volume_slice()
# J_field.plot_volume_slice()


# Poynting.plot_quiver3d()
# Poynting.plot_quiver2d(plane='x-y')
# Fig = vf.plot.volume_slice(V_field.space,V_field.field,Fig=Fig_m)


loc=0
# Poynting.plot_streamplot(plane='x-y',loc=loc)
# Poynting.plot_streamplot(plane='x-z',loc=loc)

ax_J, Fig_j = J_field.plot_contourf(plane='x-y',loc=loc,cmap='hot')
J_field.plot_quiver2d(plane='x-y',loc=loc,ax=ax_J)


Fig1 = plt.figure('H field vector')
ax = Fig1.subplots(1,3)
# ax1 = Fig1.add_subplot(2,2,1)
# ax2 = Fig1.add_subplot(2,2,2,sharex)
# ax3 = Fig1.add_subplot(2,2,3)



# Poynting.plot_contourf(plane='x-y',loc=loc,ax=ax[0])
# # Poynting.plot_streamplot(plane='x-y',loc=loc,ax=ax[0])
# Poynting.plot_streamplot(plane='y-z',loc=loc,ax=ax[1])
# Poynting.plot_streamplot(plane='x-z',loc=loc,ax=ax[2])


# ax, Fig = E_field.plot_quiver2d(plane='x-y',loc=loc)
# ax, Fig = H_field.plot_quiver2d(plane='x-y',loc=loc)
H_field.plot_streamplot(plane='x-y',loc=loc,ax=ax[0])
H_field.plot_streamplot(plane='y-z',loc=loc,ax=ax[1])
H_field.plot_streamplot(plane='x-z',loc=loc,ax=ax[2])
# H_field.plot_quiver2d(plane='x-z',loc=loc,ax=ax[2],scale)
# J_field.plot_contourf(plane='x-y',loc=loc)
# H_field.plot_quiver3d(1)
# A_field.plot_quiver3d(0.9)

Fig_m = mlab.figure('Current and H field')
Fig_m = H_field.plot_quiver3d(Fig=Fig_m,arrow_density=0.02,colormap='hot')
# J_field.plot_quiver3d(arrow_density=0.9,scale_mode='scalar')
# print('===================== hahaha')
# print(Fig_m)
J_field.plot_contour3d(Fig=Fig_m,contours=[np.max(J_field.field.magnitude())*0.1])
# J_field.plot_quiver3d(Fig=Fig_m,scale_mode='vector')#,contours=[np.max(J_field.field.magnitude())*0.01])
# J_field.plot_contour3d(Fig=Fig_m)#,contours=[np.max(J_field.field.magnitude())*0.1])



Fig_E = mlab.figure('Charge and E field')
Fig_E = E_field.plot_quiver3d(Fig=Fig_E,arrow_density=0.2,colormap='hsv')
# Fig_E = rho_field.plot_contour3d(Fig=Fig_m,contours=[np.max(abs(rho_field.field))*0.01])

# Fig_E = rho_field.plot_contour3d(Fig=Fig_m)#,contours=[np.max(abs(rho_field.field))*0.01])


Fig_P = mlab.figure('Poynting vector')
Fig_P = Poynting.plot_quiver3d(Fig=Fig_P,arrow_density=0.2,colormap='hot')


Fig_p_2d = plt.figure('Poynting vector')
ax_p = Fig_p_2d.subplots(1,3)
Poynting.plot_quiver2d(plane='x-y',ax=ax_p[0])
Poynting.plot_quiver2d(plane='y-z',ax=ax_p[1])
Poynting.plot_quiver2d(plane='x-z',ax=ax_p[2])

# scalars = space1.x_grid * space1.x_grid * 0.5 + space1.y_grid * space1.y_grid + space1.z_grid * space1.z_grid * 2.0

# obj = mlab.volume_slice(np.transpose(E_field.space.y_grid,axes=[1,0,2]),np.transpose(E_field.space.x_grid,axes=[1,0,2]),np.transpose(E_field.space.z_grid,axes=[1,0,2]),np.transpose(E_field.field.x,axes=[1,0,2]), plane_orientation='x_axes')
# obj = mlab.volume_slice(np.transpose(E_field.field.x,axes=[1,0,2]), plane_orientation='x_axes')
# obj = mlab.volume_slice(np.transpose(E_field.field.z,axes=[1,0,2]), plane_orientation='z_axes')
# obj = mlab.volume_slice(np.transpose(E_field.field.y,axes=[1,0,2]), plane_orientation='y_axes')
# obj = mlab.quiver3d(np.transpose(E_field.field.x,axes=[1,0,2]),np.transpose(E_field.field.y,axes=[1,0,2]),np.transpose(E_field.field.z,axes=[1,0,2]),scale_mode='none',mask_points=10)
# obj = mlab.volume_slice(space1.x_grid,space1.y_grid,space1.z_grid,E_field.field.x, plane_orientation='x_axes')


# Fig_m = vf.plot.volume_slice_vector(E_field.field) 

# print(np.shape(E_field.field.x))
# print(np.shape(np.transpose(E_field.field.x,axes=[1,0,2])))


plt.show()
