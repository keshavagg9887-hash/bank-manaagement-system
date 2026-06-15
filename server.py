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
def line():
    print("═" * 50)

def title(text):
    print("\n╔" + "═" * 48 + "╗")
    print(f"║{text:^48}║")
    print("╚" + "═" * 48 + "╝")

def menu_option(num, text):
    print(f"│ {num}. {text:<42}│")

def menu():
    title("BANK MANAGEMENT SYSTEM")

    print("┌" + "─" * 48 + "┐")
    menu_option(1, "My Account")
    menu_option(2, "Register New Account")
    menu_option(3, "See All Users")
    menu_option(4, "Exit")
    print("└" + "─" * 48 + "┘")
while(1):
    menu()

    try:
        choice = int(input("\n➜ Enter your choice : "))
    except ValueError:
        print("\n Please enter a valid number.")
        continue

    match choice:
        case 1:
            my_account()

        case 2:
            register_new()

        case 3:
            all_users()

        case 4:
            print("\n Thank you for using our bank.")
            break

        case _:
            print("\n Invalid choice.")
if cursor is not None:
  cursor.close()
if conn is not None:
  conn.close()
