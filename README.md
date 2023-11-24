# scikit-vector-fields

An open source Python package to perform basics vector field computations. The library is designed primarily for electromagnetic field computations and visualization. However many features can be used for other vector fields in general. 

The first version of this package published on PyPI is intended to be used as an aid in teaching Electromagnetic Engineering course to second year undergraduates at IIT Kharagpur. _*scikit-vector-fields*_ enables easy computation of divergence, curl and gradient of vector and scalar fields. 2D (based on _*matplotlib*_) and 3D (based on _*mayavi*_) visualization of the fields is also supported by the project. The idea is that this package should allow users, who are not masters of coding, to compute and visualize electromagnetic wave phenomena. A typical code should closely match with the mathematical equations on vector fields that we derive and study. 

This package does not intend to replace fullwave EM simulators, which also have rich field visualization tools. Neither this package, in the current version, can handle irregular geometries, which are better treated by computational EM tools. In typical commercially available fullwave compuational packages, the mathematical equations are hidden from the users. This is a good thing for many advanced design applications, where an EM engineer can focus on the design and let the software take care of the equations. On the contrary, the hidden nature of underlying equations is not very good at a learning stage. For students, it becomes important that they are able to understand the physical meaning of equations. For exmaple, they should be able to visualize what happens when they take curl of a vector field. This package is developed in hope that the pen-and-paper derivations and expressions can be easily liked to field visualization. 





Consists of the the following three modules.

### Module: Entities

This module consists of the following Python classes.

#### Vector
This is a vector object, defined to behave like a physical 3D vector. 

It has three attributes, 'x', 'y' & 'z'. These three can be int, float, complex numbers or _numpy_ n-dimentional arrays.

The operators are overloaded perform vector addition, subtraction, dot product (multiplication) and cross product. '^' operator is overloaded to perform cross-product. 

#### Space
This is a space coordinate object, which creates a 2D or 3D grid (based on _numpy.meshgrid_). The purpose of this object is to serve as the space variable in defining the fields, and in numerical computation of curl, divergence and gradient.  


#### Field
This is a field object. It can either represent a scalar field, or a vector field. Field object has two attributes, 'field' and 'space'. The dimension and shape of field and space must match. For scalar field, the 'field' attribute is a _numpy_ array. For vector field, the 'field' attribute is a vector object.

You can directly compute divergence and curl of a vector field by using the method _field.div()_ and _field.curl()_. 

You can directly visualize the field in 2D and 3D using several plotting methods. 


### Module: Operations

This module contain functions to compute (1) partial derivative of scalar quantity, (2) gradient of vector quantity, (3) curl of vector quantity, and (4) divergence of scalar quantity. 

It takes 'field' and 'space' as input and returns vector of scalar. These function are called for computation as methods for _field_ objects. Although the recommended way of computing curl, divergence and gradient is using methods of the _field_ object, the functions in this module are also available to the user. 


### Module: Plot.

This module contains functions to plot the fields. These functions are just to wrap around the standard _matplotlib_ and _mayavi_ plotting functions, to be compatible with the _field_ object defined in this package. Functions here aim to generate good quality plots for field visualization, with minimum level of programming skill of the user. 


------------------

## Usage Examples:


 



 
