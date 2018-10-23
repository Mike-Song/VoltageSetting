# -*- coding: utf-8 -*-

"""
Module implementing VoltageSettingDialog.
"""
import sys
import struct
from socket import * 
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog

from Ui_VoltageSetting import Ui_Dialog

gDMax = 2**20-1
gDMin = 0
gVolMax = 7.1311
gVolMin = -7.127839

class UDPSocketClient:
    def __init__(self):
        self.mHost = '192.168.1.6'
        self.mPort = 6000 
        self.mBufsize = 8 + 12 # 16 + 12 
        self.mAddress = (self.mHost, self.mPort)
        self.mUDPClient = socket(AF_INET, SOCK_DGRAM)
        self.mData = None
        self.mUDPClient.settimeout(5)

    def sendData(self):
        self.mUDPClient.sendto(self.mData,self.mAddress)

    def receiveData(self):
       self.mData, self.mAddress = self.mUDPClient.recvfrom(self.mBufsize)
       return self.mData
  

class VoltageSettingDialog(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(VoltageSettingDialog, self).__init__(parent)
        self.setupUi(self)
        self.udpSocketClient = UDPSocketClient()
        self.dValue = 0.0
        self.volValue = 1.0
        self.pushButton_Plus1.setEnabled(False)
        self.pushButton_Plus10.setEnabled(False)
        self.pushButton_Plus100.setEnabled(False)
        self.pushButton_Sub1.setEnabled(False)
        self.pushButton_Sub10.setEnabled(False)
        self.pushButton_Sub100.setEnabled(False)

    
    def sendcommand(self, cmdid,status,msgid,len,type,offset,regAddr,regValue):
          cmdid=struct.pack('H',htons(cmdid))
          status=struct.pack('H',htons(status))
          msgid=struct.pack('H',htons(msgid))
          len=struct.pack('H',htons(len))
          type=struct.pack('H',htons(type))
          offset=struct.pack('H',htons(offset))
          regAddr=struct.pack('I',htonl(int(regAddr, 16)))
          regValue=struct.pack('I',htonl(int(regValue, 16)))
          
          data = cmdid + status + msgid + len + type + offset + regAddr + regValue
          
          self.udpSocketClient.mData = data
          self.udpSocketClient.sendData()

    def writeReg(self):  
        self.sendcommand(0x5a02,0x0000,0x5a02,0x0008,0x0000,0x0000,hex(int("0x0001", 16)),hex(self.dValue ))
    
    def calVol(self,  dValue):
         self.volValue = round(((gVolMax-gVolMin)*dValue/(2**20-1) + gVolMin), 6)
         self.lineEdit_Vol.setText(str(self.volValue))
    
    @pyqtSlot()
    def on_pushButton_Set_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        volValue = float(self.lineEdit_Vol.text())
        self.dValue  = round((volValue-gVolMin)*(2**20-1)/(gVolMax-gVolMin))
         
        if(self.dValue  >= gDMax):
           self.dValue  = gDMax
        elif(self.dValue  <= gDMin):
           self.dValue  = gDMin
           
        self.writeReg()
        
        self.pushButton_Plus1.setEnabled(True)
        self.pushButton_Plus10.setEnabled(True)
        self.pushButton_Plus100.setEnabled(True)
        self.pushButton_Sub1.setEnabled(True)
        self.pushButton_Sub10.setEnabled(True)
        self.pushButton_Sub100.setEnabled(True)
    
    @pyqtSlot()
    def on_pushButton_Plus1_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.dValue += 1
        if(self.dValue >= gDMax):
           self.dValue = gDMax
        elif(self.dValue <= gDMin):
           self.dValue = gDMin
         
        self.calVol(self.dValue)
        self.writeReg()
    
    @pyqtSlot()
    def on_pushButton_Sub1_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.dValue -= 1
        if(self.dValue >= gDMax):
           self.dValue = gDMax
        elif(self.dValue <= gDMin):
           self.dValue = gDMin
         
        self.calVol(self.dValue)
        self.writeReg()
    
    @pyqtSlot()
    def on_pushButton_Plus10_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.dValue += 10
        if(self.dValue >= gDMax):
           self.dValue = gDMax
        elif(self.dValue <= gDMin):
           self.dValue = gDMin
         
        self.calVol(self.dValue)
        self.writeReg()
    
    @pyqtSlot()
    def on_pushButton_Sub10_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.dValue -= 10
        if(self.dValue >= gDMax):
           self.dValue = gDMax
        elif(self.dValue <= gDMin):
           self.dValue = gDMin
         
        self.calVol(self.dValue)
        self.writeReg()
    
    @pyqtSlot()
    def on_pushButton_Plus100_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.dValue += 100
        if(self.dValue >= gDMax):
           self.dValue = gDMax
        elif(self.dValue <= gDMin):
           self.dValue = gDMin
         
        self.calVol(self.dValue)
        self.writeReg()
    
    @pyqtSlot()
    def on_pushButton_Sub100_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.dValue -= 100
        if(self.dValue >= gDMax):
           self.dValue = gDMax
        elif(self.dValue <= gDMin):
           self.dValue = gDMin
         
        self.calVol(self.dValue)
        self.writeReg()
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    #Dialog = QtWidgets.QDialog()
    ui = VoltageSettingDialog()
    ui.show()
    sys.exit(app.exec_())
