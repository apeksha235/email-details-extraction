from datetime import datetime
import imaplib, email, os
import traceback
from imbox import Imbox
from pymongo import MongoClient
import gridfs
import mysql.connector
import re

##### EXTRACTING THE BODY ######
with Imbox('imap.gmail.com',
        username='apeksha05hegde@gmail.com',
        password='',
        ssl=True,
        ssl_context=None,
        starttls=False) as imbox:
        inbox = imbox.messages(unread=True,sent_from='')
        download_folder = r" "

        if not os.path.isdir(download_folder):
          os.makedirs(download_folder, exist_ok=True)


        for uid,message in inbox:

          message.sent_from
          message.sent_to
          message.subject
          message.headers
          message.message_id
          message.date
          message.body
          message.attachments

          s=message.body

          text=str(s['plain'][0])
          l=text.split()
          element='number:'
          n=l.index(element)
          invoice=int(l[6])
          date=l[3]
          bi=[]
          order=""
          for i in l[9:]:
            if(i=='Billing'):
              break;
            bi.append(i)
          for e in bi:
            order=order+e+" "
          li=[]
          address=" "
          for i in l[12:]:
            if(i=='--'):
              break;
            li.append(i)
          for e in li:
            address=address+e+" "
          company=l[0]
#### DOWNLOADING THE ATTACHMENT ALONG WITH THE EMAIL ####
          for idx, attachment in enumerate(message.attachments):
             try:
              att_fn = attachment.get('filename')
              download_path = f"{download_folder}/{att_fn}"
              print(download_path)
              with open(download_path, "wb") as fp:
                fp.write(attachment.get('content').read())
             except:
               print(traceback.print_exc())

connection = mysql.connector.connect(host='localhost',
                                         database='proj_db',
                                         user='root',
                                         password='apek_sql')
mycursor = connection.cursor(prepared=True)
sql = "INSERT INTO details (company, dates, invoice,address,items) VALUES (?,?,?,?,?) "
val=(company,date,invoice,address,order)
mycursor.execute(sql,val)
connection.commit()
mycursor.close() 
connection.close()

#### DOWNLOADING THE ATTACHMENT ALONG WITH THE EMAIL ####
conn=MongoClient(host="127.0.0.1",port=27017)
db=conn.mydb
filedata=open(att_fn,"rb")
data=filedata.read()
fs=gridfs.GridFS(db)
fs.put(data,filename=att_fn)
print("DONE")
