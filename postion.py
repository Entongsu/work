from math import pi
import pygmsh
import numpy as np
import random
import scipy
from scipy import linalg
import open3d  as o3d
import imageio

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
    rest_length=build_rest_length(triangles,points)
    surface_points=get_surface_points(line)
    point_properity=define_point_properity(points)
    tetra_volumn=get_tetra_volumn(tetra,points)
    dt=random_time(100)
    mass=random_mass(points)
    return points,rest_length,surface_points,tetra,point_properity,tetra_volumn,dt,mass



def substep(num_points,dt,damping,interation,mass,rest_length,v):
    spring_stiffness=100
    gravity=np.zeros(3)
    for i in range(num_points):
        v[i] =v[i] *np.exp(-dt[interation] * damping) # damping
        total_force = gravity * mass[i]
        for j in range(num_points):
            if rest_length[i,j]!=0:
                points_ij=points[i]-points[j]
                total_force += -spring_stiffness * (np.linalg.norm(points_ij) - rest_length[i, j]) * np.linalg.norm(points_ij)
                v[i] += dt[interation] * total_force / mass[i]
   
    return v

def position_update(v,points,dt,interation):
    
    for i in range(len(points)):
        points[i] += v[i] * dt[interation]
    return points
    
def spring_constraint(points,rest_length):
    constraint_neighbors=np.zeros((len(points),len(points)))
    constraint_num_neighbors=np.zeros((len(points)))
    for i in range(len(points)):
        null = 0
        for j in range(len(points)):
            if rest_length[i, j] != 0: #spring-constraint
                points_ij=points[i]-points[j]
                dist_diff = abs(np.linalg.norm(points_ij) - rest_length[i, j])
                if dist_diff > 0:
                    
                    constraint_neighbors[i, null] = j
                    null+= 1
        constraint_num_neighbors[i] = null
    return constraint_neighbors,constraint_num_neighbors



def volumn_constraint(tetra_volumn,points):
    volumn_constraint_diff=np.zeros(len(tetra_volumn))
    volumn_diff_num=np.zeros((len(points),1))
    for i in range(len(tetra_volumn)):
        
        p1 = points[int(tetra_volumn[i, 0])]
        p2 = points[int(tetra_volumn[i, 1])]
        p3 = points[int(tetra_volumn[i, 2])]
        p4 = points[int(tetra_volumn[i, 3])]
    
        volumn=triangle_volumn(p1,p2,p3,p4)
        
      
        if(abs(volumn - tetra_volumn[i, 4]) > 1e-8):
            volumn_constraint_diff[i] = volumn - tetra_volumn[i, 4]
            volumn_diff_num[int(tetra_volumn[i, 0])] += 1
            volumn_diff_num[int(tetra_volumn[i, 1])] += 1
            volumn_diff_num[int(tetra_volumn[i, 2])] += 1
            volumn_diff_num[int(tetra_volumn[i, 3])] += 1
        else:
            volumn_constraint_diff[i] = 0.0
    return volumn_constraint_diff,volumn_diff_num


# for stretch
def stretch_constraint(points,constraint_neighbors,constraint_num_neighbors,mass):
    for i in range(len(points)):
        point_i = points[i]
        posi_tmp = np.zeros(3)
        position_delta_tmp=np.zeros((len(points),3))
        mass_i_inv = 1 / mass[i]
        for j in range(int(constraint_num_neighbors[i])):
            j_index = int(constraint_neighbors[i, j])
            point_j = points[j_index]
            point_ij = point_i - point_j
            dist_diff = np.linalg.norm(point_ij) - rest_length[i,j_index]
            grad = np.linalg.norm(dist_diff)
            mass_j_inv = 1 / mass[j_index]
            mass_ij_inv = 1 / (mass_i_inv + mass_j_inv)
            position_delta = -mass_i_inv * mass_ij_inv * dist_diff * grad / constraint_num_neighbors[i]
            posi_tmp += position_delta
       
        position_delta_tmp[i] = posi_tmp
    return position_delta_tmp




def modify_volumn(points,volumn_constraint_diff,volumn_diff_num,tetra_volumn,position_delta_tmp):
    for i in range(len(points)):
        if(volumn_constraint_diff[i] != 0.0):
            #diff_volumn = volumn_constraint_diff[i]
            p1_index = tetra_volumn[i, 0]
            p2_index = tetra_volumn[i, 1]
            p3_index = tetra_volumn[i, 2]
            p4_index = tetra_volumn[i, 3]
            p1 = points[int(p1_index)]
            p2 = points[int(p2_index)]
            p3 = points[int(p3_index)]
            p4 = points[int(p4_index)]
            grad_x1 = ((p1[1] - p3[1])*(p1[2] - p2[2]))/6 - ((p1[1] - p2[1])*(p1[2] - p3[2]))/6 + ((p1[1] - p4[1])*(p2[2] - p3[2]))/6 - ((p2[1] - p3[1])*(p1[2] - p4[2]))/6
            grad_y1 = ((p1[0] - p2[0])*(p1[2] - p3[2]))/6 - ((p1[0] - p3[0])*(p1[2] - p2[2]))/6 - ((p1[0] - p4[0])*(p2[2] - p3[2]))/6 + ((p2[0] - p3[0])*(p1[2] - p4[2]))/6
            grad_z1 = ((p1[0] - p3[0])*(p1[1] - p2[1]))/6 - ((p1[0] - p2[0])*(p1[1] - p3[1]))/6 + ((p1[0] - p4[0])*(p2[1] - p3[1]))/6 - ((p2[0] - p3[0])*(p1[1] - p4[1]))/6
            grad_x2 = ((p1[1] - p3[1])*(p1[2] - p4[2]))/6 - ((p1[1] - p4[1])*(p1[2] - p3[2]))/6
            grad_y2 = ((p1[0] - p4[0])*(p1[2] - p3[2]))/6 - ((p1[0] - p3[0])*(p1[2] - p4[2]))/6
            grad_z2 = ((p1[0] - p3[0])*(p1[1] - p4[1]))/6 - ((p1[0] - p4[0])*(p1[1] - p3[1]))/6
            grad_x3 = ((p1[1] - p4[1])*(p1[2] - p2[2]))/6 - ((p1[1] - p2[1])*(p1[2] - p4[2]))/6
            grad_y3 = ((p1[0] - p2[0])*(p1[2] - p4[2]))/6 - ((p1[0] - p4[0])*(p1[2] - p2[2]))/6
            grad_z3 = ((p1[0] - p4[0])*(p1[1] - p2[1]))/6 - ((p1[0] - p2[0])*(p1[1] - p4[1]))/6
            grad_x4 = ((p1[1] - p2[1])*(p1[2] - p3[2]))/6 - ((p1[1] - p3[1])*(p1[2] - p2[2]))/6
            grad_y4 = ((p1[0] - p3[0])*(p1[2] - p2[2]))/6 - ((p1[0] - p2[0])*(p1[2] - p3[2]))/6
            grad_z4 = ((p1[0] - p2[0])*(p1[1] - p3[1]))/6 - ((p1[0] - p3[0])*(p1[1] - p2[1]))/6
            grad_p1 = np.array([grad_x1, grad_y1, grad_z1])
            tmp_p1 = (np.linalg.norm(grad_p1))**2
            w_p1 = 1 / mass[int(p1_index)]
            grad_p2 = np.array([grad_x2, grad_y2, grad_z2])
            tmp_p2 = (np.linalg.norm(grad_p2))**2
            w_p2 = 1 / mass[int(p2_index)]
            grad_p3 = np.array([grad_x3, grad_y3, grad_z3])
            tmp_p3 = (np.linalg.norm(grad_p3))**2
            w_p3 = 1 / mass[int(p3_index)]
            grad_p4 = np.array([grad_x4, grad_y4, grad_z4])
            tmp_p4 = (np.linalg.norm(grad_p4))**2
            w_p4 = 1 / mass[int(p4_index)]
            denominator = w_p1 * tmp_p1 + w_p2 * tmp_p2 + w_p3 * tmp_p3 + w_p4 * tmp_p4
            constraint_lambda = volumn_constraint_diff[i] / denominator
            delta_p1 = -constraint_lambda * w_p1 * grad_p1 / volumn_diff_num[int(p1_index)]
            delta_p2 = -constraint_lambda * w_p2 * grad_p2 / volumn_diff_num[int(p2_index)]
            delta_p3 = -constraint_lambda * w_p3 * grad_p3 / volumn_diff_num[int(p3_index)]
            delta_p4 = -constraint_lambda * w_p4 * grad_p4 / volumn_diff_num[int(p4_index)]
            position_delta_tmp[int(p1_index)] += delta_p1
            position_delta_tmp[int(p2_index)] += delta_p2
            position_delta_tmp[int(p3_index)] += delta_p3
            position_delta_tmp[int(p4_index)] += delta_p4
        return position_delta_tmp


#using shape matching
def shape_matching(stiffness, old_points, new_points):
    
    DeltaX = np.zeros((len(old_points),3))
    old_mean = np.mean(old_points,axis=0)  #t0
    new_mean = np.mean(new_points,axis=0)  #t
    old_diff = old_points - old_mean
    new_diff = new_points - new_mean
    rotation_ = np.zeros([3,3])
    for i in range(len(points)):
        rotation_ += new_diff[i,:].reshape(3,1).dot(old_diff[i,:].reshape(1,3))
  
    rotation, symmetric = scipy.linalg.polar(rotation_)
    tmp = new_mean - rotation.dot(old_mean)
    Transform = np.column_stack((rotation, tmp.T))  
    for i in range(len(points)):
        Homogenous = np.row_stack((old_points[i,:].reshape(3,1),np.array([1])))
        x_offset = stiffness * (Transform.dot(Homogenous).squeeze() - new_points[i,:])
        DeltaX[i,:] += x_offset 
    return DeltaX
    



def updata_velosity(new_points,old_points,interation,dt): #updata velosity after combining constraints
    v=np.zeros((len(points),3))
    for i in range(len(new_points)):
        v[i] = (new_points[i] - old_points[i]) * 1/dt[interation]
    return v



def get_volumn(new_points,tetra):
    volumn=0
    for i in range(len(tetra)):
        p1=new_points[tetra[i,0]]
        p2=new_points[tetra[i,1]]
        p3=new_points[tetra[i,2]]
        p4=new_points[tetra[i,3]]
       
        volumn+=triangle_volumn(p1,p2,p3,p4) 
    return volumn

def get_location(num_points,tetra,points,stiffness,dt,interation,damping,mass,rest_length,v,point_properity):
    v=substep(num_points,dt,damping,interation,mass,rest_length,v)
    old_volumn=get_volumn(points,tetra)
    print('The old volumn is',abs(old_volumn))
    old_points=position_update(v,points,dt,interation)
    new_points=np.zeros((len(points),3))
    DeltaX=np.zeros((len(points),3))
    
    for i in range(3):
        constraint_neighbors,constraint_num_neighbors=spring_constraint(old_points,rest_length)
        
        volumn_constraint_diff,volumn_diff_num=volumn_constraint(tetra_volumn,old_points)
        position_delta_tmp=stretch_constraint(old_points,constraint_neighbors,constraint_num_neighbors,mass)
        position_delta_tmp=modify_volumn(old_points,volumn_constraint_diff,volumn_diff_num,tetra_volumn,position_delta_tmp)
        DeltaX=shape_matching(stiffness, old_points, new_points)
        for i in range(len(points)):
            if point_properity[i]==1:
                new_points[i]=old_points[i]+DeltaX[i]
        
    v=updata_velosity(new_points,old_points,interation,dt)
    
    print(np.unique(v))
    new_volumn=get_volumn(new_points,tetra)
    print('The new volumn is',abs(new_volumn))

    file_name='/Users/entongsu/Downloads/robotics/week 2/data/'+str(interation)+'.npy'
    np.save(file_name,new_points)
    return new_points,v


def visual(file_name):
    pc_xyzrgb=np.load(file_name)
    pc = open3d.PointCloud()
    pc.points = open3d.Vector3dVector(pc_xyzrgb[:, 0:3])
    if pc_xyzrgb.shape[1] == 3:
        open3d.draw_geometries([pc])
        return 0
    if np.max(pc_xyzrgb[:, 3:6]) > 20:  ## 0-255
        pc.colors = open3d.Vector3dVector(pc_xyzrgb[:, 3:6] / 255.)
    else:
        pc.colors = open3d.Vector3dVector(pc_xyzrgb[:, 3:6])
    open3d.draw_geometries([pc])


def solve(points,rest_length,surface_points,tetra,point_properity,tetra_volumn,dt,mass):
   num_points=len(points)
   #num_tetra=len(tetra)
   v=np.zeros((len(points),3))
   #v =v *np.exp(0.01 * 30)
   simulation_step=10
   stiffness=1
   interation=1
   damping=30
 
   
   file_name='/Users/entongsu/Downloads/robotics/week 2/data/'+str(0)+'.npy'
   np.save(file_name,points)
   
   
   
   while interation<simulation_step:
       points,v=get_location(num_points,tetra,points,stiffness,dt,interation,damping,mass,rest_length,v,point_properity)
       interation+=1
      
    
   for i in range(simulation_step):
       file_name='/Users/entongsu/Downloads/robotics/week 2/data/'+str(i)+'.npy'  
        
   return points
    
def create_image():
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    
    # geometry is the point cloud used in your animaiton
    geometry = o3d.geometry.PointCloud()
    vis.add_geometry(geometry)
    
    for i in range(10):
        file_name='/Users/entongsu/Downloads/robotics/week 2/data/'+str(i)+'.npy'
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
        vis.capture_screen_image("/Users/entongsu/Downloads/robotics/week 2/data/temp_%04d.jpg" % i)
    vis.destroy_window()

def create_video():
    writer = imageio.get_writer('/Users/entongsu/Downloads/robotics/week 2/data/shape_matching.mp4', fps=1)

    for index in range(4):
        image_path="/Users/entongsu/Downloads/robotics/week 2/data/temp_%04d.jpg" % index
        frame = imageio.imread(image_path)
        writer.append_data(frame)
    
    writer.close()

if __name__ == '__main__':
    points,rest_length,surface_points,tetra,point_properity,tetra_volumn,dt,mass=prepare_data()
    new_points=solve(points,rest_length,surface_points,tetra,point_properity,tetra_volumn,dt,mass)
    create_image()

#%%