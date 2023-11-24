The two Data types suuported for plot data export by CST are ASCII Text (in .txt file format) and HDF5 format (having .h5 file extension).
The data points in this directory are

For 3D: 
Nx = 15
Ny = 12
Nz = 10

For 2D: 
Nx = 15
Ny = 12
Nz = 1

The Python Script snippet used for the importing the txt file and reshaping it as follows (for a 2D file)

np.seterr(invalid='ignore')  
datae = np.genfromtxt("E:\\Python_files_neeraja\\SIW_Cubedefect_1.7_E21_f1.txt", dtype=None, skip_header=2)  
datae = np.array(datae.tolist())  
x = datae[:, 0]  
x = np.transpose(x)  
x = np.reshape(x, (300, 500))  
z = datae[:, 2]  
z = np.transpose(z)  
z = np.reshape(z, (300, 500))  
ex_re = datae[:, 3]  
ex_im = datae[:, 4]  
ey_re = datae[:, 5]  
ey_im = datae[:, 6]  
ez_re = datae[:, 7]  
ez_im = datae[:, 8]  


