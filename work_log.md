# PBD

# Week 2
2021  January 18th

1、read the article about the application of PBD and make notes.

2、find and compare different methods to generate different kinds of mesh and find way to visuliaze the mesh. And I have found that by using pygmsh and pyvista, I can generate different mesh and get their points.
 
3、rewatch the video of taichi and read the documentation of taichi.




2021 January 19th

1. I have created the mesh for the PBD to test by using pygmsh libarary

2. Trying to be familiar with the pyrender to visualize 3D mesh and it seems that I can use pyrender to visualize the 3D model I downloaded.

3. Having a discussion with YunHai and begin to work the PBD coding 



2021 January 20th

1. Beginning to write the coding for the PBD and also finds to demo to help me have a better understand about the theory of PBD.

2.I have created the mesh and modify related parameter for the model.





2021 January 21th

1. Finishing the coding part for shape matching -> rigid body or soft body

2.Finishing the coding part for volumn constraint -> gas

3.Finishing the coding part for distance constraint ->  stretch


2021 January 22th

1.modifying the coding and verify the related math equation

2. using open3D to visualize the pointcloud and convert them into images and video

3. I have found a problem. When I apply volumn constraint on the object, even though I have set a velocity at the beginning, after applying the solver, the velocity always become zero. But this situation does not happen on the stretch or shape matching.


2021 January 23th

1. Trying to set some points in the object as fixed to modify the model. 

2. I have set some points in the object as fixed to modify the model. And the problem occurs in the January 22th has not happened again. 

3. I still find another problem. When I only apply the volumn constraint, the shape change in a normal ways

It seems that the code can run, but some parameter and some setting should be considered so that the simulation more reasonable.

### Weekly analysis:

I have created a video to show the situation.The video is in 2D.

1) volumn constraint

[Video](https://github.com/Entongsu/work/blob/master/data/volume/volumn_constraint.mp4 "here")


[Image of original point cloud]
![Image of original point cloud ](https://github.com/Entongsu/work/blob/master/data/volume/temp_0000.jpg)
Image of final point cloud
![Image of original point cloud ](https://github.com/Entongsu/work/blob/master/data/volume/temp_0009.jpg)

2) shape matching
 [Video](https://github.com/Entongsu/work/blob/master/data/shape%20matching/shape_matching.mp4 "here")


Image of original point cloud
![Image of original point cloud ](https://github.com/Entongsu/work/blob/master/data/shape%20matching/temp_0000.jpg)
Image of final point cloud
![Image of original point cloud ](https://github.com/Entongsu/work/blob/master/data/shape%20matching/temp_0009.jpg)


The update code is [Here](https://github.com/Entongsu/work/blob/master/postion.py "here").(It is better to run it in the spyder.)

