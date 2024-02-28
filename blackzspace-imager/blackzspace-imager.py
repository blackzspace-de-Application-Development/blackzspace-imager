import os
import sys
import subprocess
import logging
import PyQt6

import json

from os.path import *
from pathlib import Path

from subprocess import Popen, PIPE, STDOUT


from mainui import *
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QFile
from PyQt6.QtGui import QFileOpenEvent
from PyQt6.QtWidgets import (
    QApplication, 
    QWidget, 
    QFileDialog, 
    QGridLayout,
    QPushButton, 
    QLabel,
    QListWidget
)



base_dir = os.getcwd()
devices_tree_list_dir = "tmp/"
config = "config/config.json"
dev = "/dev/"
device = "device"
x = 0

f = open(config)
data = json.load(f)




class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        
        
        
        self.consoleLog.append("Console > blackzspace-image started!!!")
        self.consoleLog.append("Version: " + data["version"])
        
        
        self.set_Output_Button.clicked.connect(self.open_file_dialog)
        
        
        self.build_Button.clicked.connect(self.build)
        
        
        self.scan_Button.clicked.connect(self.get_devs)
        
        self.load_flash_Image_Button.clicked.connect(self.load_flashImage)
        
        self.flash_device_scan_Button.clicked.connect(self.get_flashdevs)
        
        self.flash_Button.clicked.connect(self.flash)
        
        
        
        
    def get_devs(self):
        proc = subprocess.run(["lsblk -o NAME -nl"], shell=True, stdout=subprocess.PIPE)
        with open(devices_tree_list_dir + "devices.tree", "w") as f:
            f.write(proc.stdout.decode("utf-8"))
            f.close()
            
        print(proc.stdout)
       
        with open(devices_tree_list_dir + "devices.tree", "r") as f:
            xs = f.readlines()
            f.close()
            
        for readline in xs:
            self.consoleLog.append("Detected : " + readline)
            self.comboBox_devices.addItem("/dev/" + readline)
            
        
        
    def get_flashdevs(self):
        proc = subprocess.run(["lsblk -o NAME -nl"], shell=True, stdout=subprocess.PIPE)
        with open(devices_tree_list_dir + "devices.tree", "w") as f:
            f.write(proc.stdout.decode("utf-8"))
            f.close()
            
        print(proc.stdout)
       
        with open(devices_tree_list_dir + "devices.tree", "r") as f:
            xs = f.readlines()
            f.close()
            
        for readline in xs:
            self.consoleLog.append("Detected : " + readline)
            self.combobox_FLash_device.addItem("/dev/" + readline)
            
    

    
        

    def open_file_dialog(self):
        filename, ok = QFileDialog.getSaveFileName(
            self,
            "Select a File", 
            "/root", 
            "Images (*.img *.tar.gz)"
        )
        if filename:
            path = Path(filename)
            self.output_Image.setText(str(path))
            file = open(filename, "w")
            file.write(str(path))
            file.close()
            
            
    def load_flashImage(self):
        filename, _ = QFileDialog.getOpenFileName(
        self,
        "Select a File",
        "/root", 
        "Images (*.img *.tar.gz)"
    )
        if filename:
            path = Path(filename)
            self.flash_Image_Path.setText(str(path))
            
        
    def flash(self):
        target = self.combobox_FLash_device.currentText()
        xoc = subprocess.run("sudo dd if='" + self.flash_Image_Path.text() + "' of=" + target.replace("\n", "") + "bs=32M, conv=fsync", shell=True, stdout=subprocess.PIPE)
        print(xoc.stdout)    
        
        
        
    def build(self, path):
        target = self.comboBox_devices.currentText()
        self.consoleLog.append("Console > Start Building Image-File: \n {filename}   \n     FROM: {target}")
        xoc = subprocess.run("sudo dd bs=4M if=" + target.replace("\n", "") + " of=" + self.output_Image.text() + " status=progress", shell=True, stdout=subprocess.PIPE)
        print(xoc.stdout)
        
        
        
        
        


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec()