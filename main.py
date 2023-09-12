import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta
import smtplib
import ssl
from decouple import config

#SMTP variables
smtpServer = config('SMTPSERVER')
port = config('SMTPPORT')
senderEmail = config('SMTPSENDEREMAIL')
recieverEmail = [config('SMTPRECEIVEREMAIL')]
subject = "WARNING: RADIUS MYSQL Replication"
message = f"From: {config('FROM_HEADER')}\nSubject:{subject}\n\n"
context = ssl.create_default_context()
#initialize SMTP
server = smtplib.SMTP(smtpServer, port)
server.starttls(context=context)

try:
    #Make sure to get your connection credentials correct
    db = mysql.connector.connect(
    host=config('SQLSERVER')
    database=config('DBNAME'),
    user=config('DBUSER'),
    password=config('DBPASSWORD'),
    auth_plugin='mysql_native_password',
    )
    if db.is_connected():
        myCursor = db.cursor(buffered=True)
        myCursor.execute("CALL rts_monitor_replication();")
        results = myCursor.fetchall()
        dbTime = results[0][-1]
        print(dbTime)
        now = datetime.now()
        print(now)
        if dbTime < now-timedelta(minutes=5):
            print("Replication is behind")
            currentLag = now-dbTime
            message+= f"WARNING: RADIUS MYSQL Replication \n is behind by {currentLag}"
        db.close()
        server.sendmail(senderEmail, recieverEmail, message)

except Error as e:
    print("Error while connecting to MySQL", e)
    error = e
    message+= f"WARNING: Error while connecting to MySQL RADIUS BACKUP {error}"
    server.sendmail(senderEmail, recieverEmail, message)

finally:
    if datetime.now().strftime("%H:%M") == "08:00":
        subject = "RADIUS MYSQL Replication Heartbeat"
        message = f"From: {config('FROM_HEADER')}\nSubject:{subject}\n\n RADIUS MYSQL Replication Monitor is up and running"
        server.sendmail(senderEmail, recieverEmail, message)
