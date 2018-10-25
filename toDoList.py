from flask import Flask, render_template, url_for, request, redirect
import mysql.connector
import pytz
from datetime import date, datetime
import time 
import json


app = Flask(__name__) 

# delay connector until MySQL database is completely initialized and ready

def delay():
    try:
        cnx = mysql.connector.MySQLConnection(user='root',password='root',database='to_do_list',host='mydb',port=3310)
        cnx.close()
    except mysql.connector.Error as err:
        time.sleep(5)
        delay()
delay()

# Fetching Today's Information from database 

def todaysDate():
    # Specified a timezone of US Eastern Time
    n = datetime.now(tz=pytz.timezone('US/Eastern'))
    todayIs ='{}/{}/{}'.format(n.month,n.day,n.year)
    return todayIs

def getTodaysInfo():
    today = todaysDate()
    cnx = mysql.connector.MySQLConnection(user='root',password='root',database='to_do_list',host='mydb',port=3310)
    c = cnx.cursor()
    c.execute("SELECT information FROM todolist WHERE date = %s;",(today,))
    todaysInfo = c.fetchall()
    c.close()
    cnx.close()
    return todaysInfo

# Fetch all dates in date

def getDates():
    today = todaysDate()
    cnx = mysql.connector.MySQLConnection(user='root',password='root',database='to_do_list',host='mydb',port=3310)
    c = cnx.cursor()
    c.execute('SELECT date FROM todolist where date!=%s;',(today,))
    dates = c.fetchall()
    c.close()
    cnx.close()
    return dates
    
# Fetching a specified info of a date in the dropdown that isn't today

def getSpecifiedDateInfo(d):
    cnx = mysql.connector.MySQLConnection(user='root',password='root',database='to_do_list',host='mydb',port=3310)
    c = cnx.cursor()
    c.execute("SELECT information FROM todolist where date=%s;",(d,))
    dateSpecificLandingInfo = c.fetchall()
    c.close()
    cnx.close()
    return dateSpecificLandingInfo

# Inserting information into the information json array column for today

def insertInfo(info):
    today = todaysDate()
    cnx = mysql.connector.MySQLConnection(user='root',password='root',database='to_do_list',host='mydb',port=3310)
    c = cnx.cursor()
    c.execute("SELECT date FROM todolist where date=%s;",(today,))
    observe = c.fetchall()
    if observe:
        c.execute("UPDATE todolist SET information = JSON_ARRAY_APPEND(information,'$', %s) WHERE date = %s;",(info.strip(),today))
    else:
        c.execute("INSERT INTO todolist VALUES (%s,JSON_ARRAY(%s));",(today,info.strip()))
    cnx.commit()
    c.close()
    cnx.close()

# Removing information from the information json array column for today
    
def removeInfo(info):
    today = todaysDate()
    cnx = mysql.connector.MySQLConnection(user='root',password='root',database='to_do_list',host='mydb',port=3310)
    c = cnx.cursor()
    c.execute("UPDATE todolist SET information = JSON_REMOVE(information,replace(JSON_SEARCH(information,'one',%s),%s,'')) where date = %s;",(info.strip(),'"',today))
    cnx.commit()
    c.execute("SELECT information FROM todolist where date = %s",(today,))
    observe = c.fetchall()[0][0].replace('[','').replace(']','')
    if observe:
        c.close()
        cnx.close()
    else:
        c.execute("DELETE FROM todolist WHERE date = %s",(today,))
        cnx.commit()
        c.close()
        cnx.close()
    
    
# Convert for display 

def convertDate(x):
    y = list(map(int,x.split('/')))
    wday = date(y[2],y[0],y[1]).weekday()
    day = ''
    if wday ==0:
        day+='Mon'
    elif wday ==1:
        day+='Tue'
    elif wday ==2:
        day+='Wed'
    elif wday ==3:
        day+='Thu'
    elif wday ==4:
        day+='Fri'
    elif wday ==5:
        day+='Sat'
    elif wday ==6:
        day+='Sun'
    day+=' '+x
    return day
        
# Running Route with Methods    

@app.route('/home',methods=['GET','POST'])    
@app.route("/",methods=['GET','POST'])
def home():
    today = 'Today, '+ convertDate(todaysDate())
    if request.method =='GET':
        homeLanding=getTodaysInfo()
        if homeLanding:
            homeLanding = json.loads(getTodaysInfo()[0][0])
        result = [i[0] for i in getDates()]
        result = sorted(result,reverse = True,key = lambda x: list(map(int,x.split('/'))))
        result = [convertDate(i) for i in result]
        return render_template('home.html',result=result,homeLanding=homeLanding,today=today)
    elif request.method =='POST':
        theDate = request.form.get('days')
        removing = request.form.get('embedded')
        if theDate and len(theDate.split(' '))<=2:
            try:
                old = json.loads(getSpecifiedDateInfo(theDate.split(' ')[1])[0][0])
            except IndexError as err:
                return redirect('home')
            result = [i[0] for i in getDates()]
            result = sorted(result,reverse = True,key = lambda x: list(map(int,x.split('/'))))
            result = [convertDate(i) for i in result]
            return render_template('archives.html',theDate=theDate,result=result,old=old,today=today)
        elif removing:
            try:
                removeInfo(removing)
                return redirect('home')
            except IndexError as err:
                return redirect('home')
        info = request.form.get('items')
        if info:
            insertInfo(info.replace('\\"','').replace('\\',''))
        return redirect('home')
        
if __name__=='__main__':
    app.run(host='0.0.0.0',port=2001,debug=True)