import numpy as np
"""Plot commands"""
import matplotlib.pyplot as plt

import mayavi.mlab as mlab
import sys as sys


import matplotlib as mpl
mpl.rc('axes',labelsize=24)
mpl.rc('font',size=24)




def quiver2d(space,vector,plane=None,loc=0,ax=None,Fig=None,color=True,cmap='jet',text_tag=None):
	
	
	if text_tag == None:
		text_tag = vector.text_tag
		
	print('Plotting: '+text_tag)
	if ax == None:
		if Fig == None:
			Fig = plt.figure(text_tag)
		
		ax = Fig.add_subplot(111)
			
			
	if space.plane == 'x-y-z-3D':
		
		if plane == 'x-y' or plane == 'y-x':
			index_of_plane = (abs(space.z-loc)).argmin()
			var1 = space.x_grid[:,:,index_of_plane]
			var2 = space.y_grid[:,:,index_of_plane]
			data1 = vector.x[:,:,index_of_plane]
			data2 = vector.y[:,:,index_of_plane]
			print('x-y plane selected. Location of z = ',space.z[index_of_plane])
			xlabel = 'x'
			ylabel = 'y'
			
		elif plane == 'y-z' or plane == 'z-y':
			index_of_plane = (abs(space.x-loc)).argmin()
			var1 = space.y_grid[:,index_of_plane,:]
			var2 = space.z_grid[:,index_of_plane,:]
			data1 = vector.y[:,index_of_plane,:]
			data2 = vector.z[:,index_of_plane,:]
			print('y-z plane selected. Location of x = ',space.x[index_of_plane])
			xlabel = 'y'
			ylabel = 'z'
			
		elif plane == 'x-z' or plane == 'z-x':
			index_of_plane = (abs(space.x-loc)).argmin()
			var1 = space.x_grid[index_of_plane,:,:]
			var2 = space.z_grid[index_of_plane,:,:]
			data1 = vector.x[index_of_plane,:,:]
			data2 = vector.z[index_of_plane,:,:]
			print('x-z plane selected. Location of y = ',space.y[index_of_plane])
			xlabel = 'x'
			ylabel = 'z'
			
		else:
			sys.exit('x-y, y-z or z-x plane must be defined to generate 2D plot from 3D data. Abort...!!!')
			
					
			
	if space.plane == 'x-y':
		var1 = space.x_grid[:,:,0]
		var2 = space.y_grid[:,:,0]
		data1 = vector.x[:,:,0] 
		data2= vector.y[:,:,0]
		xlabel = 'x'
		ylabel = 'y'
	if space.plane == 'y-z':
		var1 = space.y_grid[:,0,:]
		var2 = space.z_grid[:,0,:]

		data1 = vector.y[:,0,:]
		data2 =vector.z[:,0,:]
		xlabel = 'y'
		ylabel = 'z'
	if space.plane == 'x-z':
		var1 = space.x_grid[0,:,:]
		var2 = space.z_grid[0,:,:] 
		data1 = vector.x[:,0,:]
		data2 = vector.z[:,0,:]
		xlabel = 'x'
		ylabel = 'z'
		

	print(np.shape(data1))
	print(np.shape(var1))
	print(np.shape(data2))
	print(np.shape(var2))
	mag = np.sqrt(data1**2 + data2**2)
	if color == True:
		ax.quiver(var1,var2,data1,data2,mag,pivot='mid',cmap=cmap)
	else:
		ax.quiver(var1,var2,data1,data2,pivot='mid')
	ax.set_aspect('equal')
	ax.set_xlabel(xlabel)
	ax.set_ylabel(ylabel)
	return ax, Fig
				
				
				
	
def streamplot(space,vector,plane=None,loc=0,ax=None,Fig=None,color=True,cmap='jet',text_tag=None):
	
	
	if text_tag == None:
		text_tag = vector.text_tag
	
	
	print('Plotting: '+text_tag)
	if ax == None:
		if Fig == None:
			Fig = plt.figure(text_tag)
		
		ax = Fig.add_subplot(111)
			
			
	if space.plane == 'x-y-z-3D':
		
		if plane == 'x-y' or plane == 'y-x':
			index_of_plane = (abs(space.z-loc)).argmin()
			var1 = space.x_grid[:,:,index_of_plane]
			var2 = space.y_grid[:,:,index_of_plane]
			data1 = vector.x[:,:,index_of_plane]
			data2 = vector.y[:,:,index_of_plane]
			print('x-y plane selected. Location of z = ',space.z[index_of_plane])
			xlabel = 'x'
			ylabel = 'y'
			
		elif plane == 'y-z' or plane == 'z-y':
			index_of_plane = (abs(space.x-loc)).argmin()
			var1 = space.y_grid[:,index_of_plane,:].transpose()
			var2 = space.z_grid[:,index_of_plane,:].transpose()
			data1 = vector.y[:,index_of_plane,:].transpose()
			data2 = vector.z[:,index_of_plane,:].transpose()
			print('y-z plane selected. Location of x = ',space.x[index_of_plane])
			xlabel = 'y'
			ylabel = 'z'
			
		elif plane == 'x-z' or plane == 'z-x':
			index_of_plane = (abs(space.x-loc)).argmin()
			var1 = space.x_grid[index_of_plane,:,:].transpose()
			var2 = space.z_grid[index_of_plane,:,:].transpose()
			data1 = vector.x[index_of_plane,:,:].transpose()
			data2 = vector.z[index_of_plane,:,:].transpose()
			print('x-z plane selected. Location of y = ',space.y[index_of_plane])
			xlabel = 'x'
			ylabel = 'z'
			
		else:
			sys.exit('x-y, y-z or z-x plane must be defined to generate 2D plot from 3D data. Abort...!!!')
			
					
			
	if space.plane == 'x-y':
		var1 = space.x_grid[:,:,0]
		var2 = space.y_grid[:,:,0]
		data1 = vector.x[:,:,0] 
		data1= vector.y[:,:,0]
		xlabel = 'x'
		ylabel = 'y'
	if space.plane == 'y-z':
		var1 = space.y_grid[:,0,:].transpose()
		var2 = space.z_grid[:,0,:].transpose()
		data1 = vector.y[:,0,:].transpose()
		data2 =vector.z[:,0,:].transpose()
		xlabel = 'y'
		ylabel = 'z'
	if space.plane == 'x-z':
		var1 = space.x_grid[0,:,:].transpose()
		var2 = space.z_grid[0,:,:].transpose() 
		data1 = vector.x[0,:,:].transpose()
		data2 = vector.z[0,:,:].transpose()
		xlabel = 'x'
		ylabel = 'z'
		

	print(np.shape(data1))
	print(np.shape(var1))
	print(np.shape(data2))
	print(np.shape(var2))
	mag = np.sqrt(data1**2 + data2**2)
	if color == True:
		ax.streamplot(var1,var2,data1,data2,color=mag,cmap=cmap)
	else:
		ax.streamplot(var1,var2,data1,data2)
		
	ax.set_aspect('equal')
	ax.set_xlabel(xlabel)
	ax.set_ylabel(ylabel)
	return ax, Fig
	
def contourf(space,scalar,plane=None,loc=0,ax=None,Fig=None,color=True,cmap='jet',text_tag='No text tag defined',color_axis=None,vmax=None,vmin=None,flag_colorbar=True):
	"""Plots the contourf of the scalar quantity. """
	import matplotlib as mpl
	
	print('Plotting scalar: '+text_tag)
	if ax == None:
		if Fig == None:
			Fig = plt.figure(text_tag)
		
		ax = Fig.add_subplot(111)
	if color_axis ==  None and flag_colorbar == True and Fig !=None:
		color_axis = Fig.add_axes([0.9,0.1,0.05, 0.8])
			
			
	if space.plane == 'x-y-z-3D':
		pts_y,pts_x,pts_z = space.shape
		
		if plane == 'x-y' or plane == 'y-x':
			index_of_plane = (abs(space.z-loc)).argmin()
			var1 = space.x_grid[:,:,index_of_plane]
			var2 = space.y_grid[:,:,index_of_plane]
			data = scalar[:,:,index_of_plane]
			print('x-y plane selected. Location of z = ',space.z[index_of_plane])
			xlabel = 'x'
			ylabel = 'y'
			
		elif plane == 'y-z' or plane == 'z-y':
			index_of_plane = (abs(space.x-loc)).argmin()
			var1 = space.y_grid[:,index_of_plane,:]
			var2 = space.z_grid[:,index_of_plane,:]
			data = scalar[:,index_of_plane,:]
			print('y-z plane selected. Location of x = ',space.x[index_of_plane])
			xlabel = 'y'
			ylabel = 'z'
			
		elif plane == 'x-z' or plane == 'z-x':
			index_of_plane = (abs(space.x-loc)).argmin()
			var1 = space.x_grid[index_of_plane,:,:]
			var2 = space.z_grid[index_of_plane,:,:]
			data = scalar[index_of_plane,:,:]
			print('y-z plane selected. Location of y = ',space.y[index_of_plane])
			xlabel = 'x'
			ylabel = 'z'
			
		else:
			sys.exit('x-y, y-z or z-x plane must be defined to generate 2D plot from 3D data. Abort...!!!')
			
					
			
	if space.plane == 'x-y':
		var1 = space.x_grid[:,:,0]
		var2 = space.y_grid[:,:,0]
		data = scalar[:,:,0] 
		xlabel = 'x'
		ylabel = 'y'
	if space.plane == 'y-z':
		var1 = space.y_grid[:,0,:]
		var2 = space.z_grid[:,0,:]

		data = scalar[:,0,:]
	
		xlabel = 'y'
		ylabel = 'z'
	if space.plane == 'x-z':
		var1 = space.x_grid[0,:,:]
		var2 = space.z_grid[0,:,:] 
		data = scalar[:,0,:]
		xlabel = 'x'
		ylabel = 'z'
		

	print(np.shape(data))
	print(np.shape(var1))
	print(np.shape(var2))
	
	
    
	if vmin == None: ## Adds color bar to the given axis. 
		vmin=scalar.min()
		
	if vmax == None: ## Adds color bar to the given axis. 
		vmax=scalar.max()
        
    
	if flag_colorbar == True and color_axis != None:
		cmap=mpl.cm.get_cmap(cmap)
		norm=mpl.colors.Normalize(vmin=vmin, vmax=vmax)
    
	# if color_axis != None: ## Adds color bar to the given axis. 
		c_plot = mpl.colorbar.ColorbarBase(ax=color_axis, cmap=cmap, orientation="vertical",norm=norm)
		# if title_name != None:
		c_plot.ax.set_title(text_tag)
	
	
	ax.contourf(var1,var2,data,cmap=cmap,vmax=vmax,vmin=vmin)
	ax.set_aspect('equal')
	ax.set_xlabel(xlabel)
	ax.set_ylabel(ylabel)
	return ax, Fig
	 
	
def quiver3d(space,vector,arrow_density = 0.7,text_tag=None,scale_mode='none',Fig=None,colormap='jet'):
	
	if text_tag == None:
		text_tag = vector.text_tag
	
	if Fig == None:
		Fig = mlab.figure('Mayavi plot: '+text_tag)
	else:
		mlab.figure(Fig)
	
	
	if space.plane == 'x-y-z-3D':
		pts_y,pts_x,pts_z = space.shape
					
		print('Plotting 3D quiver plot of '+text_tag+' using mayavi')
		
		handle_s = mlab.quiver3d(space.x_grid,space.y_grid,space.z_grid, vector.x,vector.y,vector.z,scale_mode=scale_mode,mask_points=int(max([pts_x,pts_y,pts_z])*(1.1-arrow_density)),figure=Fig,colormap=colormap)

		mlab.outline()
		mlab.orientation_axes()
		mlab.axes()
		
	else:
		sys.exit('only 3D vector fields can be plotted using this command.')
	return handle_s, mlab.gcf()
	
def volume_slice_scalar(scalar,Fig=None,colormap='jet',text_tag='scalar field'):
	
	
	if Fig ==  None:
		Fig = mlab.figure('Mayavi volume slice plot:'+text_tag)
	else:
		mlab.figure(Fig)
		
	mlab.volume_slice(np.transpose(scalar,axes=[1,0,2]),figure=Fig,plane_orientation='x_axes')
	mlab.volume_slice(np.transpose(scalar,axes=[1,0,2]),figure=Fig,plane_orientation='y_axes')
	mlab.volume_slice(np.transpose(scalar,axes=[1,0,2]),figure=Fig,plane_orientation='z_axes')
		
	mlab.contour3d(np.transpose(scalar,axes=[1,0,2]),figure=Fig)
	
	mlab.outline()
	mlab.orientation_axes()
	mlab.axes()
	
	return mlab.gcf()

	
def volume_slice_vector(vector,Fig=None,colormap='jet',text_tag='vector field',arrow_density = 0.7,normal_plot=False):
	
	pts_y,pts_x,pts_z = vector.x.shape
	
	if Fig ==  None:
		Fig = mlab.figure('Mayavi volume slice plot:'+text_tag)
	else:
		mlab.figure(Fig)
	
	
	
	
	if normal_plot == True:
		scalar_x_axes = vector.x #np.sqrt(vector.y**2 + vector.z**2)
		scalar_y_axes = vector.y #np.sqrt(vector.x**2 + vector.z**2)
		scalar_z_axes = vector.z #np.sqrt(vector.x**2 + vector.y**2)
		print('Control here')
	else:
		
		scalar_x_axes = np.sqrt(vector.y**2 + vector.z**2)
		scalar_y_axes = np.sqrt(vector.x**2 + vector.z**2)
		scalar_z_axes = np.sqrt(vector.x**2 + vector.y**2)
	
	mlab.volume_slice(np.transpose(scalar_x_axes,axes=[1,0,2]), plane_orientation='x_axes',colormap=colormap)
	mlab.volume_slice(np.transpose(scalar_y_axes,axes=[1,0,2]), plane_orientation='y_axes',colormap=colormap)
	mlab.volume_slice(np.transpose(scalar_z_axes,axes=[1,0,2]), plane_orientation='z_axes',colormap=colormap)

	obj = mlab.quiver3d(np.transpose(vector.x,axes=[1,0,2]),np.transpose(vector.y,axes=[1,0,2]),np.transpose(vector.z,axes=[1,0,2]),scale_mode='none',mask_points=int(max([pts_x,pts_y,pts_z])*(1.1-arrow_density)))

	mlab.outline()
	mlab.orientation_axes()
	mlab.axes()
		
	return mlab.gcf()


def contour3d(space,scalar,Fig=None,colormap='jet',text_tag='field',contours=None):
	if Fig ==  None:
		Fig = mlab.figure('Mayavi contour3d plot:'+text_tag)
	else:
		mlab.figure(Fig)


	if contours == None:
		mlab.contour3d(np.transpose(space.x_grid,axes=[1,0,2]),np.transpose(space.y_grid,axes=[1,0,2]),np.transpose(space.z_grid,axes=[1,0,2]),np.transpose(scalar,axes=[1,0,2]),figure=Fig)
	else:	
		mlab.contour3d(np.transpose(space.x_grid,axes=[1,0,2]),np.transpose(space.y_grid,axes=[1,0,2]),np.transpose(space.z_grid,axes=[1,0,2]),np.transpose(scalar,axes=[1,0,2]),figure=Fig,contours=contours)
	mlab.outline()
	mlab.orientation_axes()
	mlab.axes()
	
	return mlab.gcf()
	
	

def plot_mayavi_quiver(F_field,figure,scale_mode='none',arrow_density=0.7,colormap='jet',line_width=2):
	
	pts_y,pts_x,pts_z = F_field.space.x_grid.shape
	
	sq = mlab.quiver3d(F_field.space.x_grid,F_field.space.y_grid,F_field.space.z_grid, F_field.field.x,F_field.field.y,F_field.field.z,scale_mode=scale_mode,mask_points=int(max([pts_x,pts_y,pts_z])*(1.1-arrow_density)),figure=figure,colormap=colormap,line_width=line_width)
	return sq


def plot_mayavi_points3d(F_field,figure,scale_mode='scalar',point_density=1,colormap='jet',opacity=0.2,vmax=None,vmin=None):
	if vmax == None:
		vmax = np.max(F_field.real().field)
		
	if vmin == None:
		vmin = np.min(F_field.real().field)
		
	pts_y,pts_x,pts_z = F_field.space.x_grid.shape
	
	s = mlab.points3d(F_field.space.x_grid,F_field.space.y_grid,F_field.space.z_grid, F_field.field,scale_mode=scale_mode,mask_points=int(max([pts_x,pts_y,pts_z])*(1.1-point_density)),figure=figure,colormap=colormap,vmax=vmax,vmin=vmin,opacity=opacity,scale_factor=0.05)
	
	return s
