import sys
import mysql.connector as mariadb
import NewUser
import pickle


mydb = mariadb.connect(
    user = "test",
    password = "password",
    host = "localhost",
    database = "GoogleEn_Db"
)

mycursor =mydb.cursor()
def login():
    loginput=int(input("Login(1) or Register(0) \n:"))
    if loginput <= 0:
        print("new user")
        NewUser.createuser()
    else:
        count = 0
        while True:
            Usernamelog = input("Username: ")
            Passwordlog = input("Password: ")
            sql_statement = "SELECT * From Login WHERE BINARY Username = '%s' AND BINARY Password = '%s'" %(Usernamelog,Passwordlog)
            mycursor.execute(sql_statement)
        
            #sql_statement2 = "SELECT Password from Login WHERE Password = '%s'" %(Passwordlog)
            #mycursor.execute(sql_statement2)
            if mycursor.fetchone():
                print("SUCCESSFULLY LOGIN!")
                with open("user.p","wb") as myFile:
                    pickle.dump(Usernamelog, myFile)
                    break
            elif count == 3:
                print("TOO MANT TRIES!!")
                sys.exit()
            else:
                count= count + 1
                print("User doesnt exist or wrong password!\n Try Again!\n")


    



#mycursor.close()