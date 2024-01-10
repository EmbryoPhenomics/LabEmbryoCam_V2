# LabEmbryoCam User Guide

<img src="assets/LEC_render.png"  width="80%">

#### ***An opensource platform for automated measurement of developing animals. The LabEmbryoCam is a project originating with the EmbryoPhenomics research group at the University of Plymouth, UK. It has been made possible by support from UKRI, NERC, BBSRC and Plymouth Science Park.***




-----------------
### INDEX
-----------------
* **1. Hardware setup**
* **2. Starting the webserver**
* **3. Homing the motorised XYZ stage**
* **4. Setting up camera and starting live stream**
* **5. Using manual controls to find and save desired positions**
* **6. Set acquisition parameters and start acquisition**
-----------------



***If you are using LabEmbryoCam, please consider joining the Google Group https://groups.google.com/g/labembryocam. Doing so will help contribute to the advancement of this opensource project, including staying up-to date with updates and receiving support.***





-----------------
### 1. HARDWARE SETUP
-----------------
The LEC is a versatile multidimensional imaging platform. A broad range of magnifications are possible, using different optical hardware, particularly lenses. 

The distance between the sample and the lens will depend on the magnification and lens characteristics. Similarly, the optimum distance between the sample and the light will depend on the optical hardware, magnification, but also the sample type.

The LEC was initially developed for dark field imaging of developing aquatic embryos. Dark field imaging, in which a black background is achieved via lighting arriving at the sample from an oblique angle, works well for imaging developing embryos.










-----------------
### 2. USER INTERFACE
-----------------

Once you have powered on your system, you can start the LabEmbryoCam (LEC) user interface by double clicking the icon on the desktop or in the Activities panel:

<img src="assets/starting-webserver.png"  width="80%">

A terminal window will automatically open followed by the browser with the webserver (user interface) loaded. We can now proceed with getting the hardware set up for running an experiment. When the LEC user interface first loads, it connects to the various hardware components automatically - give it a few seconds before interacting with it to allow this process to complete.

<img src="assets/global-ui.png"  width="80%">

The LEC user interface is divded into a number of setctions
* A) **Experiment Settings** - for loading a configuration file to repopulate previously used settings.
* B) **Camera View** - for adjusting the camera, streaming the camera feed, and snaping still images.
* C) **XYZ controls and settings** - for homing the XYZ stage, and moving the optics carriage around.
* D) **XYZ Positions** - for populating a list of XYZ positions.
* E) **XYZ View** - for interacting with XYZ positions, and automatically generating positions for wells of multiwell plates.
* F) **Experiment setup** - for configuring and running experiments - either at a single positon, or multiple.
* G) **Experiment Progress** - for monitoring the progress of an experiment.


-----------------
### 3. XYZ controls and settings
-----------------
The first step required in setting up any experiment with the LEC is to home, or 'Set Origin' the XYZ stage. This is essential to ensure that the correct origin is used when finding and creating positions and without doing this the XYZ stage will not be responsive. 

To home the stage, click the `Set Origin` button in the user interface.

***Before homing the stage, make sure there are no objects that could obstruct the movement of the stage - such as the lens being too high. Also, make sure not to use the app whilst the stage is homing as this could interfere with the process.***

<img src="assets/homing.png"  width="80%">










-----------------
### 4. CAMERA VIEW
-----------------
Camera and lighting settings will need adjusting to suit your experimental system - species, study aim etc.  

Adjusting the camera and lighting settings can simply be achieved using the `Camera View` section of the user interface: 

<img src="assets/cam-setup.png"  width="80%">

Begin by choosing a resolution - 720 x 1080 is a good compromise between speed (i.e. maximum frame rate) and resolution, and clicking 'Update'.

A live stream can be initialised using 'Start/Stop Stream' - and a rotating cursor next to the button will indicate that the camera is running.

Use the live display to ascertain what changes, if any, may be required.

You can then use the three buttons - LED, Exposure and Frame-rate, to make adjustments as required. However, changes to the camera's - exposure, frame rate, and resolution, should only be made when the 'Start/Stop Stream is deactivated. **Changes are only implemented when clicking 'Update'.**

The following are descriptions for each of the settings in the Camera View.
* **LED**: The percentage brightness of the LED ring light. Note that the lighting can also be adjusted by using the lighting mount up and down, and by screwing/unscrewing the darkfield adapter. The LED will by default go to sleep when not needed during an experiment.
* **Exposure**: The shutter speed at which the camera operates in milliseconds - 20 ms is a good starting point.
* **Frame-rate**: The frame-rate at which videos are captured. Note that for high resolutions, such as 2048x2048, you will need to reduce exposure time below 10ms if you would like to achieve a frame-rate higher than 15-20fps. 
* **Resolution**: Presets for resolution at which images will be captured.

***For changes to the camera settings to take effect you must press the `Update` button at the bottom of the Camera Settings section.***

**Note**
There are two physical adjustable parameters on the lens itself, the iris and the magnification. The upper adjustment ring is for adjusting the magnification and the lower adjustment ring is for adjusting the iris. If you change the magnification, the required distance between the sample in the multiwell plate and the lens will need to be changed as well - higher magnification requires the lens to be closer to the sample, it will also result in a darker image and perhaps even a requirement for more light (either by choosing a longer exposure, increasing the brightness of the LED, or adjusting the physical position of the light). Finally, by opening or closing the iris, the depth of field (i.e. depth of the sample that is in focus) can be adjusted. Typically greater depth of field is very welcome, but it comes at the cost of a darker image. So, a compromise is required and will need to be decided on a case-by-case basis.

Next to the 'Start/Stop Stream' button in the Camera View, is a 'Snap' button. This allows you to capture images dynamically while using the instrument. They are automatically saved in a 'snap-images' folder in the LEC application folder.

Still images are interactive, so you can zoom in and out, and move the image to find an improved view. Before starting the next step, you may wish to start the live video stream, if you haven't already, for easily finding the animals or subjects you wish to record using the LEC.

***If you would like to change the camera settings you must exit the live stream before doing this so that your changes can take effect. Then when you have finished choosing your desired setttings, press the `Update` button before starting the live stream again.***







-----------------
### 5. USING MANUAL CONTROLS TO FIND AND SAVE POSITIONS
-----------------

The manual controls can be used once the stage has finished homing. These can be found in **XYZ controls and settings**:

<img src="assets/xyz-ctrl.png"  width="80%">

The four buttons determine the step size of the movements of the XYZ stage - from 10mm to 0.01mm. Large movements are more easily achieved with a 10 mm step size, whereas smaller movements require a smaller step size. The stage will complete one 'step' for each press of the relevant button.

In conjunction with the camera live video stream, move the stage using the manual controls to move the camera to a desired position. Once you have a position that you want, click the `Current` button in the xyz section to record the current position:

<img src="assets/xyz-all.png"  width="80%">

This will add a position entry into the position list. Note that all columns and rows in the table are editable - so you can give the position a name/label.

You can repeat this step until you have recorded all the positions you want. Once you have completed recording positions, the next step is to enter the parameters for the acquisition before starting the experiment. 

The following are descriptions for each of the controls and components in the XYZ controls and settings section of the user interface:

* **Set Origin**: Press this button to home the stage at startup of the user interface
* **Left group of arrows**: These arrows correspond to moving the stage in the X and Y axis, you can move the stage forward (down arrow), backward (up arrow), left and right, but also diagonally.
* **Right group of arrows**: These arrows move the stage up and down in the Z axis.

The **XYZ View** section will populate with the relative positions of the XYZ positions that you record. If you click the toggle switch **Activate graph** this will mean that positions clicked on in this window will move the stage to that position. This is an effective way of quickly reviewing and adjusting positions.

* **Activate graph**: Enabling this switch will allow you to click on positions on the graph and then the stage will move to the select position. This can be an easy way to double-check all your positions are correct whilst you have a live stream open.

Additionally, the other settings in the **XYZ View** are:
* **Dimension**: Enabling this switch can switch between 2D or 3D view in the position plot, 3D view can be useful for visualising the z axis positions (i.e. seeing the relative heights of different positions).
* **Generate XY**: This enables the automatic creation of the entirity of a multiwell plate's positions. This is deactivated, unless you first create a position (using the **XYZ Positions** section - see below) labelled A1 (corresponding to the top left corner of a multiwell plate. Once this is done, the **Generate XY** will use this position as the basis to create X and Y coordinates for all subsequent wells. 24, 48, 96 and 384 well plates are included.
  
The **XYZ Positions** section enables creation of X, Y and Z position lists:

* **Current**: Press this button to retrieve the coordinates of the current position where the stage is at. A new entry will be added into the position list below where it can be edited further.
* **Replace**: Press this button to replace the coordinates of the selected position with those at the current position of the stage. This can be used to update a position if an animal has moved or gone out of focus. **Note that you must select a position in the position list table via clicking on the circle icon in the second column of the position list for the position you’d like to replace.**
* **Position list table**: Position list where coordinates are recorded. The first column is for removing position entries from the list, simply click the x icon for the position you’d like to remove. The second column is to permit selection of specific position entries for updating their coordinates. Finally, columns X, Y, Z and Label are all editable similar to an excel spreadsheet.








-----------------
### 6. SETTING AND STARTING ACQUISITIONS
-----------------

The acquisition parameters can be found at the bottom of the page of the user interface in the Acquisition section:

<img src="assets/expt-setup.png"  width="80%">

Here are descriptions for each acquisition parameter:
* **Number of positions**: Whether you would like to capture footage for only the current position (‘Single’) or all the XYZ positions you have recorded (‘Multiple’).
* **Number of timepoints**: How many acquisition iterations you would like the system to complete. An iteration consists of capturing footage for the specified positions. Setting the acquisition interval allows us to set this process to complete every X minutes, where X would be the acquisition interval.
* **Acquisition interval**: How long to wait between each timepoint in minutes - you must consider how long it will take for each acquisition to complete, or risk the previous acquisition not finishing before the next starts.
* **Acquisition length**: How long to acquire video for each position, at each timepoint.
* **Driver and Folder selection**: The full file path to the directory where you would like to save video. This should be selected using the Select button and navigating the browser that pops up.

Once you have added in your desired acquisition parameters, you can now start an acquisition using the Start acquisition button!

Progress of the experiemtn will be shown at the bottom of the user interface in the 'Experiment Progress' section. This enables tracking the progress of an experiment.


<img src="assets/expt-progress.png"  width="80%">




