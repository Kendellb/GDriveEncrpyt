import GoogleApI
import Encryption
import sys
#import mysql.connector as mariadb

#connect
#mydb = mariadb.connect(
#    user = "test",
#    password = "password",
#    host = "localhost",
#    database = "GoogleEn_Db"
#)
#create cursor
#mycursor = mydb.cursor()

def menu():
    try:
        while True:
            userIn = input("|U - Upload file | D - Dowload file | E - Exit").lower()
            if(userIn == "u"):
                while True:
                    print("upload file:")
                    print("\nEnter m to return to main menu.\n")
                    userIn = input("Enter file name: ")
                    if(userIn == "m"):
                        break
                    else:
                        Encryption.encrpyt(userIn)
                        upload = userIn + ".enc"
                        GoogleApI.uploadFile(upload)
                        GoogleApI.uploadFile('AESKEY')
            elif(userIn == "e"):
                print("Exiting")
                sys.exit()
            elif(userIn == "d"):
                while True:
                    print("Dowload:\n")
                    userIn1 = input("\n|S - Search for a file|D - Dowload File|E - exit to main menu|\n ").lower()
                    if(userIn1 == "s"):
                        userIn = input("Enter file name: ")
                        GoogleApI.searchFile(userIn)
                    elif(userIn1 == "d"):
                        print("Enter names of encrypted file then encrypted keys\n")
                        userIn=input("Enter file name: ")
                        
                        
                        userIn2=input("Enter file name: ")
                        fileID = GoogleApI.fileID(userIn)
                        fileID2= GoogleApI.fileID(userIn2)
                        GoogleApI.downloadFile(fileID,userIn)
                        GoogleApI.downloadFile(fileID2,userIn2)
                        Encryption.decryption(userIn2,userIn)
                    elif(userIn == "e"):
                        break
                    else:
                        print("Wrong input try again!")
            
            else:
                print("Wrong input try again!")
    except Exception:

        pass
            


#with open("user.p", "rb") as myFile:
#                data = pickle.load(myFile)
