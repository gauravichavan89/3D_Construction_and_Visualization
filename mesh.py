import vtk
import cv2
import numpy as np
from scipy.ndimage.filters import median_filter


def main():
    #Importing file
    frontView1 = cv2.imread("4_f_f.jpeg", 1)
    img_side_view1 = cv2.imread("4_s.jpg", 1)

    #kernal definition for preprocessing
    kernel = np.ones((3, 3), np.uint8)
    #converting colorspace for images
    original_image = cv2.cvtColor(frontView1, cv2.COLOR_BGR2GRAY)
    img_side_view = cv2.cvtColor(img_side_view1, cv2.COLOR_BGR2GRAY)

    # Creating a binary image for thresholding
    ret, original_image = cv2.threshold(original_image, 250, 255, cv2.THRESH_BINARY)

    # closing the gaps in the foreground and retaining only the hollow portion
    closing = cv2.morphologyEx(original_image, cv2.MORPH_CLOSE, kernel)
    # gradient = cv2.morphologyEx(closing, cv2.MORPH_GRADIENT, kernel)

    # Median filtering
    gray_image_mf = median_filter(closing, 1)

    # Calculate the Laplacian
    lap = cv2.Laplacian(gray_image_mf, cv2.CV_64F)

    # Calculate the sharpened image
    sharp = closing - 0.7 * lap

    # Saturate the pixels in either direction
    sharp[sharp > 255] = 255
    sharp[sharp < 0] = 0

    # for the main frame
    #Storing the pixel information for the thresholded image of front view
    list = []
    xCoordinate = []
    yCoordinate = []
    sortedYcoordinates = []
    for x in range(sharp.shape[0]):
        for y in range(sharp.shape[1]):
            if sharp[x, y] != 255:
                xCoordinate.append(x)
                yCoordinate.append(y)
                sortedYcoordinates.append(y)
    list.append(xCoordinate)
    list.append(yCoordinate)
    sortedYcoordinates.sort()
    count = 0
    for x in range(150):
        if sortedYcoordinates[x] == sortedYcoordinates[0]:
            count += 1
    count = int(count / 2)
    print(original_image.shape)

    ##Showing the front view image
    cv2.imshow('front', frontView1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # process handle image


    # The Preprocessing of sideview
    img_side_view = cv2.resize(img_side_view,(original_image.shape[1],original_image.shape[0]))
    print(img_side_view.shape)
    # Creating a binary image
    ret, img_side_view = cv2.threshold(img_side_view, 200, 255, cv2.THRESH_BINARY)

    # closing the gaps in the foreground and retaining only the hollow portion
    closing1 = cv2.morphologyEx(img_side_view, cv2.MORPH_CLOSE, kernel)
    # gradient = cv2.morphologyEx(closing, cv2.MORPH_GRADIENT, kernel)

    # Median filtering
    gray_image_mf1 = median_filter(closing1, 1)

    # Calculate the Laplacian
    lap1 = cv2.Laplacian(gray_image_mf1, cv2.CV_64F)

    # Calculate the sharpened image
    sharp1 = closing1 - 0.7 * lap1

    # Saturate the pixels in either direction
    sharp1[sharp1 > 255] = 255
    sharp1[sharp1 < 0] = 0

    #Storing the pixel information of the sideview
    xCoordinate_side_view = []
    yCoordinate_side_view = []
    ycoordinateTemp = []
    xcoordinateTemp = []
    for x in range(sharp1.shape[0]):
        for y in range(sharp1.shape[1]):
            if sharp1[x, y] != 255:
                xCoordinate_side_view.append(x)
                yCoordinate_side_view.append(y)
                ycoordinateTemp.append(y)
                xcoordinateTemp.append(x)
    #Sorting the list, which provides very first pixel information in either x-axis or y-axis
    ycoordinateTemp.sort()
    xcoordinateTemp.sort()

    #Getting the distance of the first pixel from top margin
    adjustmentInYdirection = xCoordinate_side_view[0]- xCoordinate[yCoordinate.index(sortedYcoordinates[0])]
    #Showing the sideview of image
    cv2.imshow('side_view', img_side_view1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    colors = vtk.vtkNamedColors()

    # Defining the points
    points = vtk.vtkPoints()
    idx = 0
    for x in range(len(xCoordinate)):
        points.InsertNextPoint(yCoordinate[x], -xCoordinate[x], 0)
        idx += 1
    #adding points in the polydata
    polydata = vtk.vtkPolyData()
    polydata.SetPoints(points)

    # Create anything you want here, we will use a cube for the demo.
    cubeSource = vtk.vtkCubeSource()
    cubeSource.SetZLength(20.0)

    #assigning the cubesorce in the glyph
    glyph3D = vtk.vtkGlyph3D()
    glyph3D.SetSourceConnection(cubeSource.GetOutputPort())
    glyph3D.SetInputData(polydata)
    glyph3D.Update()

    # storing all the pixel information in the side view
    points1 = vtk.vtkPoints()
    idx = 0
    for x in range(len(xCoordinate_side_view)):
        points1.InsertNextPoint(sortedYcoordinates[0], -xCoordinate_side_view[x]+adjustmentInYdirection ,
                                yCoordinate_side_view[x] -ycoordinateTemp[0])
        idx += 1
    #Creating polydata for sideview
    polydata1 = vtk.vtkPolyData()
    polydata1.SetPoints(points1)

    # Create anything you want here, we will use a cube for the demo.
    cubeSource1 = vtk.vtkCubeSource()
    cubeSource1.SetXLength(20.0)
    #Glyph for sideview
    glyph3D1 = vtk.vtkGlyph3D()
    glyph3D1.SetSourceConnection(cubeSource1.GetOutputPort())
    glyph3D1.SetInputData(polydata1)
    glyph3D1.Update()

    # copying information from the same handle to generate the other handle of the sunglass
    points2 = vtk.vtkPoints()
    idx = 0
    for x in range(len(xCoordinate_side_view)):
        points2.InsertNextPoint(sortedYcoordinates[-1] - cubeSource1.GetXLength() / 2,
                                -xCoordinate_side_view[x] + adjustmentInYdirection,
                                yCoordinate_side_view[x]-ycoordinateTemp[0])
        idx += 1

    #Creating polydata for the remaining handle
    polydata2 = vtk.vtkPolyData()
    polydata2.SetPoints(points2)
    glyph3D2 = vtk.vtkGlyph3D()
    glyph3D2.SetSourceConnection(cubeSource1.GetOutputPort())
    glyph3D2.SetInputData(polydata2)
    glyph3D2.Update()

    # Adding mapper for the distinct three polydatas
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(glyph3D.GetOutputPort())
    mapper1 = vtk.vtkPolyDataMapper()
    mapper1.SetInputConnection(glyph3D1.GetOutputPort())
    mapper2 = vtk.vtkPolyDataMapper()
    mapper2.SetInputConnection(glyph3D2.GetOutputPort())

    #Defining actors for the three mappers separately
    actor = vtk.vtkActor()
    actor.GetProperty().SetColor(colors.GetColor3d("alizarin_crimson"))
    actor.SetMapper(mapper)
    actor1 = vtk.vtkActor()
    #actor1.GetProperty().SetColor(colors.GetColor3d("midnight_blue"))
    actor1.SetMapper(mapper1)
    actor2 = vtk.vtkActor()
    actor2.GetProperty().SetColor(colors.GetColor3d("MistyRose"))
    actor2.SetMapper(mapper2)

    #Grouping the three parts and scaling so that it is usable in unity3D or other 3D application
    assembly = vtk.vtkAssembly()
    assembly.AddPart(actor)
    assembly.AddPart(actor1)
    assembly.AddPart(actor2)
    assembly.SetScale(.01,.01,.01)

    #We tried to reduce the size of mesh, apparently it does not work without triangulated surface
    inputPoly = vtk.vtkPolyData()
    inputPoly.ShallowCopy(glyph3D.GetOutput())
    print("Before decimation\n"
          "-----------------\n"
          "There are " + str(inputPoly.GetNumberOfPoints()) + "points.\n"
                                                              "There are " + str(
        inputPoly.GetNumberOfPolys()) + "polygons.\n")
    decimate = vtk.vtkDecimatePro()
    decimate.SetInputData(inputPoly)
    decimate.SetTargetReduction(.10)
    decimate.Update()
    decimatedPoly = vtk.vtkPolyData()
    decimatedPoly.ShallowCopy(decimate.GetOutput())
    print("After decimation \n"
          "-----------------\n"
          "There are " + str(decimatedPoly.GetNumberOfPoints()) + "points.\n"
                                                                  "There are " + str(
        decimatedPoly.GetNumberOfPolys()) + "polygons.\n")

    # Set object properties
    prop = actor.GetProperty()
    prop.SetInterpolationToPhong()  # Set shading to Phong
    prop.ShadingOn()
    # prop.SetColor(0, 15, 26)
    prop.SetDiffuse(0.8)  # 0.8
    prop.SetAmbient(0.3)  # 0.3
    prop.SetSpecular(1.0)  # 1.0
    prop.SetSpecularPower(100.0)  # 100.0

    # Set object properties
    prop = actor1.GetProperty()
    prop.SetInterpolationToPhong()  # Set shading to Phong
    prop.ShadingOn()
    # prop.SetColor(0, 51, 0)
    prop.SetDiffuse(0.8)  # 0.8
    prop.SetAmbient(0.3)  # 0.3
    prop.SetSpecular(1.0)  # 1.0
    prop.SetSpecularPower(100.0)  # 100.0

    # Set object properties
    prop = actor2.GetProperty()
    prop.SetInterpolationToPhong()  # Set shading to Phong
    prop.ShadingOn()
    # prop.SetColor(1, 1, 0)
    prop.SetDiffuse(0.8)  # 0.8
    prop.SetAmbient(0.3)  # 0.3
    prop.SetSpecular(1.0)  # 1.0
    prop.SetSpecularPower(100.0)  # 100.0

    # Define light
    light = vtk.vtkLight()
    light.SetLightTypeToSceneLight()
    light.SetAmbientColor(1, 1, 1)
    light.SetDiffuseColor(1, 1, 1)
    light.SetSpecularColor(1, 1, 1)
    light.SetPosition(-100, 100, 25)
    light.SetFocalPoint(0, 0, 0)
    light.SetIntensity(1.0)  # 0.8

    # Define light
    light1 = vtk.vtkLight()
    light1.SetLightTypeToSceneLight()
    light1.SetAmbientColor(1, 1, 1)
    light1.SetDiffuseColor(1, 1, 1)
    light1.SetSpecularColor(1, 1, 1)
    light1.SetPosition(100, -100, -25)
    light1.SetFocalPoint(0, 0, 0)
    light1.SetIntensity(1.0)

    renderer = vtk.vtkRenderer()
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.SetSize(700, 700)
    renderWindow.AddRenderer(renderer)
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)

    renderer.AddActor(actor)
    renderer.AddLight(light)
    renderer.AddLight(light1)
    renderer.AddActor(actor1)
    renderer.AddLight(light)
    renderer.AddActor(actor2)
    renderer.AddLight(light)
    renderer.SetBackground(colors.GetColor3d("slate_grey_light"))
    #Write the Obj file to disk
    objWriter = vtk.vtkOBJExporter()
    objWriter.SetFilePrefix("glass")
    objWriter.SetRenderWindow(renderWindow)
    objWriter.SetInputConnection(renderer)
    objWriter.Write()
    renderWindow.Render()
    renderWindowInteractor.Start()


if __name__ == '__main__':
    main()