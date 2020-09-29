# coding=utf-8
# python version should > 2.7.10
import os
import serial
import threading
import random
import time
import datetime
import logging
import traceback
from datetime import datetime

# 参数设置
ReportFileName = "ReportFile"
serialPort="COM3"   #串口
baudRate=9600       #波特率

# UART 口字符探测
Str_Running="FLASH TEST TESTING ..."
Str_Write="FLASH TEST WRITE"
Str_Start="FLASH TEST START"
Str_Error="FLASH TEST ERROR"

logging.basicConfig()

def CreatReportFile(ReportFile):
    if(os.path.exists(ReportFile)):
        os.remove(ReportFile)
        print ReportFile + " exit, delete."
    file = open(ReportFile, 'w')
    file.write("********** Test Report **********\n")
    file.close()

def WriteStrToFile(filename, data):
    with open(filename, 'a+') as f:
        time_info = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
        f.write(time_info + data + '\n')
        f.close()

class SerialPort(object):
    message='' 
    def __init__(self,port,buand):
        super(SerialPort, self).__init__()
        self.port=serial.Serial(port,buand,timeout=0.5)
        self.port.close()
        if not self.port.isOpen():
            self.port.open()

        if self.port.isOpen():
            print('Open %s success' % serialPort)
        else:
            print('Open %s failed' % serialPort)

    def port_open(self):
        if not self.port.isOpen():
            self.port.open()

    def port_close(self):
        self.port.close()
    def send_data(self):
            data = input("plase input:")
            n=self.port.write((data+'\n').encode())
            return n
    def read_data(self):
        while self.port.inWaiting() > 0:
            self.message=self.port.readline()
            #print self.message
            return self.message

    def setDTR(self,opt):
        self.port.setDTR(opt)

    def RandomPowerDown(self):
        global TestCont
        while True:
            event1.wait()
            sec = random.randint(1,15) # 随机时间范围
            print("Power Down after %d second" % sec)
            time.sleep(sec)
            print("POWER DOWN!")
            mSerial.setDTR(0) #下电
            # 记录断电次数到文件中
            TestCont += 1
            WriteStrToFile(ReportFile, "Power Down: %5ds | %d times" % (sec, TestCont))
            time.sleep(5)
            print("POWER ON!")
            mSerial.setDTR(1) #上电
            time.sleep(10)
            event1.clear()



TestCont=0
rx_data=None

now_time = datetime.now().strftime("_%Y-%m-%d_%H-%M-%S")
ReportFile = os.getcwd()+"\\" + ReportFileName + now_time + ".txt"
print("Creat the report file:")
print(ReportFile)

if __name__=='__main__':

    event1 = threading.Event()

    mSerial=SerialPort(serialPort,baudRate)
    print("POWER ON!")
    time.sleep(5)
    mSerial.setDTR(1) #上电
    time.sleep(10)

    t1=threading.Thread(target=mSerial.read_data)
    t2=threading.Thread(target=mSerial.RandomPowerDown)

    t1.start()
    t2.start()
    CreatReportFile(ReportFile)
    while True:
        rx_data = mSerial.read_data() 
        if rx_data:
            #print(rx_data)
            if rx_data.strip() == Str_Write.strip():
                event1.set()

            if rx_data.strip() == Str_Error.strip():
                print("Test Error!!!")
                WriteStrToFile(ReportFile, "\n ########## Test Error!!! ##########")
                time.sleep(10)
                os.system("pause")
                exit()
