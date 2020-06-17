# 3D Construction and Visualization from 2D images

We constructed an automated platform for generating 3D sunglass prototypes by extruding points from the two input 2D images - front view and side view. Therein, we apply image processing techniques to get an image that fulfils our desired requirements for the further steps in this project. We also used math and pixel information for fitting the handles. This algorithm developed with VTK and Python libraries will construct a 3D prototype for frames of any sizes but it is limited to a few shapes. Dealing with irregular frame shapes and tinted/ transparent lenses of the sunglasses make way for the future aspect of this research work.

There are two codes provided, one named as “segmentation” and other as “mesh”. Copy
the code in your python IDE (python 3.5) and add the following dependencies on the
project: vtk (v8.1.2), OpenCV (v3.4.3.18), SciPy (v1.2.1), numPy (v1.15.3)

The input images are required to be sunglasses of opaque material. It is required that for
the side view of the sunglass, it is faced to the left side for the code to work properly. One
another requirement. Initially we created the “segment” script for all kind of operations
such as
* Key '0' - To select areas of sure background
* Key '1' - To select areas of sure foreground
* Key '2' - To select areas of probable background
* Key '3' - To select areas of probable foreground
* Key 'n' - To update the segmentation
* Key 'r' - To reset the setup
* Key 's' - To save the results
However all though they were created for initial development, for the final report we don’t need
them. We only need to manually remove the frame portion from the side view and keep only the
handles of the sunglasses. 

For doing so,
* Define the filename in line 108.( filename = 'img.jpg'), where file is in the same folder.
* Run the code, two window will pop up. On the window that has the picture of side-view,
right click for the rectangle to work, drag mouse to select only frame portion, press “x” in
keyboard for that portion to go white (effects won’t be visible unless you move cursor).
For saving the file press ”w” in keyboard. (File will be saved as “cropped_sideview.png”
after program has stopped, you can press “esc” button for stopping program).
* After you have only the handle portion from side view and front view image, define the file
path of them in “frontView1” and “img_side_view1” in “mesh” script. (line 9 and 10).
* Run the code, a window will pop up showing the front view image, press escape and side view
image will be shown (make sure this is facing left), and after pressing escape again the final
mesh will show in a rendered window, and corresponding .obj file will be saved.
PS: We have included sample images for reference and testing.
