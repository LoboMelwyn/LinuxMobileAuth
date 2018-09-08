# LinuxMobileAuth
This is a small POC for authenticating in Linux Desktop using your Android Mobile's Fingerprint scanner

**Note: Works only on UNIX based system which has PAM Modules**

# Installing Instruction (Ubuntu)
1. Install Python PAM module by running this command ````sudo apt-get install libpam-python ````
1. Edit **/etc/pam.d/common-auth** and enter following line in the top of the file
  **auth  sufficient  pam_python.so /path/to/pam.py**
1. Compile the MobileAuthPOC mobile app and install it in your android phone (Make sure you enter a proper IPAddress of your Linux Machine)
1. Create a new File named **webauth.service** in   **/etc/systemd/system** and Enter following lines in it
````
[Unit]
Description=WEB Auth service

[Service]
ExecStart=/path/to/authserver.sh

[Install]
WantedBy=multi-user.target
````
You can Enable the webauth service using

````sudo service webauth enable````

````sudo service webauth start````

Now start MobileAuthPOC app in your device and test it by opening a terminal and typing ````sudo -i````