import functools
import struct
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
import mysql.connector as mariadb
import pickle
import os

#connect
mydb = mariadb.connect(
    user = "test",
    password = "password",
    host = "localhost",
    database = "GoogleEn_Db"
)
#create cursor
mycursor = mydb.cursor()

##########################GENERATE CERTIFICATE PAIR########################
def getkeys():
    new_key = RSA.generate(2048)
    def getprivatek():
        private_key = new_key.exportKey()
        return private_key
    def getpublick():
        public_key = new_key.publickey().exportKey()
        return public_key
    #print("PVK:\n")
    #print(private_key)
    #print("PBK:\n")
    #print(public_key)
    #sql_statement = "INSERT INTO Login (PublicK,PrivateK) VALUES(%s,%s);"
    #items_to_insert = (public_key,private_key)
    #mycursor.execute(sql_statement,items_to_insert)
    #mydb.commit()
    #sql_statement2 = "SELECT * from Login"
    #mycursor.execute(sql_statement2)
    #myresult = mycursor.fetchall() #fetchone()3
    #for x in myresult:
    #    print("Keys:\n")
    #    print(x)
    #    print("\n")
    #fd = open("private_key.pem", "wb")
    #fd.write(private_key)
    #fd.close()

    #fd = open("public_key.pem", "wb")
    #fd.write(public_key)
    #fd.close()

################ENCRYPT/DECRYPT DATA WITH CERTIFICATE#######################
#message = b'CODE EVERYDAY TO GET BETTER'

#key = RSA.import_key(open('public_key.pem').read())

#ciphertext = cipher.encrypt(message)
#print("\n\n")
#print(ciphertext)
#print("\n\n")
def encrpyt( in_filename, out_filename=None, chunksize=64*1024):
    statement = "SELECT Username from Login"
    mycursor.execute(statement)
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)
    user = input("Which users are you sharing this file with? This will determine the public key used to encypt\n\n")
    sql_statement = "SELECT publicK from Login WHERE username = '%s' "%(user)
    mycursor.execute(sql_statement)
    #generate AES KEY
    #Encrypt file with AES
    #Encrypt AES key with public key
    #Send the AES key encrypt with the public key and the file that is encrypted with AES 
    secret_key = os.urandom(16)
    if not out_filename:
        out_filename = in_filename + '.enc'
    ivs = os.urandom(16)
    encryptor = AES.new(secret_key,AES.MODE_CBC, ivs)
    filesize = os.path.getsize(in_filename)
    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(ivs)
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))
    userpublickey = mycursor.fetchone()
    upk = functools.reduce(lambda sub, ele: sub * 10 + ele, userpublickey)
    key = RSA.import_key(upk)
    cipher = PKCS1_OAEP.new(key)
    encrpyted = cipher.encrypt(secret_key)
    with open("AESKEY", "wb") as binary_file:
        binary_file.write(encrpyted)

def decryption(key,in_filename, out_filename=None, chunksize=24*1024):
    with open("user.p", "rb") as myFile:
        user = pickle.load(myFile)
        sql_statement = "SELECT privateK from Login WHERE username = '%s' "%(user)
        mycursor.execute(sql_statement)
    userprivatekey = mycursor.fetchone()
    #print(userprivatekey)
    uprk = functools.reduce(lambda sub, ele: sub * 10 + ele, userprivatekey)
    key2 = RSA.import_key(uprk)
    cipher = PKCS1_OAEP.new(key2)
    with open(key,'rb') as filek:
        ky = filek.read()
    userky = cipher.decrypt(ky)
    print(userky)
    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]
    with open(in_filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(userky, AES.MODE_CBC, iv)

        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))
            outfile.truncate(origsize)

#key = RSA.import_key(open('private_key.pem').read())
#cipher = PKCS1_OAEP.new(key)S
#plaintext = cipher.decrypt(ciphertext)
#print (plaintext.decode("utf-8"))


#def main():
#    decryption('AESKEY','Text File2.txt.enc')


#if __name__ == '__main__':
#   main()