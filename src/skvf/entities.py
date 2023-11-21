import numpy as np
# from . import 
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

   # def print(self):
	   # print(self.x,self.y,self.z)
	   # return
    
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
    
		self.R = np.sqrt(self.x_grid**2 + self.y_grid**2 + self.z_grid**2)
		print('Space is defined')
		
	def vec(self):
		return vector(self.x_grid,self.y_grid,self.z_grid)
		

class field():
	def __init__(self,field,space,text_tag='text tag',field_type=None):
		"""Check if vector and space are of the same dimensions and size"""
		print('Defining field')
		self.space = space
		self.text_tag = text_tag
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
		# print('computing divergence')
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
			curl_field = gradient(self.field,self.space)
		return field(curl_field,self.space,text_tag='grad('+self.text_tag+')')

	def gradient(self):
		return self.grad()
		
	def conjugate(self):
		'''Take complex conjugates of the vector elements'''
		# x = np.conjugate(self.x)
		# y = np.conjugate(self.y)
		# z = np.conjugate(self.z)
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
			return field(self.field.imag(),self.space,text_tag='Re('+self.text_tag+')')
		if self.field_type == 'scalar':
			return field(np.imag(self.field),self.space,text_tag='Re('+self.text_tag+')')
			



	def __add__(self,other):
		'''Returns the addition of the field type with other'''
			
		if isinstance(other,field):
			return field(self.field+other.field,self.space,text_tag=self.text_tag+'+'+other.text_tag)
		elif isinstance(other,float) or isinstance(other,int) or isinstance(other,complex):
			
			return field(self.field+other,self.space,text_tag=self.text_tag+'+'+str(other))
			
		else:
			sys.exit('Semantic error: Both objects must be vectors. Abort...!!!')
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
		# return self.dot(other)

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
		
		
	def plot_quiver3d(self,Fig=None,arrow_density = 0.7,text_tag=None,scale_mode='none',colormap='jet'):
		
		if text_tag == None:
			text_tag = self.text_tag
		
					
			
				
		print('Plotting 3D quiver plot of: '+text_tag)
		Fig = plot.quiver3d(self.space,self.field,arrow_density=arrow_density,text_tag=text_tag,scale_mode=scale_mode,Fig=Fig,colormap=colormap)
		
		return Fig
		
	def plot_volume_slice(self,Fig=None,colormap='jet',text_tag=None,arrow_density=0.7):
		if text_tag ==  None:
			text_tag = self.text_tag
		
		if self.field_type == 'scalar':
			Fig = plot.volume_slice_scalar(self.field,Fig=Fig,colormap='jet',text_tag=text_tag)
		
		if self.field_type == 'vector':
			Fig = plot.volume_slice_vector(self.field,Fig=Fig,colormap='jet',text_tag=text_tag,arrow_density=arrow_density)
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
		# print('control here')
		vector_zero = vector(np.zeros_like(space.x_grid),np.zeros_like(space.y_grid),np.zeros_like(space.z_grid))
	else:
		vector_zero = vector(np.zeros_like(space),np.zeros_like(space),np.zeros_like(space))
	
	return vector_zero
		
		
