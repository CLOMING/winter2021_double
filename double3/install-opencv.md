# Install Opencv on Jetson TX2

## Reference
- https://jkjung-avt.github.io/opencv3-on-tx2/
- https://mickael-k.tistory.com/46
- https://github.com/doublerobotics/d3-sdk/blob/master/docs/USB%20Drive.md
- https://stackoverflow.com/a/58088989

## Installation Steps

With python3 on Jetson TX2, `pip install cv2` and `import cv2` cannot access for Jetson TX2 On-board camera.  
We have to recompile OpenCV with Gstreamer.

However, due to fewer free space of Double3 - only 1 GB free - we must use USB Drive. See [document of DoubleRobitics](https://github.com/doublerobotics/d3-sdk/blob/master/docs/USB%20Drive.md)

### 1. Remove all old Opencv stuffs
```bash
sudo apt-get purge libopencv*
```
```bash
sudo apt-get purge python-numpy
```
```bash
sudo apt autoremove
```
### 2. Install dependencies based on the Jetson Installing OpenCV Guide
```bash
sudo apt-get install build-essential make cmake cmake-curses-gui g++ libavformat-dev libavutil-dev libswscale-dev libv4l-dev libeigen3-dev libglew-dev libgtk2.0-dev
```

### 3. Install dependencies for gstreamer stuffs
```bash
sudo apt-get install libdc1394-22-dev libxine2-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev
```

### 4. Install additional dependencies according to the pyimageresearch
```bash
sudo apt-get install libjpeg8-dev libjpeg-turbo8-dev libtiff5-dev libjasper-dev libpng12-dev libavcodec-dev
```
```bash
sudo apt-get install libxvidcore-dev libx264-dev libgtk-3-dev libatlas-base-dev gfortran
```
```bash
sudo apt-get install libopenblas-dev liblapack-dev liblapacke-dev
```
### 5. Install Qt5 dependencies
```bash
sudo apt-get install qt5-default
```

### 6. Install Python3
We use python installed by pyenv
```bash
pip install numpy
```
```bash
pip install matplotlib
```

### 7. Modify matplotlibrc
Open `~/.pyenv/versions/3.10.0/lib/python3.10/site-packages/matplotlib/mpl-data/matplotlibrc`.  
Modify 81L to `backend         : TkAgg`.  

### 8. Build Opencv
Change directory that USB mounted
```bash
cd /media/usbstick/
```
Make workspace
```bash
mkdir src && cd src
```
Download Opencv and Unzip
```bash
wget https://github.com/opencv/opencv/archive/3.4.0.zip -O opencv-3.4.0.zip
```
```bash
unzip opencv-3.4.0.zip
```
Build  OpenCV
```bash
mkdir build && cd build
```
```bash
cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D WITH_CUDA=ON -D CUDA_ARCH_BIN="6.2" -D CUDA_ARCH_PTX="" -D WITH_CUBLAS=ON -D ENABLE_FAST_MATH=ON -D CUDA_FAST_MATH=ON -D ENABLE_NEON=ON -D WITH_LIBV4L=ON -D BUILD_TESTS=OFF -D BUILD_PERF_TESTS=OFF -D BUILD_EXAMPLES=OFF -D WITH_QT=ON -D WITH_OPENGL=ON -D PYTHON3_INCLUDE_DIR= /root/.pyenv/versions/3.10.0/include/python3.10 -D PYTHON3_NUMPY_INCLUDE_DIRS=/root/.pyenv/versions/3.10.0/lib/python3.10/site-packages/numpy/core/include/ -D PYTHON3_PACKAGES_PATH=/root/.pyenv/versions/3.10.0/lib/python3.10/site-packages -D PYTHON3_LIBRARY=/root/.pyenv/versions/3.10.0/lib/libpython3.10.a -D PYTHON_DEFAULT_EXECUTABLE=$(which python3) ..
```
```bash
make -j4
```
If following error occured in 100%, See https://stackoverflow.com/a/58088989
```
/home/pi/opencv-3.3.0/modules/python/src2/cv2.cpp: In function ‘bool pyopencv_to(PyObject*, T&, const char*) [with T = cv::String; PyObject = _object]’:/home/pi/opencv-3.3.0/modules/python/src2/cv2.cpp:854:34: error: invalid conversion from ‘const char*’ to ‘char*’ [-fpermissive] char* str = PyString_AsString(obj);In file included from /home/pi/opencv-3.3.0/modules/python/src2/cv2.c
```

```bash
sudo make install
```

### 9.Check Installation
```bash
python -c "import cv2; print(cv2.__version__)"
# 3.4.0
```