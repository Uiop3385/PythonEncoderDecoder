import base64
import codecs
import os
import cryptography
from cryptography.fernet import Fernet
from Cryptodome.Cipher import AES
import requests
import time
import webbrowser
algorithm = "base64"
currentVersion = "1.2"
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
  print("2 - Fernet")
  print("3 - AES", end = "\n\n")
  choice = int(input("Enter your choice : "))
  if choice == 1:
    algorithm = "base64"
  elif choice == 2:
    algorithm = "fernet"
  elif choice == 3:
    algorithm = "aes"
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
    if algorithm != "aes":
      with open(file) as read:
        contents = read.read()
    else:
      with open(file, "rb") as read:
        contents = read.read()
    print("Encrypting data...")
    path = os.getcwd()+"/"+file
    sizebefore = os.path.getsize(path)
    if algorithm == "base64":
      try:
        contents = base64.b64encode(bytes(contents, "utf-8"))
      except:
        print("An error occured. You may have tried encrypting an already encrypted file.")
        time.sleep(2)
        menu()
    elif algorithm == "fernet":
      try:
        key = Fernet.generate_key()
        fernet = Fernet(key)
        contents = fernet.encrypt(bytes(contents, "utf-8"))
        with open("key.key", "wb") as key_file:
          key_file.write(key)
      except:
        print("An error occured. You may have tried encrypting an already encrypted file.")
        time.sleep(2)
        menu()
    elif algorithm == "aes":
      key = input("Please enter an AES encryption key (16 bytes for 128bit, 24 bytes for 192bit or 32 bytes for 256bit). You can also enter 'random16', 'random24' or 'random32' to randomely generate a key of the specified byte length. Keys entered manually may be altered to function : ")
      if "random" in key:
        if "16" in key:
          key = os.urandom(16)
        elif "24" in key:
          key = os.urandom(24)
        elif "32" in key:
          key = os.urandom(32)
      else:
        key = key.encode("utf-8")
      iv = os.urandom(16)
      try:
        cipher = AES.new(key, AES.MODE_CFB, iv)
      except:
        print("An error occured. You may have entered an invalid key; if you want to generate a valid key, enter 'random16', 'random24' or 'random32' to generate a valid key of the specified number of bytes. You may also have tried encrypting an already encrypted file.")
        time.sleep(2)
        menu()
      else:
        contents = cipher.encrypt(contents)
        with open(file, "wb") as data:
          data.write(base64.b64encode(contents))
    sizeafter = os.path.getsize(path)
    time.sleep(2)
    print("Encryption finished!")
    print("File size went from", sizebefore, "bytes to", sizeafter, "bytes!")
    if algorithm == "fernet":
      print("Make sure to keep key.key stored safely as it is necessary to decrypt the file!")
    elif algorithm == "aes":
      key_display = key.hex()
      iv_display = iv.hex()
      print("Your key (in hexadecimal) is "+str(key_display)+", make sure to store it safely as it is necessary to decrypt the file. The initialisation vector of this encryption (in hexadecimal) is "+str(iv_display)+". Keep it just as carefully.")
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
    if algorithm != "aes":
      with open(file) as read:
        contents = read.read()
    print("Decrypting data...")
    path = os.getcwd()+"/"+file
    sizebefore = os.path.getsize(path)
    if algorithm == "base64":
      try:
        contents = base64.b64decode(bytes(contents, "utf-8"))
        contents = contents.decode("utf-8")
      except:
        print("An error occured. You may have tried decrypting a file that hasn't been encrypted, or you may have chosen the wrong algorithm.")
        time.sleep(2)
        menu()
    elif algorithm == "fernet":
      try:
        with open("key.key", "rb") as key_file:
          key = key_file.read()
        fernet = Fernet(key)
        contents = fernet.decrypt(bytes(contents, "utf-8"))
        contents = contents.decode("utf-8")
      except FileNotFoundError:
        time.sleep(0.5)
        print("No key file was found! Make sure your key file is in the current directory ("+os.getcwd()+"), that it is named key.key and that it is not corrupted.")
        menu()
      except:
        print("An error occured. You may have tried decrypting a file that hasn't been encrypted, or you may have chosen the wrong algorithm, or the key file may be corrupted.")
        time.sleep(2)
        menu()
    elif algorithm == "aes":
      key = input("Enter the encryption key used (in hexadecimal) : ")
      key = bytes.fromhex(key)
      iv = input("Enter the initialisation vector (IV) used for encryption (in hexadecimal) : ")
      iv = bytes.fromhex(iv)
      try:
        with open(file, "rb") as data:
          contents = base64.b64decode(data.read())
        cipher = AES.new(key, AES.MODE_CFB, iv)
        contents = cipher.decrypt(contents)
        contents = contents.decode("utf-8")
      except:
        print("An error occured. You may have tried decrypting a file that hasn't been encrypted, or you may have chosen the wrong algorithm. You may also have entered an incorrect key and/or IV, check you've enetered them correctly.")
        time.sleep(2)
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