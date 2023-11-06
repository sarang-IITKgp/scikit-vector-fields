import numpy as np

class vector(object):
    
    def __init__(self,x,y,z):
        ### x, y, z should be arrays of the same size
        self.x = x
        self.y = y
        self.z = z
    
    
    def com_conj(self):
        """ returns complex conjugate of Vector """
        x = np.conjugate(self.x)
        y = np.conjugate(self.y)
        z = np.conjugate(self.z)
        return vector(x,y,z)
    
    def elements(self):
        """ return the elements of the vector to unpack"""
        return self.x, self.y, self.z
    
    def magnitude(self):
        """ return the magnitude of the vector """
        return np.sqrt(self.dot(self.com_conj()))
    
    def real(self):
        return vector(np.real(self.x),np.real(self.y),np.real(self.z))
        
    def imag(self):
        return vector(np.imag(self.x),np.imag(self.y),np.imag(self.z))
    
    
    def dot(self,other):
        """ performs dot product. If both the objects are Vector, returns the inner product
        if one obeject is vector and other scaler, then multiply the vector with the scalar"""
        
        if isinstance(other, vector):
            return self.x*other.x + self.y*other.y + self.z*other.z +0.0j
        elif isinstance(other, int) or isinstance(other, float) or isinstance(other,complex):
            return vector(other*self.x, other*self.y, other*self.z)
    
    def cross(self,other):
        """ Performs the cross (vector) product between two vectors """
        if isinstance(other,vector):
            x = self.y*other.z - self.z*other.y
            y = -1*(self.x*other.z - self.z*other.x)
            z = self.x*other.y - self.y*other.x
            return vector(x,y,z)
        else:
            print( 'Both objects must be of vector class')
            return None
    
    
    def __add__(self, other):
        """ Returns the vector addition of self and other """
        
    
        if isinstance(other,vector):
            x = self.x + other.x
            y = self.y + other.y
            z = self.z + other.z
        return vector(x,y,z)
        
    
    def __sub__(self, other):
        """ Returns the vector addition of self and other """
        
        if isinstance(other,vector):
            x = self.x - other.x
            y = self.y - other.y
            z = self.z - other.z
        return vector(x,y,z)
        
    def __mul__(self, other):
        return self.dot(other)
        
    def __rmul__(self, other):
        return self.dot(other)
        
        
	def __xor__(self,other):
		""" Overloads '^' operator to perform the cross (vector) product between two vectors. """
        if isinstance(other,vector):
            x = self.y*other.z - self.z*other.y
            y = -1*(self.x*other.z - self.z*other.x)
            z = self.x*other.y - self.y*other.x
            return vector(x,y,z)
        else:
            print( 'Both objects must be of vector class')
            return None
