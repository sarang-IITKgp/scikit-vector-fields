""" Code to visualize 3D scalar and vector fields"""



################################################################################
######################## Import Libraries ######################################


import numpy as np # For numerical function

import matplotlib.pyplot as plt # For 2D plot
import matplotlib as mpl


import skvf as vf

import mayavi.mlab as mlab

# import sys as sys

from os.path import dirname, realpath
import sys


import pandas as pd

#########################################


##### code to get filename. 

path=dirname(realpath(sys.argv[0])) ## get path of the current directory.

# filename = 'Near_H_Table_5X6X7.csv'
filename = 'Near_H_Table_1_SIW_tapered_slot.csv'

fullname = path+'/'+filename
# filename = path+'/bondwire_touchstone.s2p'
# filename = path+'/bondwire_touchstone_test.s2p'

# f = open(fullname,'r')

df = pd.read_csv(fullname)


print(fullname)
# print(f)

df_key = df.columns
print(df_key)
print(df_key[0],df_key[1],df_key[3],df_key[5],df_key[5],df_key[7])

def load_HFSS_field_file(filename,text_tag=None):
	'''Exported file contains following data columns:
	 Z, Y, Freq, X, F_total, Fx, Fy, Fz''' 
	path=dirname(realpath(sys.argv[0])) ## get path of the current directory.
	fullname = path+'/'+filename
	
	df = pd.read_csv(fullname)
	print('Loading file: ',fullname, 'as data frame')
	
	df_key = df.columns
	column_mapping = {
	'Z_sweep': df_key[0],
	'Y_sweep':df_key[1],
	'X_sweep':df_key[3],
	'Fx_sweep':df_key[5],
	'Fy_sweep':df_key[6],
	'Fz_sweep':df_key[7]
	}
	
	print('Extracting columns and mapping to the variables as below')
	print(column_mapping)
	
	
	
	x_range_rep = np.array(df[column_mapping['X_sweep']])
	y_range_rep = np.array(df[column_mapping['Y_sweep']])
	z_range_rep = np.array(df[column_mapping['Z_sweep']])


	x_rep = np.nonzero(np.diff(x_range_rep))[0][0]+1
	y_rep = np.nonzero(np.diff(y_range_rep))[0][0]+1
	z_rep = np.nonzero(np.diff(z_range_rep))[0][0]+1

	N_total = x_range_rep.size


	if z_rep >1:
		n_z_count = N_total/z_rep
		if y_rep >1:
			n_y_count = N_total/(n_z_count*y_rep)
			n_x_count = N_total/(n_z_count*n_y_count)
			




	print('====== Number of points ======')
	print('x count = ',n_x_count)
	print('y count = ',n_y_count)
	print('z count = ',n_z_count)


	def fun_arrange_in_grid(var_1d_array,n_z_count,n_y_count,n_x_count):
		var_grid = var_1d_array.reshape(int(n_z_count),int(n_y_count),int(n_x_count)).transpose(1,2,0)
		return var_grid

	x_grid = fun_arrange_in_grid(x_range_rep,n_z_count,n_y_count,n_x_count)*1000
	y_grid = fun_arrange_in_grid(y_range_rep,n_z_count,n_y_count,n_x_count)
	z_grid = fun_arrange_in_grid(z_range_rep,n_z_count,n_y_count,n_x_count)


	Fx_range_rep = np.array(df[column_mapping['Fx_sweep']].str.replace('i', 'j').str.replace(' ', '').astype(complex))
	Fy_range_rep = np.array(df[column_mapping['Fy_sweep']].str.replace('i', 'j').str.replace(' ', '').astype(complex))
	Fz_range_rep = np.array(df[column_mapping['Fz_sweep']].str.replace('i', 'j').str.replace(' ', '').astype(complex))
	
	print('vector field loaded')


	Fx_grid = fun_arrange_in_grid(Fx_range_rep,n_z_count,n_y_count,n_x_count)
	Fy_grid = fun_arrange_in_grid(Fy_range_rep,n_z_count,n_y_count,n_x_count)
	Fz_grid = fun_arrange_in_grid(Fz_range_rep,n_z_count,n_y_count,n_x_count)



	F_vec = vf.entities.vector(Fx_grid,Fy_grid,Fz_grid)



	space = vf.entities.space(grid=True,x_grid=x_grid,y_grid = y_grid,z_grid=z_grid)
	
	x = space.x 
	y = space.y 
	z = space.z 
	space1 = vf.entities.space(x,y,z) # This is done because space.plane is not defined when initiating space object with grid=True definition. 
	
	# ######### Define vector field ##############

	F_field = vf.entities.field(F_vec,space1,text_tag='Magnetic from the loaded file')
	
	if text_tag == None:
		F_field.text_tag = filename
	else:
		F_field.text_tag = text_tag
	
	return F_field

# E_field = load_HFSS_field_file('Near E Table_WithoutSlot_21X21X21.csv',text_tag='E-WOS')
# E_field_slot = load_HFSS_field_file('Near E Table_TaperedSlot_21X21X21.csv',text_tag='E-WTS')
E_field_slot = load_HFSS_field_file('Near E Table regionportion_30X30X30.csv',text_tag='E-WTS')
# E_field = load_HFSS_field_file('Near E Table for entire region 21X21X21.csv',text_tag='E')

# H_field = load_HFSS_field_file('Near H Table_WithoutSlot_21X21X21.csv',text_tag='H-WOS')
# # H_field = load_HFSS_field_file('Near H Table_WithoutSlot_21X21X21.csv',text_tag='H-WOS')

# H_field = load_HFSS_field_file('Near H Table for entire region 21X21X21.csv',text_tag='H')
# H_field_slot = load_HFSS_field_file('Near H Table_TaperedSlot_21X21X21.csv',text_tag='H-WTS')
H_field_slot = load_HFSS_field_file('Near H Table regionportion_30X30X30.csv',text_tag='H-WTS')

# H_field = load_HFSS_field_file('Near_H_Table_1_SIW_tapered_slot.csv')

# Pv_field = E_field^H_field.conjugate()
Pv_field_slot = E_field_slot^H_field_slot.conjugate()



# S0 = H_field.field.magnitude()
# # S0_field = vf.entities.field(S0,space1)

# S_h_vec_field = (H_field^H_field.conjugate()).imag()
S_h_vec_field = (H_field_slot^H_field_slot.conjugate()).imag()


# S_h_z = S_h_vec_field.field.z #/S0_field.field
# S_spin = vf.entities.field(S_h_z,H_field.space) # Scalar field. 

z_loc = 0.0

fig1 = plt.figure('Some field')
# ax1_f1 = fig1.add_subplot(311)
ax2_f1 = fig1.add_subplot(312)
# ax3_f1 = fig1.add_subplot(313)
# # ax1_f1.contourf(H_field.field.real().x,space1.x_grid[3,:,]
# H_field.real().plot_quiver2d(plane='x-y',loc=z_loc,ax=ax1_f1)
# H_field.real().plot_streamplot(plane='x-y',loc=z_loc,ax=ax2_f1)


# # S_h.imag().plot_contourf(plane='x-y',loc=0.28,ax=ax2_f1)
# S_spin.plot_contourf(plane='x-y',loc=z_loc,ax=ax2_f1)
S_h_vec_field.plot_contourf(plane='x-y',loc=z_loc,ax=ax2_f1)
# # S0_field.real().plot_contourf(plane='x-y',loc=z_loc,ax=ax3_f1)


# # ax1_f1.quiver(space1.x_grid[:,:,3],space1.y_grid[:,:,3],np.real(Hx_grid[:,:,3]),np.real(Hy_grid[:,:,3]))


# E_field.real().plot_quiver3d()

# H_field.real().plot_quiver3d()

# Pv_field.real().plot_quiver3d()

E_field_slot.real().plot_quiver3d()

H_field_slot.real().plot_quiver3d()

Pv_field_slot.real().plot_quiver3d()

# S_h_vec_field.plot_quiver3d()


plt.show()
