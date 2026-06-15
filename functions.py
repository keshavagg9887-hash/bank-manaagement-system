from db import connection 
try: 
    
  conn=connection()
  cursor=conn.cursor()
except:
    print("connection failed") 
    exit(1)

def check_login_id(login_id):
    if(login_id>0 and len(str(login_id))==6): return 1
    else:return 0
def register_new():
    print("please enter your details below ")
    name = input("enter you full name ")
    father_name = input('enter your fathers name')
    mother_name = input('enter your mothers name')
    phone_no = (input("enter your mobile number"))
    city = input("enter the city you live in ")
    aadhar = (input("please enter your aadhar card number"))

    data = {
        'name': name,
        'fname': father_name,
        'mname': mother_name,
        'phone_no': phone_no,
        'city': city,
        'aadhar': aadhar
    }

    try:
        data = user_data(**data)

    except Exception as e:
        print(e)
        print("you have entered wrong details")
        print("enter 1 to exit ")
        print("enter 2 to again to enter details ")

        choice = int(input('enter your choice '))

        match(choice):
            case 1:
                print("exited successfully")
                exit(1)

            case 2:
                register_new()

            case _:
                print("enter a valid choice ")
                register_new()

    query = """
    INSERT INTO user_data
    VALUES (%s,%s,%s,%s,%s,%s,0,current_timestamp) on conflict do nothing;
    """

    cursor.execute(
        query,
        (
            data.name,
            data.fname,
            data.mname,
            data.phone_no,
            data.city,
            data.aadhar
        )
    )
   
    print("you have created your account successfully ")
    print("your login id will be first 6 char of your aadhar card ")

    password = input("enter you password")

    try:
        password = user_password(p=password)

    except Exception as e:
      print(e)
      raise ValueError("passoword is not correct ")

    password = password_to_hash(password.p)

    query = '''
    insert into id_pass values(%s,%s,%s) on conflict do nothing;
    '''
   
    cursor.execute(
        query,
        (
            
            str(data.aadhar)[:6],
            password,
            data.aadhar
        )
    )
    conn.commit()

    print("we have registered your login id and password use it to login to your account")

   
    conn.commit()

    return
def my_account():
  print("LOGIN PAGE ")
  print("please enter your credentials to login into your account")
  login_id=int(input("enter your login id "))
  password=input("enter your password ")
  if(not check_login_id(login_id)):
    print('you have entered a invalid login id ')
    print("enter 1 to exit")
    print("enter 2 to continue entering data")
    choice=int(input("enter a choice "))
    match(choice):
      case 1:
       exit(1)
      case 2:
       my_account()
  try:
      password=user_password(p=password)
  except Exception as e:
      print("you have not entered a valid password ")
      print("enter 1 to exit")
      print("enter 2 to continue entering data")
      choice=int(input("enter a choice "))
      match(choice):
        case 1:
         exit(1)
        case 2:
         my_account()
  # now we have to verify it this id exists in data base or not
  # if exists then we have to move it to my account _menu
  # if not exist we will give return
  # if password is wrong we will return
  query='''
 select * from  id_pass where loginid =%s;

  '''
  cursor.execute(query,(login_id,))


  record=cursor.fetchone()
  if record==None:
    print("the given id does not exists int the database")
    my_account()

  if verify(record[1],password.p):
    print("you have been given acces to the account ")
    
    given_access(record[2])
    
  else:
    print("password is wrong ")
    message='''press 1 for the exit 
    press 2 for again entering credentia'''
    print(message)
    choice=int(input("enter your choice "))

    match(choice):
      case 1:
       
       exit(1)
      case 2:
        my_account()
      case _:
        print("enter a valid choice ")
        my_account()


def account_info(aadhar:int):
    aadhar=int(aadhar)
    query='''
    select * from user_data where aadhar=%s;

    ''' 
    cursor.execute(query,(aadhar,))
    row=cursor.fetchone()
    print(f"NAME:{row[0]}")
    print(f"FATHER_NAME:{row[1]}")
    print(f'MOTHER_NAME:{row[2]}')
    print(f'PHONE_NO:{row[3]}')
    print(f'CITY:{row[4]}')
    print(f'AADHAR:{row[5]}')
    print("press 1 to exit ")
    print("press 2 to go back to menu ")
    choice=int(input("enter your choice "))
    match(choice):
     case 1:
      exit(0)
     case 2:
      given_access(aadhar)
     case _:
      print('you have entered a wrong choice so you are being logined out ')
def balance(aadhar:int):
  query=f'''
  select balance from user_data where aadhar=%s;
  '''
  cursor.execute(query,(aadhar,))
  
  print(f'YOUR BALANCE IS {cursor.fetchone()[0]}')
  print("we are redirecting you back to orignal menu ")
  given_access(aadhar)
def deposit(aadhar:int):
  print("enter the amount you want to deposit in your account ")
  amount=None
  while(1):
    amount=float(input("ENTER AMOUNT "))
    if(amount<=0):
      print("dont enter negative amount ")
      continue
    else:break
  query1=''' 
  update user_data set balance=balance+%s where aadhar=%s returning balance;
  '''
  query2='''
  insert into transaction(aadhar,credit,debit,balance) values
  (
 %s,
 %s,
 0,
 %s
  )
  '''
  try :
    cursor.execute(query1,(amount,aadhar))
    bal=cursor.fetchone()[0]
    cursor.execute(query2,(aadhar,amount,bal))
    conn.commit()
    print('money has been credited succesfully ')
    print(f"you new balance is {bal}")

  except Exception as e :
    print(e)
    conn.rollback()
    print("transaction is aborted ")
    given_access(aadhar)
def withdrawl(aadhar:int):
    
  
    amount=None
    bal=None
    query='''
    select balance from user_data where aadhar=%s;
      '''
    cursor.execute(query,(aadhar,))
    bal=cursor.fetchone()[0]
    while(1):
        
        amount=float(input("enter the amount to be withdraw "))
        if(amount<0):
          print('dont enter negative amount ')
          continue
        elif(amount>bal):
          print(f"insufficient ballance please enter less than {bal}");
          continue
        else: break
    query1='''
      update user_data set balance=%s where aadhar=%s returning balance; 
      '''
    query2='''
      insert into transaction(aadhar,credit,debit,balance) values(%s,0,%s,%s);
      '''
    try :
        cursor.execute(query1,(bal-amount,aadhar))
        cursor.execute(query2,(aadhar,amount,bal-amount))
        conn.commit()
        print("you money has been withdrawed ")
        print(f'your current balance is {bal-amount}')
        print("we are redirecting you to the main menu ")
        given_access(aadhar)

    except:
        conn.rollback()
        print("transaction has been aborted we are redirecting you to main menu")
        given_access(aadhar)
def transfer_money(aadhar:int):
  cursor.execute('select balance from user_data where aadhar=%s',(aadhar,))
  bal=cursor.fetchone()[0]
  
  amount=float(input("enter amount to   be sent "))
  if (amount>bal):
    print("insufficient balance ")
    given_access(aadhar)
  aadhar2=int(input('enter aadhar of person you want to send money to '))
 
  cursor.execute('select * from user_data where aadhar=%s',(aadhar2,))
  if(cursor.fetchone() is None):
    print("the given aadhar is not found ")
    given_access(aadhar)
  cursor.execute('select balance from user_data where aadhar=%s',(aadhar2,)) 
  bal2=cursor.fetchone()[0]
  
  query1='update user_data set balance=balance-%s where aadhar=%s;'
  query2='insert into transaction(aadhar,credit,debit,balance) values(%s,0,%s,%s);'
  query3='update user_data set balance=balance+%s where aadhar=%s;'
  query4='insert into transaction(aadhar,credit,debit,balance) values(%s,%s,0,%s);'
  try:
    cursor.execute(query1,(amount,aadhar))
    cursor.execute(query2,(aadhar,amount,bal-amount))
    cursor.execute(query3,(amount,aadhar2))
    cursor.execute(query4,(aadhar2,amount,bal2+amount))
    conn.commit()
    print('THE TRANSACITON HAS BEEN SUCCESFULL\n')
    print(f'YOUR NEW BALANCE IS {bal-amount}')
  except:
    conn.rollback()
    print("transaction has been aborted ")
    given_access(aadhar)
def last_five(aadhar:int):
  query='select trans_id,time,debit,credit,balance from transaction where aadhar=%s order by time desc limit 5;'
  cursor.execute(query,(aadhar,))
  data=cursor.fetchall()
  if data==[]:
    print("THERE ARE NO TRANSACTIONS AVAIALBLE \n\n\n")
    print("WE ARE REDIRECTING YOU TO THE MAIN MENU")
    given_access(aadhar)
  data=pd.DataFrame(data,columns=['TRANS_ID','TIME','DEBIT','CREDIT','BALANCE'])
  print(data)
  print('we are redirecting you to main menu\n\n\n\n')
  given_access(aadhar)

def given_access(aadhar:int):
  print(f"welcome user {aadhar}")
  print("you have been logined in ")
  print("please enter one of the choices below ")
  while(1):
    print("press 1 for MY ACCOUNT INFORMATION ")
    print("press 2 for FOR BALANCE ")
    print("press 3 for TRANSFER MONEY TO OTHER BANK ACCOUNT ")
    print("press 4 for DEPOSIT MONEY ")
    print("press 5 for WITHDRAWL OF MONEY ")
    print("press 6 for last 5 transactions ")

    print("press 7 for exit ")
    choice=int(input("enter your choice "))
    match(choice):
     case 1:
      account_info(aadhar)
     case 2:
      balance(aadhar)
     case 3:
      transfer_money(aadhar)
     case 4:
      deposit(aadhar)
     case 5:
      withdrawl(aadhar)
     case 6:
      last_five(aadhar)

     case 7:
      exit(0)
     case _:
      print("please enter a valid choice ")
      given_access(aadhar)
      
def all_users():
  query='select name,aadhar,balance from user_data'
  cursor.execute(query)
  data=cursor.fetchall()
  data=pd.DataFrame(data,columns=['NAME','AADHAR','BALANCE'])
  print(data)

  return 

if cursor is not None:
  cursor.close()
if conn is not None:
  conn.close()