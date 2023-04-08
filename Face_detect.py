# Importing Libraries
import cv2
import face_recognition
import glob
import math
import os
import datetime
import numpy as np
import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import messagebox

root = tk.Tk()
root.config(bg="SpringGreen2")
Title = root.title("Video Analysis")
root.geometry('661x300')
root.resizable(0, 0)


def rootwindow():
    path = PathTextBox.get('1.0', 'end-1c')
    # Take video and store its frames in a folder
    count = 0
    frames = 0
    cap = cv2.VideoCapture(path)  # capturing the video from the given path
    frameRate = cap.get(5)  # frame rate

    # Give full path name where 
    cwd = os.getcwd()
    path = os.path.join(cwd,"Frames")
    # path1 = r'C:\\Users\\anant\\Downloads\\Video-Analysis-Using-OpenCV-main\\Video-Analysis-Using-OpenCV-main\\Frames'
    path1 = r' + path + '

    while cap.isOpened():
        frameId = cap.get(1)  # current frame number
        ret, frame = cap.read()
        if not ret:
            break
        if frameId % math.floor(frameRate) == 0:
            filename = "frame%d.jpg" % count
            count += 1
            cv2.imwrite(os.path.join(path1, filename), frame)
    cap.release()

    # Input Image
    input_image = face_recognition.load_image_file('Elon_Musk_2015.jpg')
    input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)

    # Input Image Face Recognition and encoding
    faceLoc = face_recognition.face_locations(input_image)
    encode_input = face_recognition.face_encodings(input_image)
    for face_Loc in faceLoc:
        y11, x22, y22, x11 = face_Loc
        cv2.rectangle(input_image, (x11, y11), (x22, y22), (0, 255, 0), 2)

    # Iterating over Different Frames of video
    # images = glob.glob(r'C:\Users\visha\Desktop\Mini Project\Frames\*.jpg')
    # images = glob.glob(r'C:\\Users\\anant\\Downloads\\Video-Analysis-Using-OpenCV-main\\Video-Analysis-Using-OpenCV-main\\Frames\\*.jpg')
    cwd = os.getcwd()
    path = os.path.join(cwd,"Frames", '*.jpg')
    images = glob.glob(r'+ path + ')
    for img in images:
        # Reading Different Frames
        input_test = face_recognition.load_image_file(img)
        input_test = cv2.cvtColor(input_test, cv2.COLOR_BGR2RGB)
        # Frames face location recognition and encoding
        face_test = face_recognition.face_locations(input_test)
        encode_test = face_recognition.face_encodings(input_test, face_test)

        for encode_face, face_location in zip(encode_test, face_test):
            matches = face_recognition.compare_faces(encode_face, encode_input)
            faceDis = face_recognition.face_distance(encode_input, encode_face)
            matchIndex = np.nanargmin(faceDis)
            if matches[matchIndex]:
                frames = frames + 1
            if matches[0] == False:
                # face_detect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
                face_detect = cv2.CascadeClassifier('C:\\Python310\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml')
                face_data = face_detect.detectMultiScale(input_test, 1.3, 5)
                y1, x2, y2, x1 = face_location
                cv2.rectangle(input_test, (x1, y1), (x2, y2), (0, 255, 0), 2)
                roi = input_test[y1:y2, x1:x2]
                roi = cv2.GaussianBlur(roi, (23, 23), 30)
                input_test[y1:y1 + roi.shape[0], x1:x1 + roi.shape[1]] = roi
                cv2.imshow("Frame", input_test)
                cv2.waitKey(0)
    sec = int(frames - 1)
    seconds = "Duration in seconds : " + str(sec)
    dwell = "Video time : " + str(datetime.timedelta(seconds=sec))
    new_Window = tk.Toplevel(root)
    new_Window.geometry('300x100')
    new_Window.config(bg="SpringGreen2")
    new_Window.title('Result')
    new_Window.resizable(0, 0)
    label_1 = Label(new_Window, text=seconds)
    label_1.place(x=150, y=30, anchor=CENTER)
    label_2 = Label(new_Window, text=dwell)
    label_2.place(x=150, y=65, anchor=CENTER)


def openfile():
    name = askopenfilename(initialdir="/",
                           filetypes=[("Mp4 Files", "*.mp4")],
                           title="Choose a file."
                           )
    PathTextBox.delete("1.0", END)
    PathTextBox.insert(END, name)


# Capture Image from webcam
def open_webcam():
    webcam = cv2.VideoCapture(0)
    while True:
        try:
            check, frame = webcam.read()
            cv2.imshow("Capturing", frame)
            key = cv2.waitKey(1)
            if key == ord('s'):
                cv2.imwrite(filename='saved_img.jpg', img=frame)
                webcam.release()
                img_new = cv2.imread('saved_img.jpg', cv2.IMREAD_GRAYSCALE)
                # img_new = cv2.imshow("Captured Image", img_new)
                cv2.waitKey(1650)
                cv2.destroyAllWindows()
                img_ = cv2.imread('saved_img.jpg', cv2.IMREAD_ANYCOLOR)
                gray = cv2.cvtColor(img_, cv2.COLOR_BGR2GRAY)
                img_ = cv2.resize(gray, (28, 28))
                # img_resized = cv2.imwrite(filename='saved_img-final.jpg', img=img_)
                break
            elif key == ord('q'):
                print("Turning off camera.")
                webcam.release()
                print("Camera off.")
                cv2.destroyAllWindows()
                break
        except KeyboardInterrupt:
            print("Turning off camera.")
            webcam.release()
            print("Camera off.")
            print("Program ended.")
            cv2.destroyAllWindows()
            break


# Delete all older frames
def delete():
    # directory = r'C:\Users\visha\Desktop\Mini Project/Frames'
    directory = r'C:\\Users\\anant\\Downloads\\Video-Analysis-Using-OpenCV-main\\Video-Analysis-Using-OpenCV-main\\Frames'
    files_in_directory = os.listdir(directory)
    filtered_files = [file for file in files_in_directory if file.endswith(".jpg")]
    for file in filtered_files:
        path_to_file = os.path.join(directory, file)
        os.remove(path_to_file)


def confirmation():
    MsgBox = tk.messagebox.askquestion('Exit Application', 'Are you sure you want to exit the application',
                                       icon='warning')
    if MsgBox == 'yes':
        root.destroy()
    else:
        tk.messagebox.showinfo('Return', 'You will now return to the application screen')


label1 = Label(root, text=" Video Analysis Using OpenCV ", background='springgreen4', foreground="white",
               font=("Comic Sans MS", 15), anchor=N)
label1.place(x=330, y=23, anchor=CENTER)

refresh = Button(root, text=" Refresh ", command=delete, bg="springgreen4", fg='white', font=("Comic Sans MS", 10),
                 borderwidth=0, relief="sunken")
refresh.place(x=587, y=110)

PathTextBox = Text(root, height=2, borderwidth=0, font=("Comic Sans MS", 10), relief="sunken")
PathTextBox.place(x=10, y=150)

Webcam = Button(root, text=" Open WebCam ", command=open_webcam, bg='springgreen4', fg='white',
                font=("Comic Sans MS", 10), borderwidth=0, relief="sunken")
Webcam.place(x=135, y=77)

Video_upload = Button(root, text=" Browse video ", command=openfile, bg='springgreen4', fg='white',
                      font=("Comic Sans MS", 10), borderwidth=0, relief="sunken")
Video_upload.place(x=135, y=112)

PathLabel = Label(root, text=" Upload Image : ", font=("Comic Sans MS", 10))
PathLabel.place(x=10, y=80)

PathLabel1 = Label(root, text=" Upload Video : ", font=("Comic Sans MS", 10))
PathLabel1.place(x=10, y=115)

ReadButton = Button(root, text=" Submit ", command=rootwindow, bg='springgreen4', fg='white',
                    font=("Comic Sans MS", 13), borderwidth=0, relief="sunken")
ReadButton.place(x=286, y=200)

exitbutton = Button(root, text=" Exit ", command=confirmation, bg="springgreen4", fg='white',
                    font=("Comic Sans MS", 13), borderwidth=0, relief="sunken")
exitbutton.place(x=298, y=250)

root.mainloop()
