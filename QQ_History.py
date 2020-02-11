from _overlapped import NULL
import hashlib
import sqlite3
import time

class QQoutput():
    def __init__(self,db,key,mode,s):
        self.key=key    #解密用的密钥
        self.c=sqlite3.connect(db).cursor()
        self.mode=mode
        self.s=s
        
    def fix(self,data,mode):
        #msgdata mode=0
        #other mode=1
        if(mode==0):
            rowbyte=[]
            for i in range(0,len(data)):
                rowbyte.append(data[i]^ord(self.key[i%len(self.key)]))
            rowbyte=bytes(rowbyte)
            try:
                msg=rowbyte.decode(encoding="utf-8")
            except:
                msg=NULL
            return msg
        elif(mode==1):
            str=""
            try:
                for i in range(0,len(data)):
                    str+=chr(ord(data[i])^ord(self.key[i%len(self.key)]))
            except:
                str=NULL
            return str
    def decode(self, cursor):
        for row in cursor:
            continue
        data = row[0]
        MsgEnc = self.s.encode(encoding="utf-8")
        RealKey = ""
        for i in range(0,len(MsgEnc)):
            RealKey+=chr(data[i]^MsgEnc[i])
        return RealKey
    def AddEmoji(self, msg):
        pos = msg.find('\x14')
        while(pos != -1):
            lastpos = pos
            num = ord(msg[pos+1])
            msg = msg.replace(msg[pos:pos+2], "<img src='./gif/"+str(num)+".gif' alt="+str(num)+">")
            pos = msg.find('\x14')
            if(pos == lastpos):
                break
        return msg
    def troop_message(self,num):
        num=str(num).encode("utf-8")
        md5num=hashlib.md5(num).hexdigest().upper()
        execute="select msgData,senderuin,time from mr_troop_{md5num}_New".format(md5num=md5num)
    def message(self,num,mode):
        #mode=1 friend
        #mode=2 troop
        num=str(num).encode("utf-8")
        md5num=hashlib.md5(num).hexdigest().upper()
        if(mode==1):
            execute="select msgData,senderuin,time from mr_friend_{md5num}_New".format(md5num=md5num)
        elif(mode==2):
            execute="select msgData,senderuin,time from mr_troop_{md5num}_New".format(md5num=md5num)
        else:
            print("error mode")
            exit(1)
        cursor = self.c.execute(execute)
        RealKey = self.decode(cursor)
        cursor = self.c.execute(execute)
        allmsg=[]
        for row in cursor:
            msgdata= row[0]
            uin=row[1]
            ltime=time.localtime(row[2])
            
            sendtime=time.strftime("%Y-%m-%d %H:%M:%S",ltime)
            msg=self.fix(msgdata,0)
            senderuin=self.fix(uin, 1)
            
            amsg=[]
            amsg.append(sendtime)
            amsg.append(senderuin)
            amsg.append(msg)
            allmsg.append(amsg)
        return allmsg    
    def output(self,num,mode):
        file=str(num)+".html"
        f2 = open(file,"w",encoding="utf-8")
        f2.write("<head><meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" /></head>")
        allmsg=self.message(num,mode)
        f2.write("<div style='white-space: pre-line'>")
        for msg in allmsg:
            try:
                if(msg[1][0]=="5"):
                    f2.write("<p align='right'>")
                    f2.write("<font color=\"green\">")
                    f2.write(msg[0])                    
                    f2.write("</font>-----<font color=\"blue\"><b>")
                    f2.write("1")
                    f2.write("</font></b></br>")
                else:
                    f2.write("<p align='left'>")
                    f2.write("<font color=\"blue\"><b>")
                    f2.write("2")
                    f2.write("</b></font>-----<font color=\"green\">")
                    f2.write(msg[0])
                    f2.write("</font></br>")
                f2.write(self.AddEmoji(msg[2]))
                f2.write("</br></br>")
                f2.write("</p>")               
            except:
                pass
        f2.write("</div")

try:
    mode = 1
    
    '''
    yourfriendqq = 584740257
    db = "C:/Users/30857/Desktop/qq/308571034.db"
    key = "361910168361910168"
    s = "还是在试表情"
    '''
    q=QQoutput(db,key,mode,s)
    msg=q.message(yourfriendqq,mode)
    q.output(yourfriendqq,mode)
    #for line in msg[0:5]:
    #    print(line)
except Exception as e:
    print("###########################")
    print("Exception:", e)
    print("###########################")

input("Press enter to close the window")