'''Functions related to data handling'''
import numpy as np # For numerical function

# import matplotlib.pyplot as plt # For 2D plot
# import matplotlib as mpl

from . import entities 

# import skvf as vf

import mayavi.mlab as mlab

# import sys as sys

# from os.path import dirname, realpath
import sys


import pandas as pd
import re



def get_text_between_strings_regex(main_string, start_pattern, end_pattern=None):
	# The non-greedy quantifier (.*?) ensures it matches the shortest possible string
	if end_pattern != None:
		pattern = re.compile(f"{re.escape(start_pattern)}(.*?){re.escape(end_pattern)}")
		match = pattern.search(main_string)
		text = match.group(1)
	if end_pattern == None:
		pattern = re.compile(f"{re.escape(start_pattern)}(.*)")
		match = pattern.search(main_string)
		# text = match.group(1)
	if match:
		return match.group(1)
	return None

def load_HFSS_field_file(fullname,text_tag=None):
	'''Exported file contains following data columns:
	 Z, Y, Freq, X, F_total, Fx, Fy, Fz''' 
	# path=dirname(realpath(sys.argv[0])) ## get path of the current directory.
	# fullname = path+'/'+filename
	
	df = pd.read_csv(fullname)
	print('Loading file: ',fullname, 'as data frame')
	
	df_key = df.columns
	column_mapping = {
	'Z_sweep': df_key[0],
	'Y_sweep':df_key[1],
	'X_sweep':df_key[3],
	'Fx_sweep':df_key[5],
	'Fy_sweep':df_key[6],
	'Fz_sweep':df_key[7],
	'Freq':df_key[2],
	}
	
	def extract_units(col_text):
		units_text = get_text_between_strings_regex(col_text,start_pattern='[',end_pattern=']')
		return units_text
		
	
	
	print('Extracting columns and mapping to the variables as below')
	print(column_mapping)
	
	x_unit = extract_units(column_mapping['X_sweep'])
	y_unit = extract_units(column_mapping['Y_sweep'])
	z_unit = extract_units(column_mapping['Z_sweep'])
	
	freq_unit = extract_units(column_mapping['Freq'])
	
	scale_dict = {
	'': 1,
	'mm':1e-3,
	'mum':1e-6,
	'GHz':1e9
	}
	
	x_scale = scale_dict[x_unit]
	print(x_scale)
	y_scale = scale_dict[y_unit]
	print(y_scale)
	z_scale = scale_dict[z_unit]
	print(z_scale)
	print('hahaha, Running function from SKVF')
	print(column_mapping['X_sweep'],x_unit)
	print(column_mapping['Y_sweep'],y_unit)
	print(column_mapping['Z_sweep'],z_unit)
	
	
	TH_freq = np.array(df[column_mapping['Freq']][0])
	TH_omega = 2*np.pi*scale_dict[freq_unit]*TH_freq
	
	print('omega = ',TH_omega, 'and freq in ',freq_unit,' is', TH_omega/(2*np.pi*1e9) )
	
	
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

	x_grid = fun_arrange_in_grid(x_range_rep,n_z_count,n_y_count,n_x_count)*x_scale
	y_grid = fun_arrange_in_grid(y_range_rep,n_z_count,n_y_count,n_x_count)*y_scale
	z_grid = fun_arrange_in_grid(z_range_rep,n_z_count,n_y_count,n_x_count)*z_scale


	Fx_range_rep = np.array(df[column_mapping['Fx_sweep']].str.replace('i', 'j').str.replace(' ', '').astype(complex))
	Fy_range_rep = np.array(df[column_mapping['Fy_sweep']].str.replace('i', 'j').str.replace(' ', '').astype(complex))
	Fz_range_rep = np.array(df[column_mapping['Fz_sweep']].str.replace('i', 'j').str.replace(' ', '').astype(complex))
	
	print('vector field loaded')


	Fx_grid = fun_arrange_in_grid(Fx_range_rep,n_z_count,n_y_count,n_x_count)
	Fy_grid = fun_arrange_in_grid(Fy_range_rep,n_z_count,n_y_count,n_x_count)
	Fz_grid = fun_arrange_in_grid(Fz_range_rep,n_z_count,n_y_count,n_x_count)



	F_vec = entities.vector(Fx_grid,Fy_grid,Fz_grid)



	space1 = entities.space(grid=True,x_grid=x_grid,y_grid = y_grid,z_grid=z_grid)
	
	# x = space.x 
	# y = space.y 
	# z = space.z 
	# space1 = vf.entities.space(x,y,z) # This is done because space.plane is not defined when initiating space object with grid=True definition. 
	
	# ######### Define vector field ##############

	F_field = entities.field(F_vec,space1,TH_omega = TH_omega)
	
	if text_tag == None:
		F_field.text_tag = filename
	else:
		F_field.text_tag = text_tag
	
	return F_field
