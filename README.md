# Face-Recognition-with-Real-Time-Database
This project is a real-time face recognition and attendance system. using computer vision to detect and recognize faces in a live video stream. The system compares the detected faces with a pre-trained set of known faces using face recognition algorithms. Upon successful recognition, it retrieves the corresponding information of the recognized person from a Firebase database.


https://github.com/MohamedMamdouh99/Face-Recognition-with-Real-Time-Database/assets/88439119/d7e366da-ed29-44d9-89f3-965ad06b3949


The project incorporates various technologies and libraries, including OpenCV for video capture and image processing, face_recognition for face detection and recognition, Firebase for real-time database management and storage, and numpy for array manipulation. It also uses pickle for serialization to load the pre-trained face encodings.

The system displays a graphical user interface that overlays attendance-related information on the video stream. It shows the recognized person's name, department, ID, standing, year, and starting year. Additionally, it tracks the total number of days attended and updates the attendance record in the Firebase database.
