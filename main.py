import base64
import codecs
import os
def menu():
  print("\n\n")
  print("Welcome! Would you like to :")
  print("1 - Encrypt a file")
  print("2 - Decrypt a file", end = "\n\n")
  choice = int(input("Enter your choice : "))
  if choice == 1:
    encrypt()
  elif choice == 2:
    decrypt()
  else:
    print("Incorrect choice!")
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
    contents = base64.b64encode(bytes(contents, "utf-8"))
    with open(file, "wb") as data:
      data.write(contents)
    sizeafter = os.path.getsize(path)
    print("Encryption finished!")
    print("File size went from", sizebefore, "bytes to", sizeafter, "bytes!")
    menu()
def decrypt():
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
    print("Decrypting data...")
    path = os.getcwd()+"/"+file
    sizebefore = os.path.getsize(path)
    contents = base64.b64decode(bytes(contents, "utf-8"))
    contents = contents.decode("utf-8")
    with open(file, "wt") as data:
      data.write(contents)
    sizeafter = os.path.getsize(path)
    print("Successfully decrypted file!")
    print("File size went from", sizebefore, "bytes to", sizeafter, "bytes!")
    menu()
menu()