from flask import Flask, render_template, url_for, request, redirect,Response
import mysql.connector
import pytz
from datetime import date, datetime
import time 
import json
import re

app = Flask(__name__) 


# delay connector until MySQL database is completely initialized and ready

def delay():
    try:
        cnx = mysql.connector.MySQLConnection(
            user='root',password='root',database='to_do_list',host='mydb',port=3310)
        cnx.close()
    except mysql.connector.Error:
        time.sleep(5)
        delay()


# Fetching Today's Information from database 

def todaysDate():
    # Specified a timezone of US Eastern Time
    n = datetime.now(tz=pytz.timezone('US/Eastern'))
    todayIs ='{}/{}/{}'.format(n.month,n.day,n.year)
    return todayIs

def getTodaysInfo():
    today = todaysDate()
    cnx = mysql.connector.MySQLConnection(
        user='root',password='root',database='to_do_list',host='mydb',port=3310)
    c = cnx.cursor()
    c.execute("SELECT information FROM todolist WHERE date = %s;",(today,))
    todaysInfo = c.fetchall()
    c.close()
    cnx.close()
    return todaysInfo

# Fetch all dates in date

def getDates():
    today = todaysDate()
    cnx = mysql.connector.MySQLConnection(
        user='root',password='root',database='to_do_list',host='mydb',port=3310)
    c = cnx.cursor()
    c.execute('SELECT date FROM todolist where date!=%s;',(today,))
    dates = c.fetchall()
    c.close()
    cnx.close()
    return dates
    
# Fetching a specified info of a date in the dropdown that isn't today

def getSpecifiedDateInfo(d):
    cnx = mysql.connector.MySQLConnection(
        user='root',password='root',database='to_do_list',host='mydb',port=3310)
    c = cnx.cursor()
    c.execute("SELECT information FROM todolist where date=%s;",(d,))
    dateSpecificLandingInfo = c.fetchall()
    c.close()
    cnx.close()
    return dateSpecificLandingInfo

# Inserting information into the information json array column for today

def insertInfo(info):
    today = todaysDate()
    cnx = mysql.connector.MySQLConnection(
        user='root',password='root',database='to_do_list',host='mydb',port=3310)
    c = cnx.cursor()
    c.execute("SELECT date FROM todolist where date=%s;",(today,))
    observe = c.fetchall()
    if observe:
        c.execute(
            "UPDATE todolist SET information = JSON_ARRAY_APPEND(information,'$', %s) WHERE date = %s;",
            (info.strip(),today))
    else:
        c.execute("INSERT INTO todolist VALUES (%s,JSON_ARRAY(%s));",(today,info.strip()))
    cnx.commit()
    c.close()
    cnx.close()

# Removing information from the information json array column for today
    
def removeInfo(info):
    today = todaysDate()
    cnx = mysql.connector.MySQLConnection(
        user='root',password='root',database='to_do_list',host='mydb',port=3310)
    c = cnx.cursor()
    c.execute(
        "UPDATE todolist SET information = JSON_REMOVE(information,replace(JSON_SEARCH(information,'one',%s),%s,'')) where date = %s;",
        (info.strip(),'"',today))
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

def shared_dates():
    current = todaysDate()
    today = 'Today, '+ convertDate(current)
    year = current.split('/')[-1]
    return today,year

# Running Route with Methods    
## Home 
@app.route("/",methods=['GET','POST','DELETE'])
def home():
    format_date = lambda t: (t[2],t[0],t[1])
    today,year =shared_dates()
    if request.method =='GET':
        homeLanding=getTodaysInfo()
        if homeLanding:
            homeLanding = json.loads(getTodaysInfo()[0][0])
        result = [i[0] for i in getDates()]
        
        result = sorted(result,reverse = True,key = lambda x: datetime(*format_date(tuple(
            map(int,x.split('/'))))))
        result = [convertDate(i) for i in result]
        return render_template('home.html',result=result,homeLanding=homeLanding,
        today=today,year = year)
    elif request.method =='POST':
        info = request.data
        if info:
            insertInfo(info)
            return info
        return Response(status=204)
    elif request.method=='DELETE':
        removing = request.data.decode('utf-8')   
        removeInfo(removing.replace('\\','\\\\').replace('\\"','\\\"'))      
        return removing

## History
@app.route("/<string:_date>",methods=['GET'])
def history(_date):
    theDate = _date.replace('-','/')
    format_date = lambda t: (t[2],t[0],t[1])
    today,year =shared_dates()
    regex = re.match(r'\d{1,2}-\d{1,2}-\d{4}',_date)
    if regex!=None and len(regex.group(0))== len(_date):
        try:
            old = json.loads(getSpecifiedDateInfo(theDate)[0][0])
        except IndexError:           
            return redirect('/')
        result = [i[0] for i in getDates()]
        result = sorted(result,reverse = True,key = lambda x: datetime(*format_date(tuple(
        map(int,x.split('/'))))))
        result = [convertDate(i) for i in result]          
        return render_template('archives.html',theDate=convertDate(theDate),
        result=result,old=old,today=today,year =year)
    ## 404
    return Response(status=404)
if __name__=='__main__':
    delay()
    app.run(host='0.0.0.0',port=2001,debug=True)