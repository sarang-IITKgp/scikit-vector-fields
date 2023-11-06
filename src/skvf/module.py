import numpy as np



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
		
		
	def __xor__(self,other):
		'''Overloads '^' operator to perform vector cross product'''
		return self.cross(other)
	def __neg__(self):
		return vector(-self.x,-self.y,-self.z)
	
class space():
	def __init__(self,x=None,y=None,z=None,grid=False,x_grid=None,y_grid=None,z_grid=None):
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
		
		self.R = np.sqrt(self.x_grid**2 + self.y_grid**2 + self.z_grid**2)
		print('This is space')
		
	def vec(self):
		return vector(self.x_grid,self.y_grid,self.z_grid)
		
class field():
	def __init__(self,vector,space):
		"""Check if vector and space are of the same dimensions and size"""
		print('This is field')
		
		
