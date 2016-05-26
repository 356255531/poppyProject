# Before Start
+ Official Project Web:  
https://www.poppy-project.org/creatures/get-started-with-poppy/
+ Official Documentation of Poppy Project:  
http://docs.poppy-project.org/en/getting-started/  
+ Poppy Forum:  
https://forum.poppy-project.org/
+ Poppy Head Assembly:  
https://github.com/poppy-project/poppy-humanoid/blob/master/hardware/doc/en/head_assembly.md

# Program IDE
The program will ideally done in jupyter notebook. It's more convenient to write and test code in block and you can also add description in it.  
+ You can find a useful tutorial about how to install and use it at the link below:  
http://jupyter-notebook-beginner-guide.readthedocs.io/en/latest/

# V-rep Short Guideline
+ You can find an interesting toturial under the given link:  
https://github.com/poppy-project/community-notebooks/blob/master/demo/poppy-humanoid_Controlling%20in%20V-REP%20using%20pypot.ipynb
+ In order to know how to interact with object in V-rep please go to link:
https://github.com/poppy-project/poppy-torso/blob/ff6254355ce18a26f58654f5abc82485a7a22d13/software/doc/tutorial/Poppy%20Torso%20interacting%20with%20objects%20in%20V-REP%20using%20Pypot.ipynb  
The enviroment is for poppy-torso and slightly different from humanoid and just adaptive it.
+ There is also a Demo for how to set up Poppy-Torso enviroment in the repository.

Note:
+ Be careful that VREP is often displaying pop-up that freezes the communication with pypot. You will have to close them otherwise a timeout will occur!
+ Or you will have a problem with your jupyter python kernel!


# Controller Common Issue Sheet
This chapter serves mainly as a simple guide of Odroid board in Poppy development.  
It will tell you basic knowledge about how to start working with controller.

Steps:
+ 1.	Connect all the Peripherals you need.
+ 2. Plug in the power cable and enpower it. After waiting for several seconds the blue LED on board should blink in a heart-beat model.
+ 3. Then open the Web-Interface by taping in http://poppy.local in your browser.
+ 4. Program in jupyter notebook and run it directly.
+ 5. When there is a problem occured, please first check the notes listed below.

Note:
+ 1.	The Ubuntu and Poppy environment and everything needed has already been set up.
+ 2.	Please make sure eMMC-module is successfully connected on the board before boot.
+ 3.	Wireless communication is also possible after USB wireless module has been inserted. If not, please use desktop model to check the wireless setup.
+ 4.	After booting, when blue LED should blink in a heart-beat model. If not, please check it by using desktop model with a HDMI cable whether it's off-line. 
If it dosen't work firstly follow the official documentation http://docs.poppy-project.org/en/getting-started/connect.html.  And if it is still not helpful please reinstall the system under the link https://github.com/poppy-project/odroid-poppysetup


