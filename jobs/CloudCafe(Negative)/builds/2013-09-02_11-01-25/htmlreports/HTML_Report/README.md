CloudCAFE-Python
================
**Rackspace Proprietary** Python implementation of the Cloud C.ommon A.utomation F.ramework E.ngine. The CloudCAFE-Python implementation is designed to 
be used for writing and running Automated Rackspace Cloud tests. It is the result of combining the internal zodiac (Compute), 
death-star (Cloud Object Storage) and apollo (Cloud Block Storage) frameworks together into a common engine.

CloudCAFE-Python is a **PROPRIETARY** code base. It should not be distributed outside of Rackspace and Rackspace employees. 
This includes maintaining **ANY** repository apart from this Rackspace internal github repo.

Contributions to this project are not only welcome, they are encouraged. For more information on contributing to the CloudCAFE project please consult the CloudCAFE development process guide on the Rackspace wiki at: https://one.rackspace.com/display/cloudqe/CloudCAFE+Python+Development+Process

Project WIKI:
================
The CloudCAFE framework uses the QE-Core Wiki for most of it's documentation. Please refer to https://one.rackspace.com:8443/display/cloudqe/CloudCAFE for
further documentation. 

CloudCAFE Development Process:
================
CloudCAFE uses a formal development process. You can find the detailed documentation on this process on the CloudCAFE wiki here: https://one.rackspace.com/display/cloudqe/CloudCAFE+Python+Development+Process

Project Mailing List:
================
CloudCAFE development uses an internal mailing list, cloud-cafe@lists.rackspace.com. To Subscribe, visit: https://lists.rackspace.com/sympa/info/cloud-cafe

Notes About Code Structure:
================
The CloudCAFE framework uses an Epydoc style pydoc documentation. If you are not sure what a particular cloudcafe.XYZ package is for, take a look at  
the documentation for that package (either in the generated HTML documentation or by opening the source file directly.

For more information on epydoc please see: http://epydoc.sourceforge.net/ 

API & Test Repository Documentation:
================
The **entire** CloudCAFE project, every package, class, method, etc... is documented to the epydoc standard. There is a script in /build that will automatically
generate the most current version of the CloudCAFE documentation for you **providing** you have installed Epydoc (see REQUIRED SOFTWARE/PACKAGES below).

To generate the CloudCAFE API and test case documentation:
* cd to <REPO_LOCATION>CloudCAFE-Python/build
* Execute the script generateDocs.sh
* In the browser of your choice, open the file <REPO_LOCATION>CloudCAFE-Python/docs/api-doc/index.html for the API documentation
* In the browser of your choice, open the file <REPO_LOCATION>CloudCAFE-Python/docs/repo-doc/index.html for the Test Case Respository documentation


Setup Notes:
================
* YOU MUST update your python path to include the cloudcafe and the testrepo package name spaces. For example, if you had done the git pull 
to /source/CloudCAFE-Python on your local file system you would need to do the following:
	* export PYTHONPATH=$PYTHONPATH:/source/CloudCAFE-Python/lib/


REQUIRED Software/Packages:
================
**Python 2.6.x**
CloudCAFE-Python requires the Python 2.6.x version of Python. It is compatible with 2.7.x versions as well. It is *not* compatible with Python 3 -- attempt at your own risk. 
To install Python on your local system:
* Windows and MAC Users: http://www.python.org/getit/
* Ubuntu Users: CloudCAFE-Python compatible Python is installed natively with Ubuntu 11.x and above.
  WARNING: Installing Python into Ubuntu can cause *serious* system troubles. Only do so if you know what you are doing.

**PIP Install**
The Python Package installer is required.
* python-pip for Linux and MAC Users: apt-get install python-pip
* python-pip for Windows Users: http://pypi.python.org/pypi/pip#downloads

**Python packages**
The required python packages are listed further below, but you can try to get them all with:
* pip install -r requirements.txt


**Epydoc**
This project currently requires epydoc to auto-generate python html documentation from the source code. 
To install epydoc on ubuntu/debian simply run the command: 
* sudo apt-get install python-epydoc

**PyUnit (unittest2)**
The Python xUnit implementation. PyUnit is already included in the Python installation. You can find documentation on unittest here:
http://docs.python.org/library/unittest.html

To Install:
* sudo apt-get install python-unittest2

**NOTE:** If you are using Python 2.7.x (which is required by CloudCAFE-Python) You still need the unittest2 library, this has been backported
into Python 2.7.x. See: http://pypi.python.org/pypi/unittest2, however, unittest2 is still required as CloudCAFE-Python must be backwardly compatible.   

**Requests**
* requests is available via pip install (sudo pip install requests)

**dateutil**
* The dateutil library is available via pip install (sudo pip install requests)
* NOTE: This library is standard in Python 2.7

**Paramiko**
Paramiko is required by the SSH connector in the CCEngine. You can find documentation on Parmiko here:
https://github.com/paramiko/paramiko

To Install:
* sudo pip install paramiko

**Nova Client**
This framework currently wraps the nova client command line process in order to integration test the lunr API.
This project requires that you have the nova client installed locally. *ONLY IF YOU WANT TO RUN NOVA SHELL TESTS* To install the OpenStack Nova Client:
* git clone https://github.com/openstack/python-novaclient.git
* cd to the nova-client folder created from the git clone
* python setup.py install

Eclipse Install/Setup Directions:
================
While you are free to use any IDE you choose, the Eclipse IDE provides a robust, feature full integrated development environment for Python development in general and works extremely well for CloudCAFE development. To use Eclipse with CloudCAFE:
**Install Eclipse**
* Download Eclipse from http://www.eclipse.org/downloads/ You can use any flavor of Eclipse you would like/need. Eclipse Classic is the most streamlined and ready to go for Python/CloudCAFE development.
* Install Eclipse following the default instructions

**Importing CloudCAFE into Eclipse**
CloudCAFE **already** has an Eclipse/PyDev supported project included as a part of this git repository. In order to work with CloudCAFE using Eclipse:
* Open Eclipse with PyDev installed and configured.
* Select File --> Import
* Select Existing Projects Into Workspace under General and Click Next
* Under the General Folder select Existing Projects Into Workspace and Click Next
* Click Select Root Directory and Click Browse
* Browse to your local CloudCAFE-Python gitrepo. For instance, if you cloned CloudCAFE into /source you would browse to /source/CloudCAFE-Python
* Click Finish

**PyDev for Eclipse**
PyDev is a Python IDE plug-in for Eclipse. You can find a wealth of information about PyDev at their web site: http://pydev.org To install/configure PyDev for Eclipse:
* First you must install Eclipse. PyDev is specfically an **Eclipse** Plug-in.
* It is **STRONGLY** suggested that you follow the directions found here http://pydev.org/manual_101_install.html under the section heading "Installing with the update site"
* Now that PyDev is installed you will need to configure it within Eclipse. Simply follow the directions found here: http://pydev.org/manual_101_interpreter.html

