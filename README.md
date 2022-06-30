# Crowd-Sourced-Deadline-Manager

This application runs a Crowdsourced Deadline Discovery Tool for Imperial College Department of EEE. The login is using SAML with Imperial College as the identity provider.


This flask application was set up in a Linux environment. Please use a Linux environment if you are following this user guide. Make sure you have pip and python installed.

1. Create a virtual environment, if you do not have venv, run the commmand ```sudo apt install python3.8-venv```. The virtual environment can be created by running ``` python3 -m venv path\_to\_folder/venv```
2. From the repository folder, run ```.venv/bin/activate``` to activate the virtual environment
3. Then in the same folder, there should be a requirements.txt, run ``` pip install -r requirements.txt. If there is an error about xmlsec, you can install it here using this command: ``` sudo apt-get install pkg-config libxml2-dev libxmlsec1-dev libxmlsec1-openssl```. Run the pip install after installing xmlsec.

This should set up the proper environment with all the python packages installed.

To create the mock database with some prefilled values, run ```python database.py```.
To run the application, there should be run.py file in the repository. It contains the app to launch which is taken from the __init__.py file in the flaskdeadline folder. Before launching the app, you can set the environment variables to debug and development mode by running ``` export FLASK\_DEBUG=1 ``` and ``` export FLASK\_ENV=development ```. The application can be launched via ``` python run.py ``` and the application should be started in localhost:5000/.

