import mysql.connector as sql

def main_menu():
    print("=================================^_^============================")
    print("================WELCOME==TO==KARAN'S==ATM================")
    print("=================================^_~===========================================")
    print("1. Create account")
    print("2. Login")
    print("3. Exit")
    print("================================================================================")

def log_transaction(c1, conn, acct, txn_type, amount):
    """Function to insert transactions into the database"""
    q = "select balance from records where ACCONT_NO={}".format(acct)
    c1.execute(q)
    bal = c1.fetchone()[0]
    ins = "insert into transactions(account_no, type, amount, balance) values({}, '{}', {}, {})".format(acct, txn_type, amount, bal)
    c1.execute(ins)
    conn.commit()

while True:
    conn=sql.connect(host='localhost',user='root',password='aarudh123',database='atm_bank')
    c1=conn.cursor()
    main_menu()
    op=int(input("Enter your choice : "))
    print("================================================================================")

    if op==1:
        c="y"
        while c=="y":
            m=int(input("Enter a 4 digit number as account number:"))
            cb="select * from records where ACCONT_NO={}".format(m)
            c1.execute(cb)
            d=c1.fetchall()
            data=c1.rowcount
            if data==1:
                print("This account number already exists.")
                c=input("Do you want to continue y/n - ")
                if c.lower()!="y":
                    break
            else:
                name=input("Enter your name: ")
                passw=int(input("Enter your password: "))
                ab="insert into records(ACCONT_NO,PASSWORD,NAME,CR_AMT,WITHDRAWL,BALANCE) values({},{},'{}',0,0,0)".format(m,passw,name)
                c1.execute(ab)
                conn.commit()
                print("Account successfully created!")
                s=int(input("Enter the money to be deposited : "))
                sr="update records set CR_AMT={} where ACCONT_NO={}".format(s,m)
                c1.execute(sr)
                conn.commit()
                ef="update records set balance=CR_AMT-WITHDRAWL where ACCONT_NO={}".format(m)
                c1.execute(ef)
                conn.commit()
                print("Successfully deposited.")
                log_transaction(c1, conn, m, "Deposit", s)  # 🔹 Log initial deposit
                break

    elif op==2:
        y="y"
        while y=="y":
            acct=int(input("Enter your account number: "))
            cb="select * from records where ACCONT_NO={}".format(acct)
            c1.execute(cb)
            c1.fetchall()
            data=c1.rowcount
            if data==1:
                pas=int(input("Enter your password  : "))
                e="select password from records where ACCONT_NO={}".format(acct)
                c1.execute(e)
                a=c1.fetchone()
                d=list(a)
                if pas==d[0]:
                    print("Login Successful ✅")
                    print("1. Depositing money")
                    print("2. Withdrawing money")
                    print("3. Transferring money")
                    print("4. Checking balance")
                    print("5. Deleting account")
                    print("6. Logout")
                    print("7. Transaction History")  # 🔹 New Option
                    r=int(input("Enter your choice: "))
                    print("================================================================================")

                    if r==1:
                        amt=int(input("Enter the money to be deposited: "))
                        sr="update records set CR_AMT=CR_AMT + {} where ACCONT_NO={}".format(amt,acct)
                        c1.execute(sr)
                        conn.commit()
                        ef="update records set balance=CR_AMT-WITHDRAWL where ACCONT_NO={}".format(acct)
                        c1.execute(ef)
                        conn.commit()
                        print("Successfully deposited.")
                        log_transaction(c1, conn, acct, "Deposit", amt)

                    elif r==2:
                        amt=int(input("Enter the money to withdraw: "))
                        ah="select BALANCE from records where ACCONT_NO={}".format(acct)
                        c1.execute(ah)
                        m=c1.fetchone()
                        if amt > m[0]:
                            print("Insufficient Balance ❌")
                        else:
                            sr="update records set balance=balance - {} where ACCONT_NO={}".format(amt,acct)
                            ed="update records set WITHDRAWL=WITHDRAWL+{} where ACCONT_NO={}".format(amt,acct)
                            c1.execute(ed)
                            c1.execute(sr)
                            conn.commit()
                            print("Successfully withdrawn.")
                            log_transaction(c1, conn, acct, "Withdraw", amt)

                    elif r==3:
                        act=int(input("Enter the account number to transfer to: "))
                        cb="select * from records where ACCONT_NO={}".format(act)
                        c1.execute(cb)
                        c1.fetchall()
                        data=c1.rowcount
                        if data==1:
                            m=int(input("Enter the money to be transferred : "))
                            ah="select BALANCE from records where ACCONT_NO={}".format(acct)
                            c1.execute(ah)
                            c=c1.fetchone()
                            if m > c[0]:
                                print("Insufficient balance ❌")
                            else:
                                av="update records set balance=balance-{} where ACCONT_NO={}".format(m,acct)  
                                cv="update records set balance=balance+{} where ACCONT_NO={}".format(m,act)
                                w="update records set withdrawl=withdrawl+{} where ACCONT_NO={}".format(m,acct)
                                t="update records set CR_AMT=CR_AMT+{} where ACCONT_NO={}".format(m,act)
                                c1.execute(av)
                                c1.execute(cv)
                                c1.execute(w)
                                c1.execute(t)
                                conn.commit()
                                print("Successfully transferred ✅")
                                log_transaction(c1, conn, acct, "Transfer Out", m)
                                log_transaction(c1, conn, act, "Transfer In", m)
                        else:
                            print("Target account does not exist ❌")

                    elif r==4:
                        ma="select balance from records where ACCONT_NO={}".format(acct)
                        c1.execute(ma)
                        k=c1.fetchone()
                        print("Your account Balance = ",k[0])

                    elif r==5:  # Delete Account
                        confirm=input("Are you sure you want to delete this account? (y/n): ")
                        if confirm.lower()=="y":
                            del_query="delete from records where ACCONT_NO={}".format(acct)
                            c1.execute(del_query)
                            conn.commit()
                            print("Account deleted successfully ❌")
                            break
                        else:
                            print("Account deletion cancelled.")

                    elif r==6:  # Logout
                        print("Logged out. Returning to main menu...")
                        break

                    elif r==7:  # 🔹 Transaction History
                        print("==== Transaction History ====")
                        q="select type, amount, balance, date from transactions where account_no={} order by date desc limit 10".format(acct)
                        c1.execute(q)
                        rows=c1.fetchall()
                        if rows:
                            for row in rows:
                                print("Type:",row[0], "| Amount:",row[1], "| Balance:",row[2], "| Date:",row[3])
                        else:
                            print("No transactions found.")
                    
                    y=input("Do you want to continue y/n - ")

                else:
                    print("Wrong password ❌")
                    y=input("Do you want to try again y/n - ")
            else:
                print("Your account does not exist ❌")

    elif op==3:
        print("Exiting...")
        c1.close()
        conn.close()
        break







                  
