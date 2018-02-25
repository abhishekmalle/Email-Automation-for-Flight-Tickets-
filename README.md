# Email-Automation-for-Flight-Tickets-

This project is intended to provide better support for those wanting to travel but too lazy to actually do the research.

The software/website allows the user to enter a destination, origin, and departure times, and reports with an email of the best
available flight tickets for the senario using the Amadeus API. 

Access to the website is here: http://ec2-13-59-242-68.us-east-2.compute.amazonaws.com/
Once the fields are entered, an email will be automatically be sent, signing you up.

# Instructions for use:
pip install flask
pip install flask_wtf
pip install wtforms
pip install boto
pip install amadeus

in your terminal type the command:
FLASK_APP=textrunner.py python3 -m flask run --host=0.0.0.0 --port=80

then go to 0.0.0.0:80 in your browser and you should have access.

# Contributing
Contributors are welcome, please see 
