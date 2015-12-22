Title: Write a python script to define the detecting region by clicking and dragging mouse
Date: 2015-09-30
Tags: cv, python
Category: Machine learning


In object tracking, usually,
we need to define a rectangular box which contains the object of interest and obtain the box information as follows.

{% img https://farm1.staticflickr.com/565/21640517650_2ae383659d_z.jpg %}

```
Box: (80, 86, 263, 312)
```
where (80, 86) is the upper-left point of box.
The 263 and 312 are the width and height, respectively.

And this work can be done by writing a simple script (named `tk-detect-box`) as below.

tk-detect-box:

    :::python
    #!/usr/local/bin/python3

    import cv2
    import argparse
    import os


    class Rect:
        def __init__(self, x, y, width, height):
            self.x = x
            self.y = x
            self.width  = width
            self.height = height

    def detect_box(image, win_name="window (hit q to exit)"):
        # Return a box for detection

        box_defined = False
        box = Rect(0, 0, 0, 0)
        def define_box(event, x, y, flags, param):

            nonlocal box_defined, box
            if event == cv2.EVENT_LBUTTONDOWN:
                box_defined = False
                box.x = x
                box.y = y
                box.width  = 0
                box.height = 0

            if event == cv2.EVENT_MOUSEMOVE:
                if not box_defined:
                    box.width  = x - box.x
                    box.height = y - box.y

            if event == cv2.EVENT_LBUTTONUP:
                box_defined = True

        def do_nothing(event, x, y, flags, param):
            pass

        # set mouse callback
        cv2.setMouseCallback(win_name, define_box)

        while True:
            # display the frame from video capture
            clone = image.copy()
            if box.x > 0 and box.width > 0:
                # Starting and ending point of the rectangle
                p0 = (box.x, box.y)
                p1 = (box.x + box.width, box.y + box.height)
                cv2.rectangle(clone, p0, p1, (0, 255, 0), thickness=2)

            cv2.imshow(win_name, clone)

            if (cv2.waitKey(1) & 0xFF) == ord('q'): # Hit `q` to exit
                break

        # Set a mouse callback which does nothing
        cv2.setMouseCallback(win_name, do_nothing)

        return box


    # Construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True, help="image path.")
    args = vars(ap.parse_args())

    # Arguments
    image_path = args['image']

    # Determine the width and height from the first image
    image = cv2.imread(image_path)

    # Create a window
    win_name = 'window (hit q to exit)'
    cv2.namedWindow(win_name)

    # Define the detecting box
    box = detect_box(image, win_name)

    # Output box information
    print("Box: ({}, {}, {}, {}) ".format(box.x, box.y, box.width, box.height))

    cv2.destroyAllWindows()
    {% endcodeblock %}

The usage of this script is like
```
tk-detect-box -i girl.png
```
It will open the image and let you define a rectangular box by clicking and dragging the mouse.
After hitting `q` and it will show out the box information.
