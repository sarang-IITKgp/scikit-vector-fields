# scikit-vector-fields

An open source Python package to perform basics vector field computations. The library is designed primarily for electromagnetic field computations and visualization. However many features can be used for other vector fields in general. 

The first version of this package published on PyPI is intended to be used as an aid in teaching Electromagnetic Engineering course to second year undergraduates at IIT Kharagpur. _*scikit-vector-fields*_ enables easy computation of divergence, curl and gradient of vector and scalar fields. 2D (based on _*matplotlib*_) and 3D (based on _*mayavi*_) visualization of the fields is also supported by the project. The idea is that this package should allow users, who are not masters of coding, to compute and visualize electromagnetic wave phenomena. A typical Pyhton code using this package closely matches with the mathematical equations on vector fields that we derive. 



<figure>
  <figcaption>Magnetic Field of two Hertzian dipole antenna.</figcaption>
  <img src="/tests/images/Hertz_array_H_field.png" alt="">
</figure>

--------
<figure>
  <figcaption>Radiation from two Hertzian dipoles. Radiation pattern of the antenna array can be seen in the Poynting vector plot.</figcaption>
  <img src="/tests/images/E,H,P-field_2D_plot.png" alt="">
</figure>

----------
<figure>
  <figcaption>Magnetic field of a current carrying coil.</figcaption>
  <img src="/tests/images/Magnetic_field_single_coil.gif" alt="">
</figure>

-----------
<figure>
  <figcaption>Magnetic field due to two current carrying coils, with currents in opposite direction.</figcaption>
  <img src="/tests/images/Magnetic_field_two_coils.gif" alt="">
</figure>

-----------



This package does not intend to replace fullwave EM simulators, which also have rich field visualization tools. Neither this package, in the current version, can handle irregular geometries, which are better treated by computational EM tools. In typical commercially available fullwave compuational packages, the mathematical equations are hidden from the users. This is a good thing for many advanced design applications, where an EM engineer can focus on the design and let the software take care of the equations. On the contrary, the hidden nature of underlying equations is not very good at a learning stage. For students, it becomes important that they are able to understand the physical meaning of equations. For exmaple, they should be able to visualize what happens when they take curl of a vector field. This package is developed in hope that the pen-and-paper derivations and expressions can be easily liked to field visualization. 





Consists of the the following three modules.

### 1) Module: Entities

This module consists of the following Python classes.

#### vector
This is a vector object, defined to behave like a physical 3D vector. 

It has three attributes, 'x', 'y' & 'z'. These three can be int, float, complex numbers or _numpy_ n-dimentional arrays.

The operators are overloaded perform vector addition, subtraction, dot product (multiplication) and cross product. '^' operator is overloaded to perform cross-product. 

#### space
This is a space coordinate object, which creates a 2D or 3D grid (based on _numpy.meshgrid_). The purpose of this object is to serve as the space variable in defining the fields, and in numerical computation of curl, divergence and gradient.  


#### field
This is a field object. It can either represent a scalar field, or a vector field. Field object has two attributes, 'field' and 'space'. The dimension and shape of field and space must match. For scalar field, the 'field' attribute is a _numpy_ array. For vector field, the 'field' attribute is a vector object.

You can directly compute divergence and curl of a vector field by using the method _field.div()_ and _field.curl()_. 

You can directly visualize the field in 2D and 3D using several plotting methods. 

#### source
This is a source object, which contains the vector or scalar magnitude of a source and its position. 


### 2) Module: Operations

This module contain functions to compute (1) partial derivative of scalar quantity, (2) gradient of vector quantity, (3) curl of vector quantity, and (4) divergence of scalar quantity. 

It takes 'field' and 'space' as input and returns vector of scalar. These function are called for computation as methods for _field_ objects. Although the recommended way of computing curl, divergence and gradient is using methods of the _field_ object, the functions in this module are also available to the user. 


### 3) Module: Plot.

This module contains functions to plot the fields. These functions are just to wrap around the standard _matplotlib_ and _mayavi_ plotting functions, to be compatible with the _field_ object defined in this package. Functions here aim to generate good quality plots for field visualization, with minimum level of programming skill of the user. 


------------------

## Installation
`pip install scikit-vector-fields`

### Dependencies
1. numpy
2. matplotlib
3. mayavi
4. PyQt5

If these fail to install with the installation of scikit-vector-fields, please install them manually using the following commands.

```
pip install numpy
pip install matplotlib
pip install mayavi
pip install PyQt5
```


## Importing the library in Python. 
`import skvf as vf`

## Examples:

### Electric field of dipoles.

```
import numpy as np
import skvf as vf


import matplotlib.pyplot as plt



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




##################### End function definitions #########################
########################################################################


'''Create space'''
x = np.linspace(-5,5,50)
y = np.linspace(-5,5,50)
z = np.linspace(-5,5,50)



space1 = vf.entities.space(x=x,y=y,z=z) # Creating 3D space. You can also create 2D space by giving only two variables. 

R_vec = space1.vec() # Returns vector for each point in the defined space. 


'''The first argument is the magnitude of the charge. Second argument is
the defined space. The third argument is the position of the charge.'''
V1 = potential_of_charge(-1,space = space1,r0 = vf.entities.vector(0.5,0,0))
V2 = potential_of_charge(1,space = space1,r0 = vf.entities.vector(-0.5,0,0))

V = V1+V2

V_field1 = vf.entities.field(V1,space1,text_tag='V1') # Create field by mapping scalar and space.
V_field2 = vf.entities.field(V2,space1,text_tag='V2') 



V_field = V_field1+V_field2 # Add scalar fields. 

E_field = -V_field.grad() # Compute Electric field by taking gradient of electric potential. 
rho_field = E_field.div() # Compute charge density by taking divergence of electric field. 


ax, Fig = rho_field.plot_contourf(plane='x-y',loc=0) # Plot the charge density. 
ax, Fig = E_field.plot_streamplot(plane='x-y',loc=0,ax=ax) # Plot the Electric field as streamplot. 
ax, Fig = E_field.plot_quiver2d(plane='x-y',loc=0,ax=ax) #plot the electric field asq quiever plot.

E_field.plot_quiver3d(arrow_density=0.01) # 3D quiver plot of the field using mayavi. 
plt.show()
```
 
### Hertz dipole. 

```
import numpy as np
import skvf as vf
import matplotlib.pyplot as plt



########################################################################
################# Begin function definition ############################

def A_due_to_dI(dI,r0=0,R_vec=None,space=None,omega=0):
	'''Computes and returns the Magnetic vector potential of a current, located at r0'''
	
	if R_vec == None:
		if space ==  None:
			print('At least one of R-vector or space object must be defined')
		else:
			R_vec = space.vec()
	
	
	
	if isinstance(dI,vf.entities.source):
		
		dI_vec = dI.source
		r0 = dI.r0
	else: 
		dI_vec = dI
		r0 = r0
	
	beta = omega/vf.VELOCITY_OF_LIGHT
	lambda0 = 2*np.pi/beta
	
	dl = 0.1*lambda0
	
	R_minus_r0_mag = (R_vec-r0).magnitude()
	
	Ax = vf.MU_0/(4*np.pi*R_minus_r0_mag)*dI_vec.x*dl*np.exp(-1j*beta*R_minus_r0_mag)
	Ay = vf.MU_0/(4*np.pi*R_minus_r0_mag)*dI_vec.y*dl*np.exp(-1j*beta*R_minus_r0_mag)
	Az = vf.MU_0/(4*np.pi*R_minus_r0_mag)*dI_vec.z*dl*np.exp(-1j*beta*R_minus_r0_mag)
	return vf.entities.vector(Ax,Ay,Az)

##################### End function definitions #########################
########################################################################


freq = 1e9
omega = 2*np.pi*freq
c = vf.VELOCITY_OF_LIGHT

beta = omega/c
lambda0 = 2*np.pi/beta


'''Create space'''
x = np.linspace(-3*lambda0,3*lambda0,30)
y = np.linspace(-3*lambda0,3*lambda0,30)
z = np.linspace(-3*lambda0,3*lambda0,30)


space1 = vf.entities.space(x=x,y=y,z=z) # Space defined. 


R_vec = space1.vec() #



r0 = vf.entities.vector(0,0,0) # Position of the point source. 
dI_vec = vf.entities.vector(0,0,1) # Magnitude of the vector point source.


dI = vf.entities.source(dI_vec,r0) # Define source entity. 


A_Hertz = A_due_to_dI(dI,space=space1,omega=omega) # Get Magnetic vector potential due to an infinitesimal current source.
 
A_field = vf.entities.field(A_Hertz,space1,text_tag='$vec{A}$') # Define magnetic vector potential field by mapping the vector field and space. 


H_field = (1/vf.MU_0)*A_field.curl()  # Compute Magnetic field.
E_field = (1/(1j*omega*vf.EPSILON_0))*H_field.curl() # Compute Electric field. 



Pv_field = E_field^H_field.conjugate() # Compute Poynting vector. '^' does the cross-product. 


#### following are the commands for plotting.
E_field.real().plot_volume_slice(colormap='hot')  # Volume slice plot with 3D quiver using Mayavi package. 
H_field.real().plot_volume_slice(colormap='hot')
Pv_field.real().plot_volume_slice(colormap='hot')

fig_E =plt.figure('E-field 2D plot')
ax_E = fig_E.subplots(1,3)

E_field.real().plot_quiver2d(plane='x-y',ax=ax_E[0])
E_field.real().plot_quiver2d(plane='y-z',ax=ax_E[1])
E_field.real().plot_quiver2d(plane='x-z',ax=ax_E[2])


fig_H =plt.figure('H-field 2D plot')
ax_H = fig_H.subplots(1,3)

H_field.real().plot_quiver2d(plane='x-y',ax=ax_H[0])
H_field.real().plot_quiver2d(plane='y-z',ax=ax_H[1])
H_field.real().plot_quiver2d(plane='x-z',ax=ax_H[2])

fig_P =plt.figure('Poynting vector 2D plot')
ax_P = fig_P.subplots(1,3)

Pv_field.real().plot_contourf(plane='x-y',ax=ax_P[0])
Pv_field.real().plot_quiver2d(plane='x-y',ax=ax_P[0])


Pv_field.real().plot_contourf(plane='y-z',ax=ax_P[1])
Pv_field.real().plot_quiver2d(plane='y-z',ax=ax_P[1])

Pv_field.real().plot_contourf(plane='x-z',ax=ax_P[2])
Pv_field.real().plot_quiver2d(plane='x-z',ax=ax_P[2])

plt.show()
```


 
