import mysql.connector as m
con=m.connect(host='localhost', user='root', password='taetae!3012', database='Bank')
cur=con.cursor()
ctr=0
ctr1=0
print('===========================================================================')
print("\t\t\t\tPARTHENON'S BANK")
print('===========================================================================')

import random as r

import time as t
import datetime
print(datetime.datetime.now())

ch='Y' or 'y' 

def login():            #Login funcion in order to use the feature.
    while True:
        print()
        print('Welcome Back!!')
        us=input('Username: ')
        pwd=input('Password: ')
        ch=input("Go back to main menu(y or n): ")
        if ch=='y' or ch=='Y':
            entry()
        query1="select* from accounts where username='%s' and password='%s' "%(us,pwd)
        cur.execute(query1)
        data_login=cur.fetchall()       
        if len(data_login)!=0:      #checking the existence of username
            globals()['ctr']=1      #username exists
            print('Logined Successfully')
            return us, pwd
            
        else:
            print('LOGIN UNSUCCESSFUL!')            #doesn't exists
            print('Username or Password is wrong.')
            
            

def actno():
    an = []
    temp=''
    an.append(r.randint(1, 9))          #creating random number of 11 digits
    for i in range(10):                     #for account number
        an.append(r.randint(0, 9))
    for i in an:
        temp+=str(i)
    query="select acctno from accounts"
    cur.execute(query)
    data=cur.fetchall()      
    if temp in data:
        actno()
    else:
        return temp

def getactno(u):
    query1="select acctno from accounts where username='{0}'".format(u)
    cur.execute(query1)
    data=cur.fetchone()         #fetching the account number
    temp1=''
    for i in data:
        temp1+=str(i)
    return temp1   
        

def newpwd(u):
    #print password which length between 8-12,contain atleast one lowercase,digit,uppercase and a special charector
    while True:
        print("NOTE: The password should meet all criteria.")
        print("1. It must contain atleast 1 lower case.")
        print("2. It must contain atleast 1 upper case.")       #Criterias
        print("3. It must contain atleast 1 digit.")
        print("4. It must contain atleast 1 special character.")
        a=input("Enter password: ")
        sp=0    #special characters
        up=0    #upper case
        low=0   #lower case
        dig=0   #digits
        if 8<=len(a)<=12:
            for i in a:     #checking for every value in password if it meets the criteria
                if i in ['@','#','$','%','^','&','*','!']:  
                    sp=1
                elif i in ['0','1','2','3','4','5','6','7','8','9']:
                    dig=1
                elif 65<=ord(i)<=90:
                    up=1
                elif 97<=ord(i)<=122:
                    low=1
        else:
            print("invalid!! password should be 8-12 charactors")
            continue
        if (sp==1) and (dig==1) and (low==1) and (up==1):       #if it meets all criteria,
            value1=actno()                                      #then password will be generated
            query1="insert into accounts values ('{0}','{1}','{2}')".format(value1,u,a)
            cur.execute(query1)
            con.commit()                    
            print("password generated succesffully")
            t.sleep(5)
            print('Record Saved!')
            break
            
        else:
            if 8<=len(a)<=12:
                if sp==0:                   #error to be shown if missed any criteria
                    print("Invalid!! password should contain a special character")
                    continue
                if dig==0:
                    print("Invalid!! password should contain a digit")
                    continue
                if low==0:
                    print("Invalid!! password should contain a lowercase")
                    continue
                if up==0:
                    print("Invalid!! password should contain a uppercase")
                    continue


class registration:
    def __init__(self,us):
        self.us=us      #to initialise the data structure, called every time when an object is made from class

    def signup(self):
        u=self.us
        query="select*from accounts where username='%s'"%(u,)   
        cur.execute(query)
        data=cur.fetchone()     #checking the duplicacy of the username.
        if data!=None:
            print('This Username already exists.')
            print('Try another.')
            return False
            
        else:
            newpwd(self.us)     #functions to complete rest of the registration
            createdat(self.us)
            credit(self.us)
            


def createdat(u):                   #to insert customer details in profile
    u1=u                        
    print()
    print("Enter your following details")
    t.sleep(2)
    acctno=int(getactno(u1))
    name=input("Customer Name: ")
    DOB=input("Date of Birth (yyyy-mm-dd): ")
    Mob=int(input('Phone No. : '))
    email=input('Email ID: ')
    Gname=input("Father's Name: ")
    Ad=input("Permanent Address: ")
    City=input('City: ')
    State=input('State: ')
    pin=int(input("Pin Code: "))
    adhar=int(input("Adhar Number (mandatory): "))
    query="insert into cust_det values ({0},'{1}','{2}',{3},'{4}','{5}','{6}','{7}','{8}',{9},{10})".format(acctno,name,DOB,Mob,email,Gname,Ad,City,State,pin,adhar)
    cur.execute(query)                #inserting the values in table
    con.commit()                #function used to make changes
    print('Customer details are completed.')

def credit(u):
    while True:
        print("In order to proceed, your account must have some amount of money.")
        print("Bank offers ₹500 for newbies.")          #only for first 100 users who'll use our feature.
        actno=getactno(u)                               #a small token :)
        act_name=input("Enter Account Name: ")
        cr=500              
        a=datetime.datetime.strftime(datetime.date.today(),'%Y-%m-%d')
        query="insert into acct_det (acctno,acct_name,balance) values({0},'{1}',{2})".format(actno,act_name,cr)
        cur.execute(query)
        con.commit()
        qt="insert into transactions (acctno,added_amt,Balance_amt,date) values({0},{1},{2},'{3}')".format(actno,cr,cr,a)
        cur.execute(qt)
        con.commit()
        print("Account details created!")
        print()
        print("And your Account Number is", actno)
        print("Store it for future use.")       #account number must be stored by user.

        break


def entry():
    while True:
        print("1. LOGIN")
        print("2. REGISTER")        #sign-in sign-up part
        print("3. EXIT")
        ch=int(input('Choice: '))

        #LOGIN
        if ch==1:
            us,pwd=login()
            break
        
        #REGISTRATION
        elif ch==2:
            print("To open a bank account, you must be 18 or above years older.")
            print("Let's check.")
            today=datetime.date.today()
            year=int(today.strftime("%Y"))
            age=int(input("Type the year you were born: "))
            res=year-age
            if res>=18:     #checking the age
                print("You are eligible to use this feature.")
                while True:
                    us=input("Enter Username: ")
                    reg=registration(us)
                    a=reg.signup()
                    if a==False:
                        continue
                    else:
                        pass
                    break
            else:
                print("Sorry, you're not eligible to use this feature.")
                break
        elif ch==3:
            print("See you back soon!!")
            break
        else:
            print("Invalid choice.")
            continue
        break
entry()   


###########################################################################################################
def tuptostr(x):        #to convert tuple to string
    temp=''
    for i in x:
        temp+=str(i)
    return float(temp)


def cust_det(num):      #to display customer details
        query = "select* from cust_det where acctno={}".format(num,)
        cur.execute(query)
        data=cur.fetchall()
        l=["Account No.  ","Name         ","Date of Birth","Mobile       ","Email        ","Father's Name","Address      ","City         ","State        ","Pin Code     ","Adhar No.    "]
        m=[]
        for i in range(11):
            a=data[0][i]
            m.append(a)             #displaying it in vertical form
        for j in range(len(l)):
            print(l[j],":",m[j])
        print()   

def money(num):         #transaction of money
    while True:
        print("1. WITHDRAW AMOUNT")
        print("2. ADD AMOUNT")
        print("Press any key to EXIT.")
        x = int(input("Choose an operation: "))

        #withdrawing money
        if x==1:
            amt = float(input("Enter withdrawal amount: "))
            query1="select balance from acct_det where acctno={}".format(num,)
            cur.execute(query1)
            data=cur.fetchone()
            check=tuptostr(data)
            if 0<amt<=check:    #checking the balance
                print("Checked!")
                a=datetime.datetime.strftime(datetime.date.today(),'%Y-%m-%d')
                res=check-amt
                query2="insert into transactions (acctno,withdrawal_amt,Balance_amt,date) values ({0},{1},{2},'{3}')".format(num,amt,res,a)
                cur.execute(query2)
                con.commit()
                query3="update acct_det set balance={} where acctno={}".format(res,num)
                cur.execute(query3)
                con.commit()
                print("Transaction succeeded.")
                print()
                print("The current balance in your bank account", res)
                print()
                break
            
            else:       #if no balance
                print("Transaction failed!")
                print("Not enough money.")

                                
        #crediting amount
        elif x==2:
            amt = float(input("Enter amount to be credited: "))
            query1="select balance from acct_det where acctno={}".format(num,)
            cur.execute(query1)
            data=cur.fetchone()
            check=tuptostr(data)
            print("Checked!")       #why criteria for adding money? hehe :)
            a=datetime.datetime.strftime(datetime.date.today(),'%Y-%m-%d')
            res=(check+amt)
            query2="insert into transactions (acctno,added_amt,Balance_amt,date) values ({0},{1},{2},'{3}')".format(num,amt,res,a)
            cur.execute(query2)
            con.commit()
            query3="update acct_det set balance={} where acctno={}".format(res,num)
            cur.execute(query3)
            con.commit()
            print("Transaction succeeded.")     #transaction done yay
            print()
            print("The current balance in your bank account", res)
            print()
            
        else:
            break
        
        break


def details(num):           # to display account details
    query="select*from acct_det where acctno={}".format(num,)
    cur.execute(query)
    data=cur.fetchall()
    l=["Account No.   ","Account Name  ","Balance Amount"]
    m=[]
    for i in range(3):
        a=data[0][i]
        m.append(a)
    for i in range(len(l)):
        print(l[i],":",m[i])
    print()


def delete(num):        #to delete account
    while True:
        print("For deleting your account")
        query = "select*from accounts where acctno={}".format(num,)
        cur.execute(query)
        data = cur.fetchone()
        print(data)
        t.sleep(3)
        print()             #collection all the datas to be removed from database
        print("Collecting data to be erased")
        print("This could take a while....")
        t.sleep(4)
        print()
        print("All the data have been collected")
        print("NOTE: You won't be able to retrieve the data once your account has been deleted.")
        print("For the confirmation of the deletion of your account,")
        password=input("Re-enter your password:")
        if password in data:
            print()
            query1="delete from accounts where acctno={}".format(num,)
            cur.execute(query1)
            con.commit()
            #t.sleep(5)
            query2="delete from transactions where acctno={}".format(num,)
            cur.execute(query2)
            con.commit()
            print("PROGRESS SUCCESSFUL")
            print("Your Account has been successfully deleted!")
            break
                    
        else:
            print("Wrong Password.")
            
        break     

        



print()
while True:
    #acctnum
    num=int(input("Enter your Account number: "))
    q="select acctno from accounts where acctno={}".format(num,)
    cur.execute(q)
    data=cur.fetchall()
    try: 
        if num==data[0][0]:
            break
    except IndexError:
        print("Wrong Input!")
        print("Try again.")
        

print()
print("Choose a function")
while True:
    print("1. Customer Details")
    print("2. Account Details")
    print("3. Transaction")
    print("4. Transaction Details")
    print("5. To Update Profile")
    print("6. Delete Account")
    print("7. Quit")
    print()
    n = int(input("Choose an operation: "))

#CUSTOMER DETAILS
    if n==1:
        cust_det(num)

#ACCOUNT DETAILS#
    elif n==2:
        details(num)

#TRANSACTION
    elif n==3:
        money(num)

#TRANSACTION DETAILS
    elif n==4:
        query="select * from transactions where acctno={}".format(num,)
        cur.execute(query)
        data=cur.fetchall()
        print("Account No","\tDebit,Credit","\t\tBalance","\t\t\tDate")
        for row in data:
            print(row)

#UPDATE PROFILE
    elif n==5:
        print("NOTE: The field which are not in the options means you have to contact bank, to make changes.")
        print("What you want to update: ")
        while True:
            print("1. Name")
            print("2. email")
            print("3. Father's name")
            print("4. Address")
            print("Press any key to EXIT")
            ch=int(input("Enter Choice: "))

            #to correct the name
            if ch==1:
                name=input("Enter corrected name: ")
                cur.execute("update cust_det set name='{}' where acctno={}".format(name,num))
                con.commit()
                print("The name has been updated.")

            #to update the mail
            elif ch==2:
                email=input("Enter corrected email: ")
                cur.execute("update cust_det set email='{}' where acctno={}".format(email,num))
                con.commit()
                print("The email has been updated.")

            elif ch==3:
                Gname=input("Enter Father's name: ")
                cur.execute("update cust_det set Gname='{}' where acctno={}".format(Gname,num))
                con.commit()
                print("The name has been updated.")

            #to change the address
            elif ch==4:
                print("This section includes: Complete Address")
                print("Address, City, State, pin-code")
                Ad=input("Enter Address: ")
                City=input("Enter City: ")
                State=input("Enter State: ")
                Pin=input("Enter Pin-Code(6): ")
                cur.execute("update cust_det set Ad='{}' where acctno={}".format(Ad,num))
                con.commit()
                cur.execute("update cust_det set City='{}' where acctno={}".format(City,num))
                con.commit()
                cur.execute("update cust_det set State='{}' where acctno={}".format(State,num))
                con.commit()
                cur.execute("update cust_det set pin={} where acctno={}".format(Pin,num))
                con.commit()
                print("The Address has been updated.")

            else:
                print("The details has been updated.")
                break
            break
        

#DELETING AN ACCOUNT#
    elif n==6:
        delete(num)
        print("Hope to see you again.")
        print("Good Bye!!")
        break


#QUIT
    elif n==7: 
        print("Thank You!!Visit us again")
        break
    
    else:
        print("Invalid operation")
        continue
