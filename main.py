import base64
import codecs
import os
import cryptography
from cryptography.fernet import Fernet
import requests
import time
import webbrowser
algorithm = "base64"
currentVersion = "1.1"
def menu():
  global algorithm
  global newUpdate
  global currentVersion
  global version
  print("\n\n")
  if newUpdate == True:
    print("A new update can be downloaded now from the GitHub page!")
    print("You're currently running", currentVersion, "and", version, "is available!", end = "\n\n")
  print("Welcome! Would you like to :", end = "\n\n")
  print("1 - Encrypt a file (selected algorithm : "+algorithm+")")
  print("2 - Decrypt a file (selected algorithm : "+algorithm+")")
  print("3 - Select cipher algorithm")
  if newUpdate == True:
    print("4 - Download the updated version")
  print("")
  choice = int(input("Enter your choice : "))
  if choice == 1:
    encrypt()
  elif choice == 2:
    decrypt()
  elif choice == 3:
    select_algorithm()
  elif choice == 4 and newUpdate == True:
    link = "https://github.com/Uiop3385/PythonEncoderDecoder/releases/tag/" + version
    webbrowser.open_new(link)
  else:
    print("Incorrect choice!")
    menu()

def select_algorithm():
  global algorithm
  print("\n\n")
  print("Select a cipher algorithm :", end = "\n\n")
  print("1 - Base64")
  print("2 - Fernet", end = "\n\n")
  choice = int(input("Enter your choice : "))
  if choice == 1:
    algorithm = "base64"
  elif choice == 2:
    algorithm = "fernet"
  else:
    print("Invalid choice")
    select_algorithm()
  menu()

def encrypt():
  print("\n\n")
  file = input("Please enter the file name (include the file extension too) : ")
  try:
    with open(file) as data:
      data.read()
  except:
    print("This file does not exist. Make sure it is located in the current working directory of the program, which is", os.getcwd())
    encrypt()
  else:
    with open(file) as read:
      contents = read.read()
    print("Encrypting data...")
    path = os.getcwd()+"/"+file
    sizebefore = os.path.getsize(path)
    if algorithm == "base64":
      contents = base64.b64encode(bytes(contents, "utf-8"))
    elif algorithm == "fernet":
      key = Fernet.generate_key()
      fernet = Fernet(key)
      contents = fernet.encrypt(bytes(contents, "utf-8"))
      with open("key.key", "wb") as key_file:
        key_file.write(key)
    with open(file, "wb") as data:
      data.write(contents)
    sizeafter = os.path.getsize(path)
    time.sleep(2)
    print("Encryption finished!")
    print("File size went from", sizebefore, "bytes to", sizeafter, "bytes!")
    if algorithm == "fernet":
      print("Make sure to keep key.key stored safely as it is necessary to decrypt the file!")
    menu()

def decrypt():
  print("\n\n")
  file = input("Please enter the file name (include the file extension too) : ")
  try:
    with open(file) as data:
      data.read()
  except:
    print("This file does not exist. Make sure it is located in the current working directory of the program, which is", os.getcwd())
    decrypt()
  else:
    with open(file) as read:
      contents = read.read()
    print("Decrypting data...")
    path = os.getcwd()+"/"+file
    sizebefore = os.path.getsize(path)
    if algorithm == "base64":
      contents = base64.b64decode(bytes(contents, "utf-8"))
      contents = contents.decode("utf-8")
    elif algorithm == "fernet":
      try:
        with open("key.key", "rb") as key_file:
          key = key_file.read()
        fernet = Fernet(key)
        contents = fernet.decrypt(bytes(contents, "utf-8"))
        contents = contents.decode("utf-8")
      except:
        time.sleep(0.5)
        print("No key file was found! Make sure your key file is in the current directory ("+os.getcwd()+"), that it is named key.key and that it is not corrupted.")
        menu()
    with open(file, "wt") as data:
      data.write(contents)
    sizeafter = os.path.getsize(path)
    time.sleep(2)
    print("Successfully decrypted file!")
    print("File size went from", sizebefore, "bytes to", sizeafter, "bytes!")
    if algorithm == "fernet":
      os.remove("key.key")
      print("key.key has been automatically deleted.")
    menu()
try:
  response = requests.get("https://api.github.com/repos/Uiop3385/PythonEncoderDecoder/releases/latest")
  version = response.json()["tag_name"]
except:
  print("No internet connection, could not check for updates!")
  time.sleep(3)
  newUpdate = False
else:
  if version != currentVersion:
    newUpdate = True
  else:
    newUpdate = False
menu()