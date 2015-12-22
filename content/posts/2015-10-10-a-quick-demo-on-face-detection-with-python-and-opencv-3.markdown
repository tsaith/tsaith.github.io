Title: A quick demo on face detection with python 3 and opencv 3
Date: 2015-10-10
Tags: cv, python
Category: Machine learning


Here, I record how to write a simple code for face detection with Harr-like features, which is based on python 3 and opencv 3.
The script `face_detector_haar.py` below is just slightly modified from the [post](https://realpython.com/blog/python/face-recognition-with-python/) written by Shantnu Tiwari.

face_detector_haar.py:

    :::python
    import cv2 # OpenCV
    import sys

    # Input image
    image_path = sys.argv[1]

    # Model parameters
    dir_path = "/usr/local/Cellar/opencv3/3.0.0/share/OpenCV/haarcascades" # Please modify this for your environment
    filename = "haarcascade_frontalface_default.xml" # for frontal faces
    #filename = "haarcascade_profileface.xml" # for profile faces
    model_path = dir_path + "/" + filename

    # Create the classifier
    clf = cv2.CascadeClassifier(model_path)

    # Read the image
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces on image
    faces = clf.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    print("Found {0} faces!".format(len(faces)))

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv2.imshow("Faces found", image)
    cv2.waitKey(0)


Please make sure the `model_path`  in code is correctly set when considering your OpenCV environment.
The `haarcascade_frontalface_default.xml` and `haarcascade_profileface.xml` are the model files of frontal and profile face detection, respectively.

To execute the script:
```
python3 face_detector_haar.py photo.jpg
```

Some results are demonstrated as following.

{% img https://farm1.staticflickr.com/626/21558529013_489118d07d_z.jpg %}

{% img https://farm6.staticflickr.com/5740/22189822451_d32dd51a35_z.jpg %}

{% img https://farm1.staticflickr.com/639/22189825981_0a76874f9e_z.jpg %}
