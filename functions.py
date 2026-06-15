from db import connection 
import pandas as pd
from model_schemas import user_data
from security import user_password,verify,password_to_hash
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
    print(f"\n{'='*60}")
    print(f"{' '*25}ENTER YOUR DETAILS ")
    
    name = input("ENTER YOU FULL NAME ")
    father_name = input('ENTER YOUR FATHERS NAME ')
    mother_name = input('ENTER YOUR MOTHERS NAME ')
    phone_no = (input("ENTER YOUR MOBILE NUMBER "))
    city = input("ENTER THE CITY YOU LIVE IN ")
    aadhar = (input("PLEASE ENTER YOUR AADHAR CARD NUMBER "))

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
        print("YOU HAVE ENTERED WRONG DETAILS ")
        print("ENTER 1 TO EXIT  ")
        print("ENTER 2 TO AGAIN TO ENTER DETAILS ")

        choice = int(input('ENTER YOUR CHOICE '))

        match(choice):
            case 1:
                print("\nEXITED SUCCESSFULLY\n")
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
   
    print("YOU HAVE CREATED YOUR ACCOUNT SUCCESSFULLY ")
    print("YOUR LOGIN ID WILL BE FIRST 6 CHAR OF YOUR AADHAR CARD ")

    password = input("ENTER YOU PASSWORD ")

    try:
        password = user_password(p=password)

    except Exception as e:
      print(e)
      raise ValueError("PASSOWORD IS NOT CORRECT ")

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

    print("\nWE HAVE REGISTERED YOUR LOGIN ID AND PASSWORD USE IT TO LOGIN TO YOUR ACCOUNT\n")

   
    conn.commit()

    return
def my_account():
  print(f"{'='*60}")
  
  print(f"{' '*25}LOGIN PAGE ")
  print("\nPLEASE ENTER YOUR CREDENTIALS TO LOGIN INTO YOUR ACCOUNT\n")
  login_id=int(input("ENTER YOUR LOGIN ID "))
  password=input("ENTER YOUR PASSWORD ")
  if(not check_login_id(login_id)):
    print('\nYOU HAVE ENTERED A INVALID LOGIN ID\n ')
    print("ENTER 1 TO EXIT")
    print("\nENTER 2 TO CONTINUE ENTERING DATA\n")
    choice=int(input("enter a choice "))
    match(choice):
      case 1:
       exit(1)
      case 2:
       my_account()
  try:
      password=user_password(p=password)
  except Exception as e:
      print("YOU HAVE NOT ENTERED A VALID PASSWORD ")
      print("ENTER 1 TO EXIT")
      print("ENTER 2 TO CONTINUE ENTERING DATA")
      choice=int(input("ENTER A CHOICE "))
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
    print("\nTHE GIVEN ID DOES NOT EXISTS INT THE DATABASE\n")
    my_account()

  if verify(record[1],password.p):
    print("\n\nYOU HAVE BEEN GIVEN ACCES TO THE ACCOUNT\n\n ")
    
    given_access(record[2])
    
  else:
    print("PASSWORD IS WRONG ")
    message='''\nPRESS 1 FOR THE EXIT 
PRESS 2 FOR AGAIN ENTERING CREDENTIALS\n'''
    print(message)
    choice=int(input("ENTER YOUR CHOICE "))

    match(choice):
      case 1:
       
       exit(1)
      case 2:
        my_account()
      case _:
        print("ENTER A VALID CHOICE ")
        my_account()


def account_info(aadhar:int):
    aadhar=int(aadhar)
    query='''
    select * from user_data where aadhar=%s;

    ''' 
    cursor.execute(query,(aadhar,))
    row=cursor.fetchone()
    print(f"\n\n{'='*60}")
    print(f"{' '*25}ACCOUNT INFORMATION")
    print(f"NAME:{row[0]}")
    print(f"FATHER_NAME:{row[1]}")
    print(f'MOTHER_NAME:{row[2]}')
    print(f'PHONE_NO:{row[3]}')
    print(f'CITY:{row[4]}')
    print(f'AADHAR:{row[5]}')
    print("PRESS 1 TO EXIT ")
    print("PRESS 2 TO GO BACK TO MENU ")
    choice=int(input("ENTER YOUR CHOICE "))
    match(choice):
     case 1:
      exit(0)
     case 2:
      given_access(aadhar)
     case _:
      print('YOU HAVE ENTERED A WRONG CHOICE SO YOU ARE BEING LOGINED OUT ')
def balance(aadhar:int):
  query=f'''
  select balance from user_data where aadhar=%s;
  '''
  cursor.execute(query,(aadhar,))
  print(f"\n\n{'='*60}")
  print(f"{' '*25}BALANCE ENQUIRY\n")
  print(f'YOUR BALANCE IS {cursor.fetchone()[0]}')
  print("WE ARE REDIRECTING YOU BACK TO ORIGNAL MENU ")
  given_access(aadhar)

def deposit(aadhar:int):
  print(f"\n\n{'='*60}")
  print(f"{' '*25}DEPOSIT IN BANK\n\n")
  print("ENTER THE AMOUNT YOU WANT TO DEPOSIT IN YOUR ACCOUNT ")
  amount=None
  while(1):
    amount=float(input("ENTER AMOUNT "))
    if(amount<=0):
      print("DONT ENTER NEGATIVE AMOUNT ")
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
    print('MONEY HAS BEEN CREDITED SUCCESFULLY ')
    print(f"YOU NEW BALANCE IS {bal}")

  except Exception as e :
    print(e)
    conn.rollback()
    print("\n\nTRANSACTION IS ABORTED \n\n")
    given_access(aadhar)
def withdrawl(aadhar:int):
    
    print(f"\n\n{'='*60}")
    print(f"{' '*25}WITHDRWAWL SYSTEM")
    amount=None
    bal=None
    query='''
    select balance from user_data where aadhar=%s;
      '''
    cursor.execute(query,(aadhar,))
    bal=cursor.fetchone()[0]
    while(1):
        
        amount=float(input("ENTER THE AMOUNT TO BE WITHDRAW "))
        if(amount<0):
          print('DONT ENTER NEGATIVE AMOUNt ')
          continue
        elif(amount>bal):
          print(f"INSUFFICIENT BALLANCE PLEASE ENTER LESS THAN {bal}");
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
        print("YOU MONEY HAS BEEN WITHDRAWED ")
        print(f'YOUR CURRENT BALANCE IS {bal-amount}')
        print("\nWE ARE REDIRECTING YOU TO THE MAIN MENU\n\n\n ")
        given_access(aadhar)

    except:
        conn.rollback()
        print("TRANSACTION HAS BEEN ABORTED WE ARE REDIRECTING YOU TO MAIN MENU")
        given_access(aadhar)
def transfer_money(aadhar:int):
  cursor.execute('select balance from user_data where aadhar=%s',(aadhar,))
  bal=cursor.fetchone()[0]
  print(f"\n\n{'='*60}")
  print(f"{' '*25}ACCOUNT INFORMATION")
  amount=float(input("ENTER AMOUNT TO   BE SENT "))
  if (amount>bal):
    print("INSUFFICIENT BALANCE ")
    given_access(aadhar)
  aadhar2=int(input('ENTER AADHAR OF PERSON YOU WANT TO SEND MONEY TO '))
 
  cursor.execute('select * from user_data where aadhar=%s',(aadhar2,))
  if(cursor.fetchone() is None):
    print("THE GIVEN AADHAR IS NOT FOUND\n\n ")
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
    print("transaction has been aborted \n\n\n")
    given_access(aadhar)
def last_five(aadhar:int):
  print(f"\n\n{'='*60}")
  print(f"{' '*25}LAST  FIVE TRANSACTIONS ")
  query='select trans_id,time,debit,credit,balance from transaction where aadhar=%s order by time desc limit 5;'
  cursor.execute(query,(aadhar,))
  data=cursor.fetchall()
  if data==[]:
    print("THERE ARE NO TRANSACTIONS AVAIALBLE \n\n\n")
    print("WE ARE REDIRECTING YOU TO THE MAIN MENU\n\n\n")
    given_access(aadhar)
  data=pd.DataFrame(data,columns=['TRANS_ID','TIME','DEBIT','CREDIT','BALANCE'])
  print(data)
  print('WE ARE REDIRECTING YOU TO MAIN MENU\n\n\n\n')
  given_access(aadhar)

def given_access(aadhar:int):
  print(f"\n\n{'='*60}")
  print(f"{' '*25}WELCOME USER ")
 
  print("YOU HAVE BEEN LOGINED IN ")
  print("PLEASE ENTER ONE OF THE CHOICES BELOW ")
  while(1):
    print("press 1 for MY ACCOUNT INFORMATION ")
    print("press 2 for FOR BALANCE ")
    print("press 3 for TRANSFER MONEY TO OTHER BANK ACCOUNT ")
    print("press 4 for DEPOSIT MONEY ")
    print("press 5 for WITHDRAWL OF MONEY ")
    print("PRESS 6 FOR LAST 5 TRANSACTIONS ")

    print("PRESS 7 FOR EXIT\n\n ")
    choice=int(input("ENTER YOUR CHOICE "))
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
      print("PLEASE ENTER A VALID CHOICE\n\n\n ")
      given_access(aadhar)
      
def all_users():
  query='select name,aadhar,balance from user_data'
  cursor.execute(query)
  data=cursor.fetchall()
  data=pd.DataFrame(data,columns=['NAME','AADHAR','BALANCE'])
  print(data)

  return 
