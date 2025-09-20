import numpy as np
from . import plot
import sys as sys

class vector(object):
	def __init__(self,x,y,z,text_tag='vector'):
		''' x, y, z should be arrays of the same size'''
		self.x = x
		self.y = y
		self.z = z
		self.dim=len(np.shape(self.x))
		self.shape=np.shape(self.x)
		self.text_tag =text_tag
		return

	def conjugate(self):
		'''Take complex conjugates of the vector elements'''
		x = np.conjugate(self.x)
		y = np.conjugate(self.y)
		z = np.conjugate(self.z)
		return vector(x,y,z)
	
	def print(self):
		print('----------',self.text_tag,'----------')
		print('x=',self.x)
		print('y=',self.y)
		print('z=',self.z)
		return

	def elements(self):
		""" return the elements of the vector to unpack"""
		return self.x, self.y, self.z
	
	def real(self):
		'''Returns the real components of all the elements'''
		return vector(np.real(self.x),np.real(self.y),np.real(self.z))
	def imag(self):
		'''Returns the real components of all the elements'''
		return vector(np.imag(self.x),np.imag(self.y),np.imag(self.z))
		
	def dot(self,other):
		""" performs dot product. If both the objects are Vector, returns the inner product.
		If one object is vector and other scalar, then multiply the vector with the scalar"""
		
		
		if isinstance(other, vector):
			dot_product = self.x*other.x + self.y*other.y + self.z*other.z
		elif isinstance(other, int) or isinstance(other, float) or isinstance(other,complex):
			dot_product = vector(other*self.x, other*self.y, other*self.z)
		
		return dot_product
		
	def magnitude(self):
		'''returns the magnitude of the vector'''
		return np.sqrt(self.dot(self.conjugate()))
		
	def cross(self,other):
		'''Computes and returns cross product between two vectors'''
		if isinstance(other,vector):
			x = self.y*other.z - self.z*other.y
			y = -1*(self.x*other.z - self.z*other.x)
			z = self.x*other.y - self.y*other.x
			return vector(x,y,z)
		else:
			print('Both objects must be vectors')
			return None
			
    
	def __add__(self,other):
		'''Returns the vector addition of self with other'''
		if isinstance(other,vector):
			x = self.x + other.x
			y = self.y + other.y
			z = self.z + other.z
			return vector(x,y,z)
		else:
			print('Both objects must be vectors')
			return None

	def __sub__(self,other):
		'''Returns the vector subtraction of self with other'''
		if isinstance(other,vector):
			x = self.x - other.x
			y = self.y - other.y
			z = self.z - other.z
			return vector(x,y,z)
		else:
			print('Both objects must be vectors')
			return None
	
	def __mul__(self,other):
		return self.dot(other)
   
	def __rmul__(self,other):
		return self.dot(other)
		
	def __truediv__(self,other):
		return vector(self.x/other,self.y/other,self.z/other)
		
	def __xor__(self,other):
		'''Overloads '^' operator to perform vector cross product'''
		return self.cross(other)
		
	def __neg__(self):
		return vector(-self.x,-self.y,-self.z)
	
class space(object):
	def __init__(self,x=None,y=None,z=None,grid=False,x_grid=None,y_grid=None,z_grid=None,text_tag=None):
		"""check if the data is 1D. If yes, use meshgrid to generate 2D or 3D"""
		
		if grid == False:
			self.x = x
			self.y = y
			self.z = z
			
			
			if (not isinstance(self.x,type(None))) and (not isinstance(self.y,type(None))) and isinstance(self.z,type(None)):
				self.dim = 2
				self.plane = 'x-y'
				self.x_grid, self.y_grid = np.meshgrid(x,y)
				self.z_grid = np.zeros_like(self.x_grid)
				self.shape = (len(self.y),len(self.x),0)
				
				print(self.plane)
				
				
			elif (not isinstance(self.x,type(None))) and (isinstance(self.y,type(None))) and (not isinstance(self.z,type(None))):
				self.dim = 2
				self.plane = 'x-z'
				self.x_grid, self.z_grid = np.meshgrid(x,z)
				self.y_grid = np.zeros_like(self.x_grid)
				self.shape = (len(self.z),0,len(self.x))
				print(self.plane)
				
			elif (isinstance(self.x,type(None))) and (not isinstance(self.y,type(None))) and (not isinstance(self.z,type(None))):
				self.dim = 2
				self.plane = 'y-z'
				self.y_grid, self.z_grid = np.meshgrid(y,z)
				self.x_grid = np.zeros_like(self.y_grid)
				
				self.shape = (0,len(self.z),len(self.y))
				print(self.plane)
				
			elif (not isinstance(self.x,type(None))) and (not isinstance(self.y,type(None))) and (not isinstance(self.z,type(None))):
				self.dim = 3
				self.plane = 'x-y-z-3D'
				self.x_grid, self.y_grid, self.z_grid = np.meshgrid(x,y,z)
				self.shape = (len(self.y),len(self.x),len(self.z))
				print(self.plane)
		if grid == True:
			
			self.x_grid = x_grid
			self.y_grid = y_grid
			self.z_grid = z_grid
			self.x = x_grid[0,:,0]
			self.y = y_grid[:,0,0]
			self.z = z_grid[0,0,:]
			self.shape = (len(self.y),len(self.x),len(self.z))
			self.plane = 'x-y-z-3D'
    
		self.R = np.sqrt(self.x_grid**2 + self.y_grid**2 + self.z_grid**2)
		print('Space is defined')
		
	def vec(self):
		return vector(self.x_grid,self.y_grid,self.z_grid)
		

class field():
	def __init__(self,field,space,text_tag='text tag',field_type=None,TH_omega=None):
		"""Check if vector and space are of the same dimensions and size"""
		print('Defining field')
		self.space = space
		self.text_tag = text_tag
		self.TH_omega = TH_omega
		if isinstance(field,vector):
			self.field = field
			self.field_type = 'vector'
			print('Vector field: ' + self.text_tag + ' defined.')
		else:
			self.field = field
			self.field_type = 'scalar'
			print('Scalar field: ' + self.text_tag + ' defined.')
			
		
		return    
	def div(self):
		if isinstance(self.field,vector):
			from .operations import divergence
			print('Computing divergence of '+self.text_tag)
			div_field = divergence(self.field,self.space)
		else: 
			sys.exit('Semantic Error: cannot compute divergence of scalar field. Abort..!!')
		return field(div_field,self.space,text_tag='div('+self.text_tag+')')
		
	def divergence(self):
		return self.div()
		

	def curl(self):
		if isinstance(self.field,vector):
			from .operations import curl
			print('Computing curl of '+self.text_tag)
			curl_field = curl(self.field,self.space)
		else: 
			sys.exit('Semantic Error: cannot compute curl of scalar field. Abort..!!')
		return field(curl_field,self.space,text_tag='curl('+self.text_tag+')')

	def grad(self):
		if isinstance(self.field,vector):
			sys.exit('Semantic Error: cannot compute gradient of vector field. Abort..!!')
		else: 
			from .operations import gradient
			print('Computing gradient of '+self.text_tag)
			grad_field = gradient(self.field,self.space)
		return field(grad_field,self.space,text_tag='grad('+self.text_tag+')')

	def gradient(self):
		return self.grad()
		
	def conjugate(self):
		'''Take complex conjugates of the vector elements'''
		if self.field_type == 'vector':
			return field(self.field.conjugate(),self.space,text_tag = '('+self.text_tag+')*')
		else:
			return field(np.conjugate(self.field),self.space,text_tag = '('+self.text_tag+')*')
		
	def real(self):
		'''Returns the real components of all the elements'''
		if self.field_type == 'vector':
			return field(self.field.real(),self.space,text_tag='Re('+self.text_tag+')')
		if self.field_type == 'scalar':
			return field(np.real(self.field),self.space,text_tag='Re('+self.text_tag+')')
			
	def imag(self):
		'''Returns the real components of all the elements'''
		if self.field_type == 'vector':
			return field(self.field.imag(),self.space,text_tag='Im('+self.text_tag+')')
		if self.field_type == 'scalar':
			return field(np.imag(self.field),self.space,text_tag='Im('+self.text_tag+')')
			


	def return_field_at_point(self,r0):
		"""Returns the  value of field at (closest to) location r0"""
		
		x0 = r0.x
		y0 = r0.y
		z0 = r0.z
		space = self.space
		
		index_of_x = (abs(space.x-x0)).argmin()
		index_of_y = (abs(space.y-y0)).argmin()
		index_of_z = (abs(space.z-z0)).argmin()
		
		x_pt = space.x[index_of_x]
		y_pt = space.y[index_of_y]
		z_pt = space.z[index_of_z]
		
		
		if self.field_type=='vector':
			vector_field = self.field
			field_value_at_r0 = vector(vector_field.x[index_of_y,index_of_x,index_of_z],vector_field.y[index_of_y,index_of_x,index_of_z],vector_field.z[index_of_y,index_of_x,index_of_z])
			
		
		
		
		if self.field_type=='scalar':
			scalar_field = self.field
			field_value_at_r0 = scalar_field[index_of_y,index_of_x,index_of_z]
			
		
		r_pt = vector(x_pt,y_pt,z_pt)
		
		
		return field_value_at_r0, r_pt


	def return_field_in_plane(self,plane,loc):
		
		if plane == 'x-y' or plane == 'y-x':
			index_of_plane = (abs(self.space.z-loc)).argmin()
			x_grid_slice = np.array([self.space.x_grid[:,:,index_of_plane]])
			y_grid_slice= np.array([self.space.y_grid[:,:,index_of_plane]])
			z_grid_slice= np.array([self.space.z_grid[:,:,index_of_plane]])
			
			
			if self.field_type == 'vector':
				Field_x = np.array([self.field.x[:,:,index_of_plane]])
				Field_y = np.array([self.field.y[:,:,index_of_plane]])
				Field_z = np.array([self.field.z[:,:,index_of_plane]])
				print('x-y plane sliced. Location of z = ',self.space.z[index_of_plane])
			if self.field_type =='scalar':
				Field = np.array([self.field[:,:,index_of_plane]])
				print('x-y plane sliced. Location of z = ',self.space.z[index_of_plane])
			
		elif plane == 'y-z' or plane == 'z-y':
			index_of_plane = (abs(self.space.x-loc)).argmin()
			x_grid_slice = np.array([self.space.x_grid[:,index_of_plane,:]])
			y_grid_slice= np.array([self.space.y_grid[:,index_of_plane,:]])
			z_grid_slice= np.array([self.space.z_grid[:,index_of_plane,:]])
			
			
			if self.field_type == 'vector':
				Field_x = np.array([self.field.x[:,index_of_plane,:]])
				Field_y = np.array([self.field.y[:,index_of_plane,:]])
				Field_z = np.array([self.field.z[:,index_of_plane,:]])
				print('y-z plane sliced. Location of x = ',self.space.x[index_of_plane])
			if self.field_type =='scalar':
				Field = np.array([self.field[:,index_of_plane,:]])
				print('y-z plane sliced. Location of x = ',self.space.x[index_of_plane])
			
			
		elif plane == 'x-z' or plane == 'z-x':
			index_of_plane = (abs(self.space.y-loc)).argmin()
			x_grid_slice = np.array([self.space.x_grid[index_of_plane,:,:]])
			y_grid_slice= np.array([self.space.y_grid[index_of_plane,:,:]])
			z_grid_slice= np.array([self.space.z_grid[index_of_plane,:,:]])
			if self.field_type == 'vector':
				Field_x = np.array([self.field.x[index_of_plane,:,:]])
				Field_y = np.array([self.field.y[index_of_plane,:,:]])
				Field_z = np.array([self.field.z[index_of_plane,:,:]])
				print('x-z plane sliced. Location of y = ',self.space.y[index_of_plane])
			if self.field_type =='scalar':
				print('x-z plane sliced. Location of y = ',self.space.y[index_of_plane])
				Field = np.array([self.field[index_of_plane,:,:]])
			
			
		else:
			sys.exit('x-y, y-z or z-x plane must be defined to get 2D plane from 3D data. Abort...!!!')
		
		# space_slice = vf.entities.space(grid=True,x_grid=x_grid_slice,y_grid=y_grid_slice,z_grid=z_grid_slice)
		# field_slice = vf.entities.vector(Field_x,Field_y,Field_z)
		
		
		if self.field_type == 'vector':
			field_slice = vector(Field_x,Field_y,Field_z)
		if self.field_type == 'scalar':
			field_slice = Field
			
			
		space_slice = space(grid=True,x_grid=x_grid_slice,y_grid=y_grid_slice,z_grid=z_grid_slice)
		
		# print(x_grid_slice)
		# print(y_grid_slice)
		# print(z_grid_slice)
		# field_slice = None
		# space_slice = None
		
		return field_slice, space_slice


	def return_field_on_line(self,along,x0=0,y0=0,z0=0):
		
		
		
		if along == 'x' or along == 'X':
			# index_of_x = (abs(space.x-x0)).argmin()
			index_of_y = (abs(self.space.y-y0)).argmin()
			index_of_z = (abs(self.space.z-z0)).argmin()
			# index_of_plane = (abs(self.space.z-loc)).argmin()
			x_line = np.array(self.space.x_grid[index_of_y,:,index_of_z])
			y_pt =  np.array(self.space.y[index_of_y])
			z_pt =  np.array(self.space.z[index_of_z])
			
			if self.field_type == 'vector':
				Field_x = np.array(self.field.x[index_of_y,:,index_of_z])
				Field_y = np.array(self.field.y[index_of_y,:,index_of_z])
				Field_z = np.array(self.field.z[index_of_y,:,index_of_z])
				print('Line along x extracted at the location of (y0,z0) = ',(y_pt,z_pt))
				
			if self.field_type =='scalar':
				Field = np.arrary(self.field[index_of_y,:,index_of_z])
				print('Line along x extracted at the location of (y0,z0) = ',(y_pt,z_pt))
			# print(x_line,y_pt,z_pt)
			line_space = space(x=x_line,y=[y_pt],z=[z_pt]) 
			
		elif along == 'y' or along == 'Y':
			index_of_x = (abs(self.space.x-x0)).argmin()
			# index_of_y = (abs(space.y-y0)).argmin()
			index_of_z = (abs(self.space.z-z0)).argmin()
			# index_of_plane = (abs(self.space.z-loc)).argmin()
			# x_line = np.array([self.space.x_grid[index_of_y,:,index_of_z]])
			x_pt =   np.array(self.space.x[index_of_x])
			y_line = np.array(self.space.y_grid[:,index_of_x,index_of_z])
			z_pt =  np.array(self.space.z[index_of_z])
			
			if self.field_type == 'vector':
				Field_x = np.array(self.field.x[:,index_of_x,index_of_z])
				Field_y = np.array(self.field.y[:,index_of_x,index_of_z])
				Field_z = np.array(self.field.z[:,index_of_x,index_of_z])
				print('Line along y extracted at the location of (x0,z0) = ',(x_pt,z_pt))
				
			if self.field_type =='scalar':
				Field = np.arrary([self.field[index_of_y,:,index_of_z]])
				print('Line along y extracted at the location of (x0,z0) = ',(x_pt,z_pt))
			
			line_space = space(x=[x_pt],y=y_line,z=[z_pt]) 
			
		elif along == 'z' or along == 'Z':
			index_of_x = (abs(self.space.x-x0)).argmin()
			index_of_y = (abs(self.space.y-y0)).argmin()
			# index_of_z = (abs(space.z-z0)).argmin()
			# index_of_plane = (abs(self.space.z-loc)).argmin()
			# x_line = np.array([self.space.x_grid[index_of_y,:,index_of_z]])
			x_pt =  np.array(self.space.x[index_of_x])
			# y_line = np.array([self.space.y_grid[:,index_of_x,index_of_z]])
			y_pt =   np.array(self.space.y[index_of_y])
			# z_pt= self.space.z[index_of_z]
			z_line = np.array(self.space.z_grid[index_of_y,index_of_x,:])
			
			if self.field_type == 'vector':
				Field_x = np.array(self.field.x[index_of_y,index_of_x,:])
				Field_y = np.array(self.field.y[index_of_y,index_of_x,:])
				Field_z = np.array(self.field.z[index_of_y,index_of_x,:])
				print('Line along z extracted at the location of (x0,y0) = ',(x_pt,y_pt))
				
			if self.field_type =='scalar':
				Field = np.arrary(self.field[index_of_y,index_of_x,:])
				print('Line along y extracted at the location of (x0,y0) = ',(x_pt,y_pt))
			
			line_space = space(x=[x_pt],y=[y_pt],z=z_line) 
			
		else:
			sys.exit('x-y, y-z or z-x plane must be defined to get 2D plane from 3D data. Abort...!!!')
		
		# space_slice = vf.entities.space(grid=True,x_grid=x_grid_slice,y_grid=y_grid_slice,z_grid=z_grid_slice)
		# field_slice = vf.entities.vector(Field_x,Field_y,Field_z)
		field_slice = vector(Field_x,Field_y,Field_z)
		# space_slice = space(x=x_grid_slice,y_grid=y_grid_slice,z_grid=z_grid_slice)
		
		# print(x_grid_slice)
		# print(y_grid_slice)
		# print(z_grid_slice)
		# field_slice = None
		# space_slice = None
		
		return field_slice, line_space
		
	def magnitude(self):
		return field(self.field.magnitude(),self.space,text_tag = 'mag('+self.text_tag+')')
	
	
	def normalize(self):
		""" Normalize the vector field with the maxmimum magnitude over entire space."""
		text_tag = self.text_tag
		if self.field_type == 'scalar':
			print('Normalizing the scalar field in',self.text_tag)
			F_max = max(np.abs(self.field))
		if self.field_type == 'vector':
			print('Normalizing the vector field in',self.text_tag)
			F_max = np.abs(self.field.magnitude()).max()
		Field_norm = self/F_max
		Field_norm.text_tag = 'normalized('+text_tag+')'
		return Field_norm

	def normalize_pointwise_by(self,scalar_field):
		'''Normalize i.e. divide the Field values point-wise with the values contained in scalar_field. 'scalar_field should either of a field of type scalar, or ndarray matching the dimensions of '''
		
		if isinstance(scalar_field,field):
			if scalar_field.field_type == 'vector':
				sys.exit('Semantic error: Abort...!!! The field with which you want point-wise normalization must be scalar field.')
			if scalar_field.field_type == 'scalar':
				norm_factor = scalar_field.field
				text_norm = scalar_field.text_tag
		else:
			norm_factor = scalar_field
			text_norm = 'ndarray'
		
		if self.field_type =='scalar':
			Field_norm = field(self.field/norm_factor,self.space,text_tag = 'Ptwise-norm('+self.text_tag+') by '+text_norm)
		elif self.field_type == 'vector':
			Field_norm_vec_x = self.field.x/norm_factor 
			Field_norm_vec_y = self.field.y/norm_factor 
			Field_norm_vec_z = self.field.z/norm_factor 
			
			Field_norm_vec = vector(Field_norm_vec_x,Field_norm_vec_y,Field_norm_vec_z)
			
			Field_norm = field(Field_norm_vec,self.space,text_tag = 'Ptwise-norm('+self.text_tag+') by '+text_norm)
			
		return Field_norm



	def TH_at_t(self,omega,t):
		'''Return the field after harmonically evolving for 't' time with 'omega' frequency'''
		
		if self.field_type == 'vector':
			Fx = self.field.x*np.exp(1j*omega*t)
			Fy = self.field.y*np.exp(1j*omega*t)
			Fz = self.field.z*np.exp(1j*omega*t)

			F_vec_t = vector(Fx,Fy,Fz)

			return field(F_vec_t,self.space,text_tag=self.text_tag+'*exp(j '+str(omega)+'*'+str(t)+')')
		if self.field_type == 'scalar':
			F_scalar_t = self.field*np.exp(1j*omega*t)
			return field(F_scalar_t,self.space,text_tag=self.text_tag+'*exp(j '+str(omega)+'*'+str(t)+')')




	def __add__(self,other):
		'''Returns the addition of the field type with other'''
			
		if isinstance(other,field):
			return field(self.field+other.field,self.space,text_tag=self.text_tag+'+'+other.text_tag)
		elif isinstance(other,float) or isinstance(other,int) or isinstance(other,complex):
			
			return field(self.field+other,self.space,text_tag=self.text_tag+'+'+str(other))
			
		else:
			sys.exit('Semantic error: Both objects must be fields of same type or one should be a scalar value. Abort...!!!')
			return None

	def __sub__(self,other):
		'''Returns the vector subtraction of self with other'''
		if isinstance(other,field):
			return field(self.field-other.field,self.space,text_tag=self.text_tag+'-'+other.text_tag)
			
		elif isinstance(other,float) or isinstance(other,int) or isinstance(other,complex):
			
			return field(self.field-other,self.space,text_tag=self.text_tag+'-'+str(other))
			
			
		else:
			sys.exit('Semantic error: Both objects must be vectors. Abort...!!!')
			return None

	def __mul__(self,other):
		if isinstance(other,field):
			return field(self.field*other.field,self.space,text_tag=self.text_tag+'*'+other.text_tag)
		elif isinstance(other,float) or isinstance(other,int) or isinstance(other,complex):
			return field(self.field*other,self.space,text_tag=self.text_tag+'*'+str(other))
		else:
			sys.exit('Semantic error: Either both objects must be vectors, or one should be scalar. Abort...!!!')
			return None

	def __rmul__(self,other):
		return self.__mul__(other)

	def __truediv__(self,other):
		if isinstance(other,float) or isinstance(other,int):
			return field(self.field/other,self.space,text_tag=self.text_tag+'/'+str(other))
		else:
			sys.exit('Semantic error: You can only divide field by a float or int. Abort...!!!')
			return None

	def __xor__(self,other):
		'''Overloads '^' operator to perform vector cross product'''
		if isinstance(other,field):
			return field(self.field^other.field,self.space,text_tag=self.text_tag+'X'+other.text_tag)
		else:
			sys.exit('Semantic error: Both objects must be field. Abort...!!!')
			return None

	def __neg__(self):
		return field(-self.field,self.space,text_tag='-'+self.text_tag)
		
	'''plot functions follow'''
	
	def plot_quiver2d(self,plane=None,loc=0,ax=None,Fig=None,color=True,cmap='jet',text_tag=None):
		
		if text_tag == None:
			text_tag = self.text_tag
		
		print('Plotting 2D quiver for: '+self.text_tag)
		ax, Fig = plot.quiver2d(self.space,self.field,plane=plane,loc=loc,ax=ax,Fig=Fig,color=color,cmap=cmap,text_tag=text_tag)
		return ax, Fig
		
	def plot_streamplot(self,plane=None,loc=0,ax=None,Fig=None,color=True,cmap='jet',text_tag = None):
		
		if text_tag == None:
			text_tag = self.text_tag
		
		print('Plotting 2D streamplot for: '+text_tag)
		ax, Fig = plot.streamplot(self.space,self.field,plane=plane,loc=loc,ax=ax,Fig=Fig,color=color,cmap=cmap,text_tag=text_tag)
		return ax, Fig
		
	def plot_contourf(self,plane=None,loc=0,ax=None,Fig=None,color=True,cmap='jet',text_tag=None,color_axis=None,vmax=None,vmin=None,flag_colorbar=True):
		
		
		if text_tag == None:
			text_tag = self.text_tag
		
		
		if self.field_type == 'scalar':
			
			print('Plotting 2D field plot for: '+self.text_tag)
			ax, Fig = plot.contourf(self.space,self.field,plane=plane,loc=loc,ax=ax,Fig=Fig,color=color,cmap=cmap,text_tag=text_tag,color_axis=color_axis,vmax=vmax,vmin=vmin,flag_colorbar=flag_colorbar)
			
		if self.field_type == 'vector':
			print('Plotting 2D magnitude plot of: '+self.text_tag)
			ax, Fig = plot.contourf(self.space,self.field.magnitude(),plane=plane,loc=loc,ax=ax,Fig=Fig,color=color,cmap=cmap,text_tag=text_tag,color_axis=color_axis,vmax=vmax,vmin=vmin,flag_colorbar=flag_colorbar)

		return ax, Fig
		
		
	def plot_1d_plot(self,along,x0=0,y0=0,z0=0,ax=None,Fig=None,color=True,cmap='jet',text_tag=None,color_axis=None,vmax=None,vmin=None,flag_colorbar=True):
		
		
		if text_tag == None:
			text_tag = self.text_tag
		
		
		if self.field_type == 'scalar':
			
			print('Plotting 2D field plot for: '+self.text_tag)
			ax, Fig = plot.contourf(self.space,self.field,plane=plane,loc=loc,ax=ax,Fig=Fig,color=color,cmap=cmap,text_tag=text_tag,color_axis=color_axis,vmax=vmax,vmin=vmin,flag_colorbar=flag_colorbar)
			
		if self.field_type == 'vector':
			print('Plotting 2D magnitude plot of: '+self.text_tag)
			ax, Fig = plot.contourf(self.space,self.field.magnitude(),plane=plane,loc=loc,ax=ax,Fig=Fig,color=color,cmap=cmap,text_tag=text_tag,color_axis=color_axis,vmax=vmax,vmin=vmin,flag_colorbar=flag_colorbar)

		return ax, Fig
		
		
	def plot_quiver3d(self,Fig=None,arrow_density = 0.7,text_tag=None,scale_mode='none',colormap='jet'):
		
		if text_tag == None:
			text_tag = self.text_tag
		
					
			
				
		print('Plotting 3D quiver plot of: '+text_tag)
		handle_s, Fig = plot.quiver3d(self.space,self.field,arrow_density=arrow_density,text_tag=text_tag,scale_mode=scale_mode,Fig=Fig,colormap=colormap)
		
		return handle_s, Fig
		
	def plot_volume_slice(self,Fig=None,colormap='jet',text_tag=None,arrow_density=0.7,normal_plot=False):
		if text_tag ==  None:
			text_tag = self.text_tag
		
		if self.field_type == 'scalar':
			Fig = plot.volume_slice_scalar(self.field,Fig=Fig,colormap=colormap,text_tag=text_tag)
		
		if self.field_type == 'vector':
			Fig = plot.volume_slice_vector(self.field,Fig=Fig,colormap=colormap,text_tag=text_tag,arrow_density=arrow_density,normal_plot=normal_plot)
		return Fig
	
	def plot_contour3d(self,Fig=None,colormap='jet',text_tag=None,contours=None):
		if text_tag == None:
			text_tag = self.text_tag
			
		if self.field_type == 'scalar':
			Fig = plot.contour3d(self.space,self.field,Fig=Fig,text_tag=text_tag,colormap='jet',contours=contours)
		if self.field_type == 'vector':
			Fig = plot.contour3d(self.space,self.field.magnitude(),Fig=Fig,text_tag=text_tag,colormap='jet',contours=contours)
			
		return Fig
			


class source(object):
	def __init__(self,source,r0,text_tag=None,source_type=None):
		"""Define source"""
		
		if text_tag == None:
			self.text_tag = 'text tag'
		else:
			self.text_tag = text_tag
		
		if not isinstance(r0,vector):
			sys.exit('Position has to be an object of vector class. Abort !!!')
		
		if not source.shape == r0.shape:
			sys.exit('The shape of \'source\'  and position (r0) must be the same. Abort !!!')
				
				
		if isinstance(source,vector):
			self.source_type = 'vector'
			self.source = source
			self.r0 = r0
			print('Vector source: ' + self.text_tag + ' defined.')
		else:
			self.field_type = 'scalar'
			self.source = source
			self.r0 = r0
			print('Scalar field: ' + self.text_tag + ' defined.')
		return
		
		
	def shift_x(self,shift):
		self.r0 = vector(self.r0.x+shift,self.r0.y,self.r0.z)
		return self
	def shift_y(self,shift):
		self.r0 = vector(self.r0.x,self.r0.y+shift,self.r0.z)
		return self
	def shift_z(self,shift):
		self.r0 = vector(self.r0.x,self.r0.y,self.r0.z+shift)
		return self
	def shift_r(self,r_shift):
		self.r0 = vector(self.r0.x+r_shift.x,self.r0.y+r_shift.y,self.r0.z+r_shift.z)
		return self



def zero_field_vector_like(space):
	if isinstance(space,type(space)):
		field_zero = field(zero_vector_like(space),space)
		print('control here')
	else: 
		sys.exit('Zero field can be defined only if the argument is an object of type space. Abort !!!')
	
	return field_zero

def zero_field_scalar_like(space):
	if isinstance(space,type(space)):
		field_zero = field(np.zeros_like(space.x),space)
	else: 
		sys.exit('Zero field can be defined only if the argument is an object of type space. Abort !!!')
	return field_zero

def zero_vector_like(space):
	if isinstance(space,type(space)):
		vector_zero = vector(np.zeros_like(space.x_grid),np.zeros_like(space.y_grid),np.zeros_like(space.z_grid))
	else:
		vector_zero = vector(np.zeros_like(space),np.zeros_like(space),np.zeros_like(space))
	
	return vector_zero
		
		
