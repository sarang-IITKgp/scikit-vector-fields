import numpy as np
from .entities import vector

def gradient(scalar_field,space):
    """Gradient function implemented in the library. 
    Input:
    scalar_field: scalar 2D or 3D numpy array as input.
    space: An object of Class space of the entities module.'space' can be 2D or 3D. 
    The dimensions and shape of scalar_field and space.x, space.y & space.z, should be equal
    Returns:
    An object of Class vector of the entities module.
    numpy gradient is used to compute the gradient."""
    if space.dim == 2:
        if space.plane == 'x-y':
            [dV_y, dV_x ] = np.gradient(scalar_field)

            [dxy_grid, dx_grid] = np.gradient(space.x_grid) 

            [dy_grid, dyx_grid] = np.gradient(space.y_grid) 

            dV_by_dx = dV_x/dx_grid
            dV_by_dy = dV_y/dy_grid 
            dV_by_dz = np.zeros_like(dV_by_dx) 
            
            
        if space.plane == 'y-z':
            [dV_z, dV_y ] = np.gradient(scalar_field)

            [dyz_grid, dy_grid] = np.gradient(space.y_grid) 

            [dz_grid, dzy_grid] = np.gradient(space.z_grid) 

            dV_by_dy = dV_y/dy_grid
            dV_by_dz = dV_z/dz_grid 
            dV_by_dx = np.zeros_like(dV_by_dy)
        
        if space.plane == 'x-z':
            [dV_z, dV_x ] = np.gradient(scalar_field)

            [dxz_grid, dx_grid] = np.gradient(space.x_grid) 

            [dz_grid, dzx_grid] = np.gradient(space.z_grid) 

            dV_by_dx = dV_x/dx_grid
            dV_by_dz = dV_z/dz_grid 
            dV_by_dy = np.zeros_like(dV_by_dx)
            
            
    if space.dim == 3:
            [dV_y, dV_x, dV_z] = np.gradient(scalar_field)

            [dxy_grid, dx_grid, dxz_grid] = np.gradient(space.x_grid) 
            [dy_grid, dyx_grid, dyz_grid] = np.gradient(space.y_grid) 
            [dzy_grid, dyx_grid, dz_grid] = np.gradient(space.z_grid) 

            dV_by_dx = dV_x/dx_grid
            dV_by_dy = dV_y/dy_grid 
            dV_by_dz = dV_z/dz_grid 
            
         
    return vector(dV_by_dx,dV_by_dy,dV_by_dz)


def partial_derivative(scalar_field,space):
    
    if space.dim == 2:
        
        if space.plane == 'x-y':
            [dV_y, dV_x ] = np.gradient(scalar_field)

            [dxy_grid, dx_grid] = np.gradient(space.x_grid) 

            [dy_grid, dyx_grid] = np.gradient(space.y_grid) 

            partial_x = dV_x/dx_grid
            partial_y = dV_y/dy_grid 
            partial_z = np.zeros_like(partial_x) 
            
            
        if space.plane == 'y-z':
            [dV_z, dV_y ] = np.gradient(scalar_field)

            [dyz_grid, dy_grid] = np.gradient(space.y_grid) 

            [dz_grid, dzy_grid] = np.gradient(space.z_grid) 

            partial_y = dV_y/dy_grid
            partial_z = dV_z/dz_grid 
            partial_x = np.zeros_like(partial_y)
        
        if space.plane == 'x-z':
            [dV_z, dV_x ] = np.gradient(scalar_field)

            [dxz_grid, dx_grid] = np.gradient(space.x_grid) 

            [dz_grid, dzx_grid] = np.gradient(space.z_grid) 

            partial_x = dV_x/dx_grid
            partial_z = dV_z/dz_grid 
            partial_y = np.zeros_like(partial_x)
            
                
    if space.dim == 3:
            [dV_y, dV_x, dV_z] = np.gradient(scalar_field)

            [dxy_grid, dx_grid, dxz_grid] = np.gradient(space.x_grid) 
            [dy_grid, dyx_grid, dyz_grid] = np.gradient(space.y_grid) 
            [dzy_grid, dyx_grid, dz_grid] = np.gradient(space.z_grid) 

            partial_x = dV_x/dx_grid
            partial_y = dV_y/dy_grid 
            partial_z = dV_z/dz_grid 
    
        
            
    return partial_x, partial_y, partial_z
    


def divergence(field_vector,space):
    """Field function must be an object of  vector Class. Dimensions must be matching with that of space.
    Returns a scalar variable."""
    
    
    
    partial_x, dummy, dummy = partial_derivative(field_vector.x,space)
    dummy, partial_y, dummy = partial_derivative(field_vector.y,space)
    dummy, dummy, partial_z = partial_derivative(field_vector.z,space)
    
    return partial_x+partial_y+partial_z
    
def curl(field_vector,space):
    """Field function must be an object of vector. Dimensions must be matching with that of space.
    Returns a field of object type vector."""
    
    A_x = field_vector.x
    A_y = field_vector.y
    A_z = field_vector.z
    
    
    
    dAx_by_dx, dAx_by_dy, dAx_by_dz = partial_derivative(A_x,space)
    dAy_by_dx, dAy_by_dy, dAy_by_dz = partial_derivative(A_y,space)
    dAz_by_dx, dAz_by_dy, dAz_by_dz = partial_derivative(A_z,space)
    
    curl_A_x = dAz_by_dy - dAy_by_dz
    curl_A_y = dAx_by_dz - dAz_by_dx
    curl_A_z = dAy_by_dx - dAx_by_dy
    
    return vector(curl_A_x,curl_A_y,curl_A_z)
    
    
    
    
