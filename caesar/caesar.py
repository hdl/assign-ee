#
# Name:
# ID:
# Date: March 8, 2015

import sys

class CaesarCipher:
    """docstring for CaesarCipher"""
    def __init__(self):
        self.hash_table={}
        for c in "0123456789":
            self.hash_table[c] = ord(c)-ord('0')
        for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            self.hash_table[c] = ord(c)-ord('A')+10
        for c in "abcdefghijklmnopqrstuvwxyz":
            self.hash_table[c] = ord(c)-ord('a') +36
        self.index_list="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

        self.decrypted_text=""
        self.encrypted_text=""
    def ClearALL(self):
        self.decrypted_text=""
        self.encrypted_text=""
    def PrintDecrypted(self):
        print(self.decrypted_text)
    def PrintEncrypted(self):
        print(self.encrypted_text)

    def Encrypt(self, shift):
        if shift<1 or shift >61 or shift==26 or shift==36:
            return
        self.encrypted_text=""
        for c in self.decrypted_text:
            if c in self.index_list:
                new_index = self.hash_table[c]+shift
                if new_index > 61:
                    new_index = new_index-62
                if new_index <0:
                    new_index = 62 + new_index # 0 1 2....61
                c = self.index_list[new_index]
            self.encrypted_text=self.encrypted_text+c
        #print"After: "+self.encrypted_text

    def Decrypt(self, shift):
        if shift<1 or shift >61 or shift==26 or shift==36:
            return
        self.decrypted_text=""
        for c in self.encrypted_text:
            if c in self.index_list:
                new_index = self.hash_table[c]-shift
                if new_index > 61:
                    new_index = new_index-62
                if new_index <0:
                    new_index = 62 + new_index # 0 1 2....61
                c = self.index_list[new_index]
            self.decrypted_text=self.decrypted_text+c
        #print"After"+self.decrypted_text
    def LoadEncryptedFile(self, filename):
        try:
            with open (filename, "r") as myfile:
                self.encrypted_text=myfile.read()
            if self.encrypted_text=="":
                print("File is empty")
                return False
            else:
                return True
        except:
            print("File not exist")
            return False

    def LoadDecryptedFile(self, filename):
        try:
            with open (filename, "r") as myfile:
                self.decrypted_text=myfile.read()
            if self.decrypted_text=="":
                print("File is empty")
                return False
            else:
                return True
        except:
            print("File not exist")
            return False
    def SaveEncryptedFile(self, filename):
        with open (filename, "w") as newfile:
            newfile.write(self.encrypted_text)
    def SaveDecryptedFile(self, filename):
        with open (filename, "w") as newfile:
            newfile.write(self.decrypted_text)
    def ShowALL(self):
        print("decry is:")
        print(self.decrypted_text)
        print("encry is")
        print(self.encrypted_text)
    def DetermineShift(self):
        # english leetter frequency
        cor=[0.64297,0.11746,0.21902,0.33483,1.00000,0.17541,
        0.15864,0.47977,0.54842,0.01205,0.06078,0.31688,0.18942,
        0.53133,0.59101,0.15187,0.00748,0.47134,0.49811,0.71296,
        0.21713,0.07700,0.18580,0.01181,0.15541,0.00583]
        error=[0.0]*61
        for shift in range(0,61):
            self.Decrypt(shift)
            arr = self.freq(self.decrypted_text)
            e=0.0
            for j in range(0, 26):
                e+=abs(arr[j]-cor[j])**2
            error[shift]=e;

        result=[]
        result.append(error.index(min(error)))
        error.remove(min(error))
        result.append(error.index(min(error)))
        error.remove(min(error))
        result.append(error.index(min(error)))
        error.remove(min(error))
        print(result)



    def freq(self, text):
        arr=[0.0]*26
        for ch in text:
            x=ord(ch)
            if(x>97 and x<=122):
                arr[x-97]+=1.0
        for i in range(0,26):
            try:
                arr[i]/=max(arr)
            except:
                continue
        return arr

def display_menu():
    print('''C Clear All
L Load Encrypted File
R Read Decrypted File
S Store Encrypted File
W Write Decrypted File
O Output Encrypted Text
P Print Decrypted Text
E Encrypt Decrypted Text
D Decrypted Encrypted Text
Q Quit
G Debug
--------------------------''')
    return

def run_choice(MyCaesarCipher, choice):
    if choice=='C':
        MyCaesarCipher.ClearALL()
    elif choice=='L':
        filename = input("Enter Filename> ")
        MyCaesarCipher.LoadDecryptedFile(filename)
    elif choice=='R':
        filename = input("Enter Filename> ")
        MyCaesarCipher.LoadDecryptedFile(filename)
    elif choice=='S':
        filename = input("Enter Filename> ")
        MyCaesarCipher.SaveEncryptedFile(filename)
    elif choice=='W':
        filename = input("Enter Filename> ")
        MyCaesarCipher.SaveDecryptedFile(filename)
    elif choice=='O':
        MyCaesarCipher.PrintEncrypted()
    elif choice=='P':
        MyCaesarCipher.PrintDecrypted()
    elif choice=='E':
        shift = int(input("Enter Shift Amount> "))
        MyCaesarCipher.Encrypt(shift)
    elif choice=='D':
        shift = int(input("Enter Shift Amount> "))
        MyCaesarCipher.Decrypt(shift)
    elif choice=='Q':
        sys.exit(0)
    elif choice=="G":
        MyCaesarCipher.ShowALL()



if __name__ == '__main__':
    MyCaesarCipher = CaesarCipher()
    #print len(sys.argv)
    if(len(sys.argv)==1):
        # no argument
        while(1):
            display_menu()
            choice = input("Enter Choice> ")
            run_choice(MyCaesarCipher, choice.upper())

    elif(len(sys.argv)==3):
        try:
            shift = int(sys.argv[1])
            if abs(shift)<0 or abs(shift) >61 or abs(shift)==26 or abs(shift)==36:
                print("Invalid syntax: caesar shift infile [outfile]")
                sys.exit(0)
            inputfile=sys.argv[2]
            if shift>0:
                MyCaesarCipher.LoadDecryptedFile(inputfile)
                MyCaesarCipher.Encrypt(abs(shift))
                MyCaesarCipher.PrintEncrypted()
            elif shift<0:
                MyCaesarCipher.LoadEncryptedFile(inputfile)
                MyCaesarCipher.Decrypt(abs(shift))
                MyCaesarCipher.PrintDecrypted()
            elif shift==0:
                MyCaesarCipher.LoadEncryptedFile(inputfile)
                MyCaesarCipher.DetermineShift()
        except ValueError:
            print("aInvalid syntax: caesar shift infile [outfile]")
            sys.exit(0)
    elif(len(sys.argv)==4):
            inputfile=sys.argv[2]
            MyCaesarCipher.LoadEncryptedFile(inputfile)
            for i in range(0,62):
                print(i)
                MyCaesarCipher.Decrypt(i)
                MyCaesarCipher.PrintDecrypted()
    else:
        print("Invalid syntax: caesar shift infile [outfile]")







