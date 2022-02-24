# Double3SDK
See [double3sdk/README.md](double3sdk/README.md).

# winter2021_recognition
Git Submodule of [winter2021_recognition](https://github.com/junghyuncho/winter2021_recognition).  
```bash
git submodule init # just in the beginning

git submodule update --remote # fetch and update submodule
```
See [winter2021_recognition/README.md](winter2021_recognition/README.md).

# App
OpenCV based app
## Installiation
### Python `3.10.0`
```bash
pip install -r requirements.txt
```
### Opencv
> ### **UPDATE**  
> We use **USB WEBCAM** due to jetson-camera error.  
> If jetson-camera error is fixed, call `self.use_jetson()` in `Camera.set()`

We need to build opencv manually to use Nvidia Jetson TX2
See [install-opencv.md](install-opencv.md).

If you are not going to use the Nvidia Jetson camera, you can install opencv more easily.
```bash
pip install opencv-python==4.5.5.62
```
## Run
```bash
bash run.sh
```