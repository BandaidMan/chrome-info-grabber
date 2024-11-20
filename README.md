# Chrome Info Grabber

### Description
A small python program that grabs various pieces of information that Google Chrome can store locally on your device. Can currently output your top sites, history, and decrypted passwords to the console. Easily flagged by AV so it is recommended to use this on a VM with defenses completely disabled.

### Dependencies
Make sure you have the following libraries installed with pip3
```
pycryptodome
pywin32
sqlite3
```

### Usage
```
python3 chrome-info-grabber.py
```
Developed for Windows11, no guarantee it will work on anything else.

### Potential Future Developments
1. Add options for information types gathered, specify how many entries for stuff like history and topsites
2. Make a generalized function for grabbing info from each db
3. Find other data stored locally that would be interesting to grab

### How it Works
To get a better understanding of how the program works, I would recommend pulling up the program alongside this short description.

Google Chrome doesn't store all of your information in Google servers somewhere. There are portion of information stored on your machine, although some of which may instead go to cloud storage if the right options are selected. The specific information grabbed so far from this program is in the appdata folder, located somewhere in `C:\Users\YOURUSER\AppData\Local\Google\Chrome\User Data`. Here, Chrome likes to store information in SQLite3 databases, with most of the information I found being in plaintext (thankfully not passwords though). Also stored is the Windows DPAPI-encrypted AES-GCM encryption key for the stored passwords. After decrypting the key using DPAPI and a few other small steps, we are ready to start grabbing information from the SQLite 3 databases, which can easily be connected to and queried with python. Most of this is plaintext so it can be printed out to the console, but the passwords saved for logins first need to be decrypted. In each encrypted password grabbed from the database, it has 4 distinct parts to it. A "v10" prefix, the IV for AES-GCM (96 bits or 12 bytes), the encrypted password, and 16 bytes of what I think is the message authentication code (MAC). Knowing this information, the password can now be decrypted and outputted to the console like the other plaintext information.


