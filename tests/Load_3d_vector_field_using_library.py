""" Code to visualize 3D scalar and vector fields"""



################################################################################
######################## Import Libraries ######################################


import numpy as np # For numerical function

import matplotlib.pyplot as plt # For 2D plot
import matplotlib as mpl


import skvf as vf

import mayavi.mlab as mlab

# import sys as sys

# from os.path import dirname, realpath
# import sys


# import pandas as pd
# import re as re
#########################################



# E_field_slot = load_HFSS_field_file('Near E Table_WithoutSlot_21X21X21.csv',text_tag='E-WTS)
E_field_slot = vf.data.load_HFSS_field_file('Near E Table_WithoutSlot_21X21X21.csv',text_tag='E-WTS')




# H_field_slot = load_HFSS_field_file('Near H Table_TaperedSlot_21X21X21.csv',text_tag='H-WTS')
# H_field_slot = load_HFSS_field_file('Near H Table_WithoutSlot_21X21X21.csv',text_tag='H-WTS')
H_field_slot = vf.data.load_HFSS_field_file('Near H Table_WithoutSlot_21X21X21.csv',text_tag='H-WTS')



H_field_t = H_field_slot.TH_at_t(H_field_slot.TH_omega,1*np.pi/H_field_slot.TH_omega)


Pv_field_slot = E_field_slot^H_field_slot.conjugate()



S_h_vec_field = (H_field_slot^H_field_slot.conjugate()).imag()

S0_h = np.abs(H_field_slot.field.x)**2 + np.abs(H_field_slot.field.y)**2

S0_h_field = vf.entities.field(S0_h,H_field_slot.space)

S3_h_pointwise_norm = S_h_vec_field.normalize_pointwise_by(S0_h_field)




z_loc = 0.2e-3

fig1 = plt.figure('Some field')
# ax1_f1 = fig1.add_subplot(311)
ax1_f1 = fig1.add_subplot(311)
ax2_f1 = fig1.add_subplot(312)
ax3_f1 = fig1.add_subplot(313)

E_field_slot.real().plot_contourf(plane='x-y',loc=z_loc,ax=ax1_f1)
H_field_slot.real().plot_quiver2d(plane='x-y',loc=z_loc,ax=ax2_f1)

S_h_vec_field.plot_contourf(plane='x-y',loc=z_loc,ax=ax3_f1)


E_field_slot.real().plot_quiver3d()

H_field_slot.real().plot_quiver3d()
H_field_t.real().plot_quiver3d()

Pv_field_slot.real().plot_quiver3d()



plt.show()
