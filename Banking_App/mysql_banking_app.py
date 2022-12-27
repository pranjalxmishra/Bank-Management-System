import mysql.connector 
import pandas as pd 
import random
from termcolor import colored

mydb = mysql.connector.connect(host  = "localhost",user = 'pranjal',passwd = 'root512',database ='bank_manage')
mycursor = mydb.cursor()
mycursor.execute('select * from details')
data = mycursor.fetchall()

df = pd.DataFrame(data,columns= ['Account_Number', 'Name', 'Address', 'Phone_Number', 'Aadhaar_No', 'Amount', 'Password'])

def update_data(info):
  choice = int(input('\nEnter 0 to update Name\nEnter 1 to update Address\nEnter 2 to update Phone_Number\nEnter 3 to update Password : '))

  if choice == 0:
    new_name = input("\nEnter the new Name : ")
    df["Name"] = df["Name"].replace(info[1],new_name)
    print('Name updated successfully !')


  elif choice == 1:
    new_address = input("\nEnter your new Address : ")
    df["Address"] = df["Address"].replace(info[2],new_address)
    print('Name updated successfully !')

  elif choice == 2 :
    new_number = input("\nEnter your new Phone_Number : ")
    df["Phone_Number"] = df["Phone_Number"].replace(info[3],new_number)
    print('Name updated successfully !')

  elif choice == 3 :
    pasw = int(input('Enter your new password (only digits) : '))
    confirm_pasw = int(input('Confirm your password : '))
    while True:
      if pasw != confirm_pasw:
        text = colored('Passwords not matching', "red")
        pasw = int(input('\nCreate your password : '))
        confirm_pasw = int(input('Confirm your password : '))
      else:
        break
    df["Password"] = df["Password"].replace(info[6],pasw)
    print('Password updated successfully !')


def remove_user(acc_no):
  global df
  while True:
    acc = [int(i) for i in df["Account_Number"]]
    if acc_no not in acc:
        text = colored("Account Number not found, Please try again!",'red')
        print(text)
    else:
        break
  choice = input('Are you sure you want to delete your account [y/n] : ')
  if choice == 'y':
    df.drop(acc.index(acc_no),axis=0,inplace = True)
    text = colored(f'Account with account number {acc_no} is removed.','red')
    print(text)

def new_user():
  global df
  
  acc_no = random.randint(10000,99999)
  while True:
    if acc_no in [int(i) for i in df["Account_Number"]]:
      acc_no = random.randint(10000,99999)
    else:
      break

  Account = acc_no
  name = input("\nEmter your name : ")  
  address = input("Enter your address : ")
  phone_num = int(input("Enter your phone number : "))
  aadhaar = input("Enter your Aadhaar Number : ")
  amount = int(input("Enter your amount : "))
  pasw = int(input('Create your password (only digits) : '))
  confirm_pasw = int(input('Confirm your password : '))

  while True:
    if pasw != confirm_pasw:
      text = colored('Passwords not matching', "red")
      pasw = int(input('\nCreate your password : '))
      confirm_pasw = int(input('Confirm your password : '))
    else:
      break

  new_user_input = [Account,name,address,phone_num,aadhaar,amount,pasw]
  a_series = pd.Series(new_user_input, index = df.columns)
  df = df.append(a_series, ignore_index=True) 
  text = colored(f"\nYour details are added successfully.\nYour account number is {acc_no}\nPlease don't lose it.", 'red')
  print(text)


def existing_user():
  global df
  acc_no = int(input("\nEnter your Account Number : "))
  password = int(input('Enter your password : '))
  while True:
    if acc_no not in [int(i) for i in df[df.columns[0]]]:
      acc_no = int(input("Not found. Please enter your correct account number: "))
    elif acc_no == 'q':
      quit()
    else:
      break 


  info = list(df[df["Account_Number"] == acc_no].values[0])
  while True:
    if info[6] != password:
      password = int(input('Wrong password! Please enter correct password : '))
    else:
      break

  text = colored(f"{info[1]}",'red',attrs=['bold'])
  print(f'\nWelcome, {text}!')

  while True:
    print('------------------------------------------------------------------------------------')
    n = int(input("Enter 0 to update your information.\nEnter 1 to check your information.\nEnter 2 to withdraw an amount.\nEnter 3 to deposit an amount.\nEnter 4 to close your account\nEnter 5 to quit your account : ")) 
    valid = [1,2,3,4,0,5]

    while True:
      if n not in valid:
        n = int(input("Invalid input! \nEnter 0 to update your information.\nEnter 1 to check your information.\nEnter 2 to withdraw an amount.\nEnter 3 to deposit an amount.\nEnter 4 to close your account : "))
      else:
        break

    if n == 0:
      update_data(info)

    elif n == 1:
      layout = f"""
+------------------+----------------+-------------------+
  Account_Number   | {info[0]}
  Name             | {info[1]}
  Address          | {info[2]}
  Phone_Number     | {info[3]}
  Aadhaar_No       | {info[4]}
  Amount           | {info[5]}
+------------------+----------------+-------------------+
      """
      print(layout)

    elif n == 2:
      am = int(input("\nEnter the amount to be withdrawn: "))
      if am <= info[5]:
        amount = info[5]
        print("Withdrawal successful.\nAvailable Balance: ",info[5] - am)
        df["Amount"] = df["Amount"].replace(amount,amount-am)
      else:
        print("Insufficient balance.\nAvailable balance: ",info[5])

    elif n == 3:
      dm = int(input("\nEnter the amount to be deposited: "))
      # amount = df.loc[[int(i) for i in df[df.columns[0]]].index(acc_no),"Amount"]
      amount = info[5]
      info[5] = info[5] + dm
      df["Amount"] = df["Amount"].replace(amount,amount+dm)
      print("Deposit successful.\nAvailable Balance: ",info[5])
    
    elif n == 4:
      remove_user(acc_no)
      break
      
    else: 
      break
  print('------------------------------------------------------------------------------------')
  


def main():
  while True:
    valid_entries = [1,2,3,0]
    option = int(input("\n\nEnter 1 if you are a new customer.\nEnter 2 if you are an existing customer.\nEnter 3 to terminate the application. : "))
    while True :
      if option not in valid_entries:
        option = int(input("Invalid input!\n\nEnter 1 if you are a new customer.\nEnter 2 if you are an existing customer.\nEnter 3 to terminate the application : "))
      else:
        break
    if option == 0:
      print(df)
      break

    elif option == 1:
      new_user()
      break

    elif option == 2 :
      existing_user()  
      break 

    elif option == 3:
      print("\nThank you, for banking with us!")
      mycursor.execute('truncate table details')
      data = []
      for i in df.values:
        data.append(tuple(i))
      insdata = "insert into details values(%s,%s,%s,%s,%s,%s,%s)"
      mycursor.executemany(insdata,data)
      mydb.commit()
      quit()

text = colored("\t\tWelcome to the Reserve Bank of India!",'yellow', attrs=['dark'])
print(text)
while True:
	main()
    

 