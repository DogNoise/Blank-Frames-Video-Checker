# Black frames video checker

This simple python tool was created to get rid of annoying problem with QC of rendered videos. 

It is very common problem (especially with Adobe Premire Pro) to sometimes insert black frames into renders due to render error. Those problems accure randomly, and user is not notified about it. 


Examples:
- [Exporting Black Video](https://community.adobe.com/t5/premiere-pro-discussions/exporting-black-video/td-p/10196335)  - Premire Por forum
- [Random Black frams or dropped frames](https://community.adobe.com/t5/premiere-pro-discussions/random-black-frams-or-dropped-frames/td-p/13481017) - Premire Por forum
- [Random black frames in Premiere Pro](https://community.adobe.com/t5/premiere-pro-discussions/random-black-frames-in-premiere-pro/td-p/13095455) - Premire Por forum


I wrote this code a while ago. It's maily designed to run on windows as this problem appers mainly on those devices. It's a great tool that will save you a lof of time. Just run your finished renders through this program before sending to client, to see if it rendered sucessfully. 


## Install
Before running this script please check if you have those libraries. You can install them using pip.

#### PySimpleGUI
```python
pip install PySimpleGUI
```
#### MoviePy
```python
pip install moviepy
```

