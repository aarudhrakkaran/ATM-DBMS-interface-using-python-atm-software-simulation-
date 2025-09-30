import mysql.connector as sql
conn=sql.connect(host='localhost',user='root',password='manager',database='  ATM_MACHINE')
if conn.is_connected():
      print("sucessfully connected")
c1=conn.cursor()
mn="CREATE TABLE RECORDS( ACCONT_NO  INT(4) primary key,PASSWORD INT(3),NAME VARCHAR(20),CR_AMT INT default(0),WITHDRAWL INT default(0),BALANCE INT default(0))"
c1.execute(mn)
print("Sucessfulluy created")
