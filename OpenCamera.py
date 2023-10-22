# importing the python open cv library
import cv2

# intialize the webcam and pass a constant which is 0
cam = cv2.VideoCapture(0)

# title of the app
cv2.namedWindow('python webcam screenshot app')

#0 images collected initially
img_counter = 0

# while loop
while True:
    # initializing the frame, ret
    ret, frame = cam.read()
    # if statement
    if not ret:
        print('failed to grab frame')
        break
    # the frame will show with the title of test
    cv2.imshow('test', frame)
    #get continuous live video feed from laptops webcam
    k  = cv2.waitKey(1)
    # if the escape key is been pressed, the app will stop
    if k%256 == 27:
        print('escape hit, closing the app')
        break
    # if the space bar key is pressed take screenshot
    elif k%256  == 32:
        # the format for storing the images
        img_name = f'opencv_frame_{img_counter}'
        # saves the image as a png file
        cv2.imwrite(img_name + ".png", frame)
        print('screenshot taken')
        # the number of images automatically increases by 1
        img_counter += 1

# release the camera
cam.release()

# stops the camera window
cam.destoryAllWindows()