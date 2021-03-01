# PBD


## week 7

I have writen several function from viper by python and I think I need some paramter and methods to visualize the deformed process to verify the accurancy of the function. At the same time, I have confusement over some detail. 
1. It seems that the contraint paramter is modified by myself or modified during the visualizing the objects. 
2. I wonder whether I needs to write the whole "viper" project into python format or just some important fuction?
3. I think it is better to write the coding into a python project? I means that it seems that a lof of previous setting is needed.
4. I tried to real-time visualizing in blender and it seems that it is feasible enough and it seems that open3d can do the real-time rendering.But I have not verified that. 
## week 6
4. In this week, I used the python console in the blender to create muscle objects by coding and modified it by using "knife" to create the triangle mesh on the surface of cone. And I have improved the model step by step. And all of the process can be completed by coding, which can improve the effiency, especially when we need to create a lot of objects. 


   (1) Creating the the surface which will be used as demo to create muslce surface, but the location of particle is not ideal. 
 
 <div align=center>
<img src="https://github.com/Entongsu/work/blob/master/image/1.png"  width="200" height="200"  />
</div>

<div align=center>
<img src="https://github.com/Entongsu/work/blob/master/image/shape_matching_process.gif"  width="300" height="300"  />
</div>
     (2) Using knife to cut the original model into 100 small piece, which can make the location of circle partical more accurate.
 
 <div align=center>
<img src="https://github.com/Entongsu/work/blob/master/image/2.png"  width="200" height="200"  />
</div>
     (3) In order to create the cone between two circle particle with triangle mesh, I also use "knife " to cut the surface for 3 times. 

<div align=center>
<img src="https://github.com/Entongsu/work/blob/master/image/3.png"  width="200" height="200" />
</div>
Image does not have triangle mesh between two circle sphere.
<div align=center>
<img src="https://github.com/Entongsu/work/blob/master/image/no_surface_mesh%20.png" width="400" height="400" />
 </div>

Image has triangle mesh between two circle sphere.

<div align=center>
<img src="https://github.com/Entongsu/work/blob/master/image/surface_mesh%20.png"  width="400" height="400" />
</div>
  It is obvious that with the "knife cut", thera are several triangle mesh between the two circle sphere. 
    (4) Also the coding can union all the bones together，but it needs human to adjust the segmentation by hand. 

2. Dataset:I have writen a document which can be used to save and reload the data of the muscle model effiecently. 

3. I have read the "Viper" coding and I am trying to write it into a python format.

## week 5

Happy New Year!

1. I have designed a simple muscle model by using blender and generate the tetra of the muscle by using the gmsh.

2. I am writing the code about the real time rendering. But I have encountered a problem that it seems that the rendering process needs a cpu with 32G or 64G storage.And my computer just has 32G, which is not suitable to do the rendering directly. Because when I apply the rendering, my computer becomes very slow and cannot do annything.

3. I am also writing the code for muscle simulation. But the coding in the Viper is a little difficult in understanding and I also cannot find the theory about the restricted CVD, which makes it harder for me to comprehen the coding. 


## week 4

1. I have rewrote the code for the shape matching, volumn and distance constrains. It seems that the volumn and distance constrains can function and put the deformed mesh toward the original volumn and distance. 

2. **Modification of the coding**
1) shape matching: I have made the transformation function complete.
2) volumn constrain: I have rewrote the coding refering to the [link](https://github.com/InteractiveComputerGraphics/PositionBasedDynamics/blob/master/PositionBasedDynamics/PositionBasedDynamics.cpp), but I have problems about the stiffness.
3) stretch constrain: I have rewrote the coding refering to the [link](https://github.com/InteractiveComputerGraphics/PositionBasedDynamics/blob/master/PositionBasedDynamics/PositionBasedDynamics.cpp),but I have problems about the stiffness.
It seems that the volumn constrain and stretch constrain function slowly and by combining them with shape matching, the model can function much better.

3. I begin to learn the software blender and has made some basic 3D object and also use gmsh to generate mesh for them to run in my code.In order to simulate the muscle, I need to some time to learn more for the blender. 

4. I have tried to use the ply file I get from the blender to apply into the shape matching process. The interation steps is 30 times. It seems the final point cloud has some difference with the original one. 
The image show the transparent final point cloud. 
<img src="https://github.com/Entongsu/work/blob/master/image/final.png" width="500" height="500" />
The image shows the difference between the orignal and final point cloud.And the fissures  show the difference. 

<img src="https://github.com/Entongsu/work/blob/master/image/difference.png" width="500" height="500" />

5. It seems that the mesh incuding the tetra mesh and triangle mesh and sometimes the generated mesh just has triangle mesh, so I try to write the coding for  strain  triangle constrain and it seems that this kind of constraint is suitable in simulating the soft object. I plan to add some constrain to my coding which is suitable to the triangle mesh. It seems that in the three constraint I have coded now, only the shape matching and stretch constraint is usable. Because the generated mesh only has triangle mesh. But the shape matching constraint is more suitable for the rigid body? and the strech constraint run very slow. I think it is suitable to add some other triangle constrain and other constrain to better simulation the PBD?
 

6. With the help of blender, I can visualize the triangle mesh and tetra mesh for the object I generated from pygmsh. I found the the triangle mesh only has surface data and I think it is the reason why some place in open3d is transparent. But If I apply the tetra mesh into the blender, it is obvious that the whole oject has tetra mesh. 
The images shows the shape of object I generate from the pygmsh.The left one is triangle mesh and the right one is tetra mesh. 

<img src="https://github.com/Entongsu/work/blob/master/image/pygmsh.png" width="500" height="500" />
<img src="https://github.com/Entongsu/work/blob/master/image/pygmsh_1.png" width="500" height="500" />

## week 3

### 1. shape_matching.py 



### Coding notation
1) The most important part is shape matching and the former coding can be ignored. [link] (https://github.com/Entongsu/work/blob/master/shape_matching%20demo/shape_matching.py#L137)

2) And user can change the location of the original points by changing the value of the velocity here. [link]
(https://github.com/Entongsu/work/blob/master/shape_matching%20demo/shape_matching.py#L137)

3) Changing the file location when run the code.

4) The 'substep' part in the coding: Damping to reduce the velocity. It seems that this part in the coding of taichi is very important. If I do not use this part in my coding, it seems that the shape matching part and the volumn constrain part can function well, but it need to take more time to return the origin.


### experiment on the complex object

In order to verify the coding, I have do experiment on the complex object.
And I have found some interesting points. If the stiffness is small, the deformed object needs more times to find the best rigid transformation.

And the coding keep the object deformed all the time. So the object will be deformed, even though it return to the normal position in the last time. 

It seems that the situation can be changed by setting some points as fixed. Under this situation, the final points will be near the original one.(But the fixed points should take a large proportion of all points. )



<img src="https://github.com/Entongsu/work/blob/master/shape_matching%20demo/shape_matching.gif" width="700" height="700" />


### Comparison

#### Comparsion 1
I have run for 100 times to get the final point cloud.
I have made a comparsion between the different point cloud.
1) The image of original point cloud and deformed point cloud from differnt angle.

<img src="https://github.com/Entongsu/work/blob/master/shape_matching%20demo/3Dimage/deformed1.png" width="300" height="300" />


<img src="https://github.com/Entongsu/work/blob/master/shape_matching%20demo/3Dimage/deformed2.png" width="300" height="300" />


<img src="https://github.com/Entongsu/work/blob/master/shape_matching%20demo/3Dimage/deformed3.png" width="300" height="300" />


<img src="https://github.com/Entongsu/work/blob/master/shape_matching%20demo/3Dimage/deformed14.png" width="300" height="300" />

2) The image of original point cloud and final point cloud from differnt angle.

<img src="https://github.com/Entongsu/work/blob/master/shape_matching%20demo/3Dimage/final1.png" width="300" height="300" />


<img src="https://github.com/Entongsu/work/blob/master/shape_matching%20demo/3Dimage/final2.png" width="300" height="300" />


<img src="https://github.com/Entongsu/work/blob/master/shape_matching%20demo/3Dimage/final13.png" width="300" height="300" />



<img src="https://github.com/Entongsu/work/blob/master/shape_matching%20demo/3Dimage/final14.png" width="300" height="300" /> 



The pink one is original point cloud and the black one in the 1) is deformed object and black one in 2) is 
final point cloud. 

And the average distance betwween the original point cloud  and deformed  point cloud is 0.9359840468431038.

And the average distance betwween the original point cloud  and final  point cloud is 4.322568059488684e-09.

#### Comparsion 2
And the average distance betwween the original point cloud  and deformed  point cloud is 0.35488046835904546.

I have run for 60 times to get the final point cloud, the average distance  betwween the original point cloud  and final  point cloud is 0.0051741315057538765.

1) The gif of original points .(The pink one is the orignal points) 

<img src="https://github.com/Entongsu/work/blob/master/shape%20matching/original.gif" width="700" height="700" />

2) The gif of deformed points .(The pink one is the deformed points) 

<img src="https://github.com/Entongsu/work/blob/master/shape%20matching/deformed.gif" width="700" height="700" />

3) The gif of final points. (The red one is the final points.)
<img src="https://github.com/Entongsu/work/blob/master/shape%20matching/final.gif" width="700" height="700" />



In order to make a comparsion between orginal point cloud and the final point cloud, I have combined them together. 
From the average distance and image, it is reasonable to regard that after applying the shape matching, the original point cloud and final point cloud is matching well.

4) The gif of combined original and  final points. (The red one is the final points and the pink one is original points)
<img src="https://github.com/Entongsu/work/blob/master/shape%20matching/comparision.gif" width="700" height="700" />

5) The process of shape matching.
<img src="https://github.com/Entongsu/work/blob/master/shape%20matching/shape_matching_process.gif" width="700" height="700" />

### 2. volumn constraint

I have found that by running the original demo, the volumn of the deformed point cloud become bigger and bigger. So I rewrite the part about volumn constraint. After I rewrite this part, the volumn becomes smaller and smaller after applying the volumn constrain. But it needs to take more steps to return to the original volumn. During this process, I do not set any points as fixed.

It is the process of deformed point cloud to return to original volumn. 
<img src="https://github.com/Entongsu/work/blob/master/volume/volumn_process.gif" width="700" height="700" />


## Week 2
### 2021  January 18th

1、read the article about the application of PBD and make notes.

2、find and compare different methods to generate different kinds of mesh and find way to visuliaze the mesh. And I have found that by using pygmsh and pyvista, I can generate different mesh and get their points.
 
3、rewatch the video of taichi and read the documentation of taichi.




### 2021 January 19th

1. I have created the mesh for the PBD to test by using pygmsh libarary

2. Trying to be familiar with the pyrender to visualize 3D mesh and it seems that I can use pyrender to visualize the 3D model I downloaded.

3. Having a discussion with YunHai and begin to work the PBD coding 



### 2021 January 20th

1. Beginning to write the coding for the PBD and also finds to demo to help me have a better understand about the theory of PBD.

2.I have created the mesh and modify related parameter for the model.



### 2021 January 21th

1. Finishing the coding part for shape matching -> rigid body or soft body

2.Finishing the coding part for volumn constraint -> gas

3.Finishing the coding part for distance constraint ->  stretch


### 2021 January 22th

1.modifying the coding and verify the related math equation

2. using open3D to visualize the pointcloud and convert them into images and video

3. I have found a problem. When I apply volumn constraint on the object, even though I have set a velocity at the beginning, after applying the solver, the velocity always become zero. But this situation does not happen on the stretch or shape matching.


### 2021 January 23th

1. Trying to set some points in the object as fixed to modify the model. 

2. I have set some points in the object as fixed to modify the model. And the problem occurs in the January 22th has not happened again. 

3. I still find another problem. When I only apply the volumn constraint, the shape change in a normal ways



### Weekly analysis:

I have created a video to show the situation.The video is in 2D.

1) volumn constraint

[Video](https://github.com/Entongsu/work/blob/master/volume/volumn_constraint.mp4 "here")



2) shape matching

 [Video](https://github.com/Entongsu/work/blob/master/shape%20matching/shape_matching.mp4 "here")




After I set some points to be fixed, the change of velocity of shape matching and volume constraint seems to be more reasonable. But when I apply the shape matching to the model, the volume becomes smaller and smaller. I think it is likely caused by the parameter setting.

The update code is [Here](https://github.com/Entongsu/work/blob/master/postion.py "here").(It is better to run it in the spyder.)

