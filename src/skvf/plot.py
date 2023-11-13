import numpy as np
"""Plot commands"""
import matplotlib.pyplot as plt

import mayavi.mlab as mlab
import sys as sys


def quiver2d(space,vector,plane=None,loc=0,ax=None,Fig=None,color=True,cmap='jet'):
	print('Plotting: '+vector.text_tag)
	if ax == None:
		if Fig == None:
			Fig = plt.figure(vector.text_tag)
		
		ax = Fig.add_subplot(111)
			
			
	if space.plane == 'x-y-z-3D':
		# pts_y,pts_x,pts_z = space.shape
		
		if plane == 'x-y' or plane == 'y-x':
			# slice_2d =  
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
			print('y-z plane selected. Location of y = ',space.y[index_of_plane])
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
		var1 = space.y_grid[:,0,:]
		var2 = space.z_grid[:,0,:]

		data1 = vector.y[:,0,:]
		dtaa2 =vector.z[:,0,:]
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
				
				
				
	
def streamplot(space,vector,plane=None,loc=0,ax=None,Fig=None,color=True,cmap='jet'):
	print('Plotting: '+vector.text_tag)
	if ax == None:
		if Fig == None:
			Fig = plt.figure(vector.text_tag)
		
		ax = Fig.add_subplot(111)
			
			
	if space.plane == 'x-y-z-3D':
		# pts_y,pts_x,pts_z = space.shape
		
		if plane == 'x-y' or plane == 'y-x':
			# slice_2d =  
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
			# var1 = space.y_grid[:,index_of_plane,:]
			# var2 = space.z_grid[:,index_of_plane,:]
			# data1 = vector.y[:,index_of_plane,:]
			# data2 = vector.z[:,index_of_plane,:]
			var1 = space.y_grid[:,index_of_plane,:].transpose()
			var2 = space.z_grid[:,index_of_plane,:].transpose()
			data1 = vector.y[:,index_of_plane,:].transpose()
			data2 = vector.z[:,index_of_plane,:].transpose()
			print('y-z plane selected. Location of x = ',space.x[index_of_plane])
			xlabel = 'y'
			ylabel = 'z'
			
		elif plane == 'x-z' or plane == 'z-x':
			index_of_plane = (abs(space.x-loc)).argmin()
			# var1 = space.x_grid[index_of_plane,:,:]
			# var2 = space.z_grid[index_of_plane,:,:]
			# data1 = vector.x[index_of_plane,:,:]
			# data2 = vector.z[index_of_plane,:,:]
			var1 = space.x_grid[index_of_plane,:,:].transpose()
			var2 = space.z_grid[index_of_plane,:,:].transpose()
			data1 = vector.x[index_of_plane,:,:].transpose()
			data2 = vector.z[index_of_plane,:,:].transpose()
			print('y-z plane selected. Location of y = ',space.y[index_of_plane])
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
	if color_axis ==  None and flag_colorbar == True:
		color_axis = Fig.add_axes([0.9,0.1,0.05, 0.8])
			
			
	if space.plane == 'x-y-z-3D':
		pts_y,pts_x,pts_z = space.shape
		
		if plane == 'x-y' or plane == 'y-x':
			# slice_2d =  
			index_of_plane = (abs(space.z-loc)).argmin()
			var1 = space.x_grid[:,:,index_of_plane]
			var2 = space.y_grid[:,:,index_of_plane]
			data = scalar[:,:,index_of_plane]
			# data2 = vector.y[:,:,index_of_plane]
			print('x-y plane selected. Location of z = ',space.z[index_of_plane])
			xlabel = 'x'
			ylabel = 'y'
			
		elif plane == 'y-z' or plane == 'z-y':
			index_of_plane = (abs(space.x-loc)).argmin()
			var1 = space.y_grid[:,index_of_plane,:]
			var2 = space.z_grid[:,index_of_plane,:]
			data = scalar[:,index_of_plane,:]
			# data2 = vector.z[:,index_of_plane,:]
			print('y-z plane selected. Location of x = ',space.x[index_of_plane])
			xlabel = 'y'
			ylabel = 'z'
			
		elif plane == 'x-z' or plane == 'z-x':
			index_of_plane = (abs(space.x-loc)).argmin()
			var1 = space.x_grid[index_of_plane,:,:]
			var2 = space.z_grid[index_of_plane,:,:]
			data = scalar[index_of_plane,:,:]
			# data2 = vector.z[index_of_plane,:,:]
			print('y-z plane selected. Location of y = ',space.y[index_of_plane])
			xlabel = 'x'
			ylabel = 'z'
			
		else:
			sys.exit('x-y, y-z or z-x plane must be defined to generate 2D plot from 3D data. Abort...!!!')
			
					
			
	if space.plane == 'x-y':
		var1 = space.x_grid[:,:,0]
		var2 = space.y_grid[:,:,0]
		data = scalar[:,:,0] 
		# data1= vector.y[:,:,0]
		xlabel = 'x'
		ylabel = 'y'
	if space.plane == 'y-z':
		var1 = space.y_grid[:,0,:]
		var2 = space.z_grid[:,0,:]

		data = scalar[:,0,:]
		# dtaa2 =vector.z[:,0,:]
		xlabel = 'y'
		ylabel = 'z'
	if space.plane == 'x-z':
		var1 = space.x_grid[0,:,:]
		var2 = space.z_grid[0,:,:] 
		data = scalar[:,0,:]
		# data2 = vector.z[:,0,:]
		xlabel = 'x'
		ylabel = 'z'
		

	print(np.shape(data))
	print(np.shape(var1))
	# print(np.shape(data2))
	print(np.shape(var2))
	# mag = np.sqrt(data1**2 + data2**2)
	
	
    
	if vmin == None: ## Adds color bar to the given axis. 
		vmin=scalar.min()
		
	if vmax == None: ## Adds color bar to the given axis. 
		vmax=scalar.max()
        
    
	if flag_colorbar == True:
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
	 
	
def quiver3d(space,vector,cmap='jet',plotting_library='Mayavi',arrow_density = 0.7):
	# print('Plotting: '+vector.text_tag)
	
	if space.plane == 'x-y-z-3D':
		pts_y,pts_x,pts_z = space.shape
		if plotting_library == 'Mayavi':
			
			print('Plotting 3D quiver plot of '+vector.text_tag+' using mayavi')
			fig2_m = mlab.figure('Mayavi plot: '+vector.text_tag)
			# mlab.clf(fig2_m)
			
			# mlab.quiver3d(space.x_grid,space.y_grid,space.z_grid, vector.x,vector.y,vector.z,scale_mode='none',mask_points=int(int(max([pts_x,pts_y,pts_z])*/arrow_density)))
			mlab.quiver3d(space.x_grid,space.y_grid,space.z_grid, vector.x,vector.y,vector.z,scale_mode='none',mask_points=int(max([pts_x,pts_y,pts_z])*(1-arrow_density)))

			mlab.outline()
			mlab.orientation_axes()
			mlab.axes()
		
	else:
		sys.exit('only 3D vector fields can be plotted using this command.')
		
	
