#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 09:41:07 2021

@author: entongsu
"""


from math import pi
import pygmsh
import numpy as np
import random
import scipy
from scipy import linalg
import open3d  as o3d
import imageio
from scipy.spatial.transform import Rotation as R

import copy
def generate_mesh():


    with pygmsh.geo.Geometry() as geom:
        poly = geom.add_polygon(
            [
                [+0.0, +0.5],
                [-0.1, +0.1],
                [-0.5, +0.0],
                [-0.1, -0.1],
                [+0.0, -0.5],
                [+0.1, -0.1],
                [+0.5, +0.0],
                [+0.1, +0.1],
            ],
            mesh_size=0.05,
        )
    
        geom.twist(
            poly,
            translation_axis=[0, 0, 1],
            rotation_axis=[0, 0, 1],
            point_on_axis=[0, 0, 0],
            angle=pi / 3,
        )

        mesh = geom.generate_mesh()
   
    return mesh.points,mesh.cells[0][1],mesh.cells[1][1],mesh.cells[2][1],mesh.cells[3][1]


def build_rest_length(triangles,points):
     num_points=len(points)
     rest_length=np.zeros((num_points,num_points))
     for tri in triangles:
         rest_length[tri[0],tri[1]]=np.linalg.norm(points[tri[0]]-points[tri[1]])
         rest_length[tri[0],tri[2]]=np.linalg.norm(points[tri[0]]-points[tri[2]])
         rest_length[tri[1],tri[2]]=np.linalg.norm(points[tri[1]]-points[tri[2]])
         rest_length[tri[1],tri[0]]=np.linalg.norm(points[tri[1]]-points[tri[0]])
         rest_length[tri[2],tri[0]]=np.linalg.norm(points[tri[2]]-points[tri[0]])
         rest_length[tri[2],tri[1]]=np.linalg.norm(points[tri[2]]-points[tri[1]])
     return rest_length

def get_surface_points(line):
    surface_points=np.unique(line)
    return surface_points

def define_point_properity(points):
    point_properity=np.ones(len(points))
    list=range(1,len(points))
    fixed_points=random.sample(list,int(len(points)/2))
    point_properity[fixed_points]=0
    return point_properity

def get_tetra_volumn(tetra,points):
    tetra_volumn=np.zeros((len(tetra),5))
    index=0
    for tra in tetra:
        
        tetra_volumn[index,0:4]=tra
        p1=points[tra[0]]
        p2=points[tra[1]]
        p3=points[tra[2]]
        p4=points[tra[3]]
        
       
        volumn=triangle_volumn(p1,p2,p3,p4)
        tetra_volumn[index,4]=volumn
        index+=1
    return tetra_volumn
 
def random_mass(points):
    mass=np.zeros((len(points)))
    for i in range(len(points)):
        mass[i]=random.random()
    return mass

       
def random_time(simulation_step=100):    
    dt=np.zeros((simulation_step))
    for i in range(simulation_step):
        dt[i]=random.random()
    return dt

def triangle_volumn(p1,p2,p3,p4):
    volumn_matrix=np.array([[1,1,1,1],
                                [p1[0],p2[0],p3[0],p4[0]],
                                 [p1[1],p2[1],p3[1],p4[1]],
                                 [p1[2],p2[2],p3[2],p4[2]]])
    volumn=np.linalg.det(volumn_matrix)/6
    return volumn
    
    
def prepare_data():
    points,line,triangles,tetra,vertex=generate_mesh()
    get_points=np.array([[0,0,1],[0,2,1],[2,2,1],[2,0,1]]).astype(float)
    rest_length=build_rest_length(triangles,points)
    surface_points=get_surface_points(line)
    point_properity=define_point_properity(points)
    tetra_volumn=get_tetra_volumn(tetra,points)
    dt=random_time(100)
    mass=random_mass(points)
    return get_points,rest_length,surface_points,tetra,point_properity,tetra_volumn,dt,mass



def position_update(v,points,dt,interation):
    
    for i in range(len(points)):
        points[i] += v[i] * dt[interation]
    return points


#The above function can be ignored. And the later one is the most important part
    
#using shape matching
def shape_matching(stiffness, old_points,new_points):
    
    DeltaX = np.zeros((len(old_points),3))
    old_mean = np.mean(old_points,axis=0)  #t0
    new_mean = np.mean(new_points,axis=0)  #t
    old_diff = old_points - old_mean
    new_diff = new_points - new_mean
    rotation_ = np.zeros([3,3])
    A=np.zeros([3,3])
    for i in range(len(points)):
        qi=points[i]
        wi=0
        rotation_ += new_diff[i,:].reshape(3,1).dot(old_diff[i,:].reshape(1,3))
        '''
        x2 = wi * qi[0] * qi[0]
        y2 = wi * qi[1] * qi[1]
        z2 = wi * qi[2] * qi[2]
        xy = wi * qi[0] * qi[1]
        xz = wi * qi[0] * qi[2]
        yz = wi * qi[1] * qi[2]
        A[0, 0] += x2 
        A[0, 1] += xy 
        A[0, 2] += xz
        A[1, 0] += xy
        A[1, 1] += y2
        A[1, 2] += yz
        A[2, 0] += xz
        A[2, 1] += yz
        A[2, 2] += z2
        
    rotation_  =rotation_.dot(np.linalg.inv(A))  
    '''
    rotation, symmetric = scipy.linalg.polar(rotation_)
    
    rotation=rotation/np.linalg.det(rotation)
    tmp =  new_mean-rotation.dot(old_mean)
   
    Transform = np.column_stack((rotation, tmp.T))  
    for i in range(len(points)):
        
        Homogenous = np.row_stack((old_points[i,:].reshape(3,1),np.array([1])))
        
        x_offset =1 *(Transform.dot(Homogenous).squeeze() - new_points[i,:])
        DeltaX[i,:] += x_offset +old_points[i,:]-Transform.dot(Homogenous).squeeze()
        #DeltaX[i,:] += x_offset
        
    return DeltaX
  
def updata_velosity(new_points,old_points,interation,dt): #updata velosity after combining constraints
    v=np.zeros((len(points),3))
    for i in range(len(new_points)):
        v[i] = (new_points[i] - old_points[i]) * 1/dt[interation]
    return v

def get_location(num_points,tetra,unchange,new_points,stiffness,dt,interation,damping,mass,rest_length,v,point_properity):
   
    #v=substep(num_points,dt,damping,interation,mass,rest_length,v)
    #print(np.unique(v))
    #old_volumn=get_volumn(points,tetra)
    #print('The old volumn is',abs(old_volumn))
    print(unchange)
    if interation==2:
        new_points=position_update(v,new_points,dt,interation)
        print(new_points)
        file_name='/Users/entongsu/Downloads/robotics/week_2/data/'+str(1)+'.npy'
        np.save(file_name,new_points)
   
    new_points=position_update(v,new_points,dt,interation)
    #new_points=position_update(v,points,dt,interation)
    DeltaX=np.zeros((len(unchange),3))
   
    for i in range(300):
        
        #constraint_neighbors,constraint_num_neighbors=spring_constraint(new_points,rest_length)
        
        #volumn_constraint_diff,volumn_diff_num=volumn_constraint(tetra_volumn,new_points)
        #position_delta_tmp=stretch_constraint(new_points,constraint_neighbors,constraint_num_neighbors,mass)
        #position_delta_tmp=modify_volumn(new_points,volumn_constraint_diff,volumn_diff_num,tetra_volumn)
        DeltaX=shape_matching(stiffness, unchange, new_points)
        
        for i in range(len(unchange)):
            #if point_properity[i]==1 :
                 new_points[i]=new_points[i]+DeltaX[i]
      
    
    
    v=updata_velosity(new_points,points,interation,dt)
 
    
   
    #new_volumn=get_volumn(new_points,tetra)
    #print('The new volumn is',abs(new_volumn))
    file_name='/Users/entongsu/Downloads/robotics/week_2/data/'+str(interation)+'.npy'
    np.save(file_name,new_points)
    return new_points,v

def solve(points,rest_length,surface_points,tetra,point_properity,tetra_volumn,dt,mass):
   num_points=len(points)
   #num_tetra=len(tetra)
   v=np.zeros((len(points),3))
   v[1]=[1,2,3]
   v[2]=[2,3,4]
   v[3]=[2,4,6]
   v[0]=[1,3,5]
   
   list=range(1,len(points))

   #fixed_points=random.sample(list,int(len(points)/100))
   #r = R.from_quat([0, 0, np.sin(np.pi/6), np.cos(np.pi/6)])
   #kk=r.as_matrix()
   #kk[1]=[1,2,3]
   #for i in range(len(points)):
   #    new_points[i]=kk.dot(points[i])
   
   #v[2]=[2,3,0]
   new_points= copy.deepcopy(points)
   simulation_step=15
   stiffness=1
   interation=2
   damping=30
   #file_name='/Users/entongsu/Downloads/robotics/week_2/data/'+str(0)+'.npy'
   #np.save(file_name,points)
   
   file_name='/Users/entongsu/Downloads/robotics/week_2/data/'+str(1)+'.npy'
   np.save(file_name,points)
   
   
   unchange=points
   while interation<simulation_step:
       
       #unchange=np.array([[0,0,1],[0,2,1],[2,2,1],[2,0,1]]).astype(float)
       new_points,v=get_location(num_points,tetra,unchange,new_points,stiffness,dt,interation,damping,mass,rest_length,v,point_properity)
       interation+=1
       #points=unchange
       
      
    
   
        
   return new_points
    
def create_image():
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    
    # geometry is the point cloud used in your animaiton
    geometry = o3d.geometry.PointCloud()
    vis.add_geometry(geometry)
    
    for i in range(15):
        file_name='/Users/entongsu/Downloads/robotics/week_2/data/'+str(i)+'.npy'
        pc_xyzrgb=np.load(file_name)
        pc = o3d.PointCloud()
        pc.points = o3d.Vector3dVector(pc_xyzrgb[:, 0:3])
        # now modify the points of your geometry
        # you can use whatever method suits you best, this is just an example
        
        geometry.points = pc.points 
        vis.add_geometry(geometry)
        vis.update_geometry()
        vis.poll_events()
        vis.update_renderer()
        vis.capture_screen_image("/Users/entongsu/Downloads/robotics/week_2/data/temp_%04d.jpg" % i)
    vis.destroy_window()

def create_video():
    writer = imageio.get_writer('/Users/entongsu/Downloads/robotics/week_2/data/shape_matching.mp4', fps=1)

    for index in range(15):
        image_path="/Users/entongsu/Downloads/robotics/week_2/data/temp_%04d.jpg" % index
        frame = imageio.imread(image_path)
        writer.append_data(frame)
    
    writer.close()

if __name__ == '__main__':
    points,rest_length,surface_points,tetra,point_properity,tetra_volumn,dt,mass=prepare_data()
  
    new_points=solve(points,rest_length,surface_points,tetra,point_properity,tetra_volumn,dt,mass)
    create_image()
    create_video()

#%%
distance=new_points[2]-new_points[1]
print(np.linalg.norm(distance))
#%%