# CapstoneLemoyne
Read Me
Configuring the app.py file:
1. Open AJ Apps
2. Search for VSCode 1.78
3. Open VSCode 1.78
4. Install the following extensions
	a. Go to the view tab inside VSCode
	b. Click on Extensions
	c. Search for Python v2023.8.0, and install
	d. Python Extension Pack v1.7.0
	e. Flask-snippets v0.1.3
5. Install Python
	a. Open the app.py
b. Click Select Interpreter in the bottom right corner
c. Click the option to download Python
d. A new Microsoft store box should appear, click on get
e. If the Select Interpreter is still golden, click it and select Python 3.11.7 from the
drop-down
f. Go to File Explorer, then click on View
g. Click on the option to show Hidden items
h. Follow the path c: -> users -> *yourloginname* -> AppData (should be a slightly
different color -> local -> Microsoft -> WindowsApps -> Python3.11
If you followed the path, click on the address bar
Copy the path to your click board
6. Install the pip commands
a. Go to the search bar, type in command prompt
b. Open and you should be met with
c. Type in cd /d c:\, should change you to the c drive
d. Hopefully, you still have the path in your clipboard, type in cd *paste path*
e. Now that you are in the proper directory install the pip commands
i. pip install -U Flask
ii. pip install -U Werkzeug
iii. python -m pip install requests
iv. pip install mysql-connector-python
7. You may need to reload the Visual Studio Code a couple of times for the extensions to
take effect
8. With the new app.py contained in this zip file, you should be able to run without
debugging successfully
9. Login on the page, http://127.0.0.1:5000/login