# PBD


## week 3
### shape_matching.py 

In order to run the code, user should modify the file location and can custom the some parameter,such as stiffness 

And I have set the origin points as unchanged and the original shape is square.
The original square as show below. 
location of the original points

![Image ](https://github.com/Entongsu/work/blob/master/shape_matching%20demo/changeall/temp_0000.jpg)

[0., 0., 1.],
[0., 2., 1.],
[2., 2., 1.],
[2., 0., 1.]

And the changed points location as bewlow.

![Image ](https://github.com/Entongsu/work/blob/master/shape_matching%20demo/changeall/temp_0001.jpg)

location of the changed points.

[[0.72801132 0.72801132 0.72801132]

 [0.72801132 1.45602264 2.18403397]
 
 [0.72801132 0.72801132 0.72801132]
 
 [0.72801132 0.72801132 0.72801132]]
 
 I have change the second point into a very different location and other points change into the same location.
 

And the video has showed the changed of the points. 

If I set the stiffness of stiffness into different value, the shape of the square becomes bigger, but if I set the stiffness as 1, the shape of the square unchanged. 

1)if the stiness is 0.01,
The locations of final points.

[video](https://github.com/Entongsu/work/blob/master/shape_matching%20demo/shape_matching_0.01.mp4)

| original points | final points |
| :-----| ----: | 
|[0., 0., 1.]| [-13771.57154176, -10093.62211758,  -6416.97837706] |
|  [0., 2., 1.]|[-13771.53298178, -10096.10121165,  -6416.9365703 ] |
| [2., 2., 1.] | [-13774.0123206 , -10096.1402962 ,  -6416.96258813]|
| [2., 0., 1.]|[-13774.05088058, -10093.66120212,  -6417.00439489]|

The orignal distance between two pair of points is 2, but now the distance become 2.4797463771484245.

2)But if I change the stiffness into 1, 

[video](https://github.com/Entongsu/work/blob/master/shape_matching%20demo/shape_matching_1.mp4)

| original points | final points |
| :-----| ----: | 
|[0., 0., 1.]| -17034.90662831, -14501.31517926, -11968.72516619] |
|  [0., 2., 1.]|[-17034.92732662, -14503.31251132, -11968.6239919 ] |
| [2., 2., 1.] |[-17036.92693506, -14503.2935489 , -11968.65872676]|
| [2., 0., 1.]|[-17036.90623676, -14501.29621685, -11968.75990105] |

The orignal distance between two pair of points is 2, but now the distance keep about 2.000000000000434, but the points become far away from the original one.

3)if I set stiffness as 0.1, the final distance is 2.000000000014667. 

[video](https://github.com/Entongsu/work/blob/master/shape_matching%20demo/shape_matching_0.1.mp4)

### Analysis

I think the size of the shape is affected by the setting of the stiffness. It is normal to get different size for the same points. But I am not sure whether it is normal for points to become far from the original one. 

Because the location of the final points becomes far away from the original one, the points in the image seems to be smaller, but the distance between pair of points is unchanged. 

I also verify my coding by just changing the location of one point, the distance between pair of points is unchanged. 

In order to show the size of the final points, I have modify the coding here. [link](https://github.com/Entongsu/work/blob/master/shape_matching%20demo/shape_matching.py#L180)

And after I modify the location of the final points, the image show the actual size of the final square. 

1) change the location of one point. 
![image](https://github.com/Entongsu/work/blob/master/shape_matching%20demo/onepoint/temp_0002.jpg)

2) change four points 
![image](https://github.com/Entongsu/work/blob/master/shape_matching%20demo/changeall/temp_0002.jpg)

### Coding notation
1)The most important part is shape matching and the former coding can be ignored. [link] (https://github.com/Entongsu/work/blob/master/shape_matching%20demo/shape_matching.py#L137)

2) And user can change the location of the original points by changing the value of the velocity here. [link]
(https://github.com/Entongsu/work/blob/master/shape_matching%20demo/shape_matching.py#L137)

3) Changing the file location when run the code.



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


Image of original point cloud
![Image of original point cloud ](https://github.com/Entongsu/work/blob/master/volume/temp_0000.jpg)
Image of final point cloud
![Image of original point cloud ](https://github.com/Entongsu/work/blob/master/volume/temp_0009.jpg)

2) shape matching

 [Video](https://github.com/Entongsu/work/blob/master/shape%20matching/shape_matching.mp4 "here")


Image of original point cloud
![Image of original point cloud ](https://github.com/Entongsu/work/blob/master/shape%20matching/temp_0000.jpg)
Image of final point cloud
![Image of original point cloud ](https://github.com/Entongsu/work/blob/master/shape%20matching/temp_0009.jpg)


After I set some points to be fixed, the change of velocity of shape matching and volume constraint seems to be more reasonable. But when I apply the shape matching to the model, the volume becomes smaller and smaller. I think it is likely caused by the parameter setting.

The update code is [Here](https://github.com/Entongsu/work/blob/master/postion.py "here").(It is better to run it in the spyder.)

