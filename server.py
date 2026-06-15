import psycopg2 as connector
from model_schemas import user_data
from security import user_password,verify,password_to_hash
from psycopg2.extras  import DictCursor
import pandas as pd
from db import connection
from functions import check_login_id,register_new,my_account,account_info,balance,deposit,withdrawl,transfer_money,last_five,given_access,all_users
conn=None
cursor=None
try:
  conn=connection()
  cursor=conn.cursor()
  query='''
  create table if not exists id_pass(
  loginid  int,
  password text,
  aadhar bigint primary key
  );
   '''
  cursor.execute(query)
  conn.commit()
  query='''
        create table if not exists user_data(
        name varchar not null,
        fname varchar not null,
        mname varchar not null,
        phone bigint not null,
        city varchar not null,
        aadhar bigint primary key,
        balance int default 0,
        time_of_creation timestamp default current_timestamp

        );
        '''
  cursor.execute(query)
  conn.commit()
  query='''
  create table if not exists transaction(
  trans_id bigserial primary key  ,
  time timestamp default current_timestamp,
  aadhar bigint not null ,
  credit real not null ,
  debit real not null ,
  balance real not null,
  foreign key(aadhar) references user_data(aadhar)
  );

  '''
  cursor.execute(query)
  conn.commit()
except Exception as e:
    print("connection failed")
    print(e)
    exit(1)
print("WELCOME TO BANK MANAGEMENT SYSTEM")
while(1):
    print("ENTER 1 FOR MY ACCOUNT")
    print("ENTER 2 FOR REGISTERING NEW ACCOUNT")
    print("ENTER 3 FOR SEEING ALL THE USERS")
    print("ENTER 4 FOR EXIT")
    choice=int(input("ENTER YOUR CHOICE"))
    match(choice):
     case 1:
        my_account()
        continue
     case 2:
        register_new()
        continue

     case 3:
        all_users()
        continue
     case 4:
       exit(1)
     case _:
        print("please enter a valid choice")
        continue
if cursor is not None:
  cursor.close()
if conn is not None:
  conn.close()