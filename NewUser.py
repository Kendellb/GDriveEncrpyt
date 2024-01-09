import mysql.connector as mariadb
import Encryption

mydb = mariadb.connect(
    user = "test",
    password = "password",
    host = "localhost",
    database = "GoogleEn_Db"
)

mycursor =mydb.cursor()
def createuser():
    print("Register:")
    Usernamelog = input("Username: ")
    Passwordlog = input("Password: ")
    #print(Encryption.getpublick())
    #print(Encryption.getprivatek())
    sql_statement = "INSERT INTO  Login (Username, Password,PublicK,PrivateK) VALUES (%s,%s,%s,%s);"
    items_to_insert = (Usernamelog,Passwordlog,Encryption.getpublick(),Encryption.getprivatek())
    mycursor.execute(sql_statement,items_to_insert)
    mydb.commit()
    print("New User Created")
    

#def main():
#    createuser()

#if __name__ == '__main__':
#    main()