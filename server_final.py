#!/usr/bin/env python
# coding: utf-8
import socket
import os
import sys
import json
import hashlib
import datetime
import datetime

def md5(fname,shared_folder_path):
    hash_md5 = hashlib.md5()
    os.chdir(shared_folder_path)
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
global history
history = ""

port0 = 51020
dataport0 = 51021

global conn0
global conn1
ssocket0 = socket.socket() 
ssocket0.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
ssocket0_d = socket.socket()
ssocket0_d.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

host = socket.gethostname() 
ssocket0.bind((host, port0)) 
ssocket0_d.bind((host, dataport0))
ssocket0_d.listen(5)
ssocket0.listen(5) 
print("[Listening to the ports]")

conn1, addr1 = ssocket0_d.accept()
conn0, addr0 = ssocket0.accept()
# print("Successfully established connection with the client")
print("[Established connection with the client for file and info transfer]")

shared_folder_path = '../Shared_Directory'
os.chdir(shared_folder_path)
print("Server-side shared path:", shared_folder_path)
while True: 
    command = conn0.recv(4096).decode()
    print("---------------------------------------------------------------------------")
    print("Client request: ",command,"\n")
    main_arg = command.split(' ')[0]
    history += command + "\n" 
    
    if main_arg == "IndexGet":
        print("Command: IndexGet")
        # args = command.split(" ")
        if command.split(' ')[1] == "shortlist":
            print("[Display file info for files which which are modified in the time interval]")
            argument = command.split(' ')
            date_low = argument[2].split('/')
            date_high = argument[4].split('/')
            time_low = argument[3].split(':')
            time_high = argument[5].split(':')
            
            year_low = int(date_low[2])
            year_high = int(date_high[2])
            month_low = int(date_low[1])
            month_high = int(date_high[1])
            day_low = int(date_low[0])
            day_high = int(date_high[0])

            sec_low = int(time_low[2])
            sec_high = int(time_high[2])
            minute_low = int(time_low[1])
            minute_high = int(time_high[1])
            hour_low = int(time_low[0])
            hour_high = int(time_high[0])
            timestamp_low = datetime.datetime(year_low,month_low,day_low,hour_low,minute_low,sec_low)
            timestamp_high = datetime.datetime(year_high,month_high,day_high,hour_high,minute_high,sec_high)
            files_names = os.listdir()
            
            file_types = []
            file_sizes = []
            file_timestamps = []
            file_info = []
            # file_info.append("#")
            for file in files_names:
                if not file:
                    break
                file_timestamp = datetime.datetime.fromtimestamp(os.path.getmtime(file))
                if (file_timestamp >= timestamp_low) and (file_timestamp <= timestamp_high):
                    file_timestamp = datetime.datetime.timestamp(file_timestamp)
                    # print("111111")
                    if len(argument)==7:
                        file_name, file_extension = os.path.splitext(file)
                        if argument[6] == "*.txt":
                            if file_extension == ".txt":
                                # print("22222")
                                file_size = os.stat(file).st_size
                                file_info.append(file)
                                file_info.append(file_timestamp)
                                file_info.append(file_size)
                                file_info.append(file_extension)
                                file_info.append("#")
                                print("FileName:",file ," TS:",file_timestamp ,"type:",file_extension ," size:",file_size)
                        elif argument[6] == "*.pdf":
                            if file_extension == ".pdf":
                                # print("333333")
                                file_size = os.stat(file).st_size
                                file_info.append(file)
                                file_info.append(file_timestamp)
                                file_info.append(file_size)
                                file_info.append(file_extension)
                                file_info.append("#")
                                print("FileName:",file ," TS:",file_timestamp ,"type:",file_extension ," size:",file_size)                                
                    else:
                        file_info.append(file)
                        file_info.append(file_timestamp)
                        # print("444444")
                        # print("File in window:",file)
                        file_name, file_extension = os.path.splitext(file)
                        file_size = os.stat(file).st_size
                        file_info.append(file_size)
                        file_info.append(file_extension)
                        file_info.append("#")
                        print("FileName:",file ," TS:",file_timestamp ,"type:",file_extension ," size:",file_size)
            conn0.send(str(file_info).encode())

        elif command.split(' ')[1] == "displayfiles":
            print("[Display filenames in shared path]")
            files_names = os.listdir()
            conn0.send(str(files_names).encode())
       
        elif command.split(' ')[1] == "history":
            print("[View history of commands used]")
            print(history)
            conn0.send(history.encode())
        
        elif command.split(' ')[1] == "longlist":
            print("Status: Client requested the list of all files")
            files_names = os.listdir()
            
            file_types = []
            file_sizes = []
            file_timestamps = []
            file_info = []
            file_info.append("#")
            for file in files_names:
                if not file:
                    break
                file_timestamp = datetime.datetime.fromtimestamp(os.path.getmtime(file))
                # if (file_timestamp >= timestamp_low) and (file_timestamp <= timestamp_high):
                file_timestamp = datetime.datetime.timestamp(file_timestamp)
                file_info.append(file)
                file_info.append(file_timestamp)
                # print("File in window:",file)
                file_name, file_extension = os.path.splitext(file)
                file_size = os.stat(file).st_size
                file_info.append(file_size)
                file_info.append(file_extension)
                file_info.append("#")
                print("FileName:",file ," TS:",file_timestamp ,"type:",file_extension ," size:",file_size)
            conn0.send(str(file_info).encode()) 

    elif main_arg == "FileHash":
        # flag = command.split(' ')[1]
        data = ""
        print("entered filehash")
        if command.split(' ')[1] == "verify":
            print("[Verify filehash]\n")
            file = command.split(' ')[2]
            if not file:
                error = "File path\n"
                conn0.send(error.encode())
            else:
                checksum = md5(file,'../Shared_Directory')
                file_timestamp = datetime.datetime.fromtimestamp(os.path.getmtime(file))
                # file_timestamp = datetime.datetime.timestamp(file_timestamp)
                data += "Filename:"+ file + "\n" + "Checksum:" + checksum + "\n" + "Timestamp:" + str(file_timestamp) + "\n" + '\n'
                conn0.send(data.encode())
        
        elif command.split(' ')[1] == "checkall":
            print("[checkall FileHash]\n")
            files_names = os.listdir()
            for file in files_names:
                if not file:
                    break
                checksum = md5(file,'../Shared_Directory')
                file_timestamp = datetime.datetime.fromtimestamp(os.path.getmtime(file))
                data += "Filename:"+ file + "\n" + "Checksum:" + checksum + "\n" + "Timestamp:" + str(file_timestamp) + "\n" +"----------------------------------------------" + "\n"
            conn0.send(data.encode())

    elif main_arg == "FileDownload":
        filename = command.split(' ')[2]
        print("[SENDING FILE TO CLIENT :]",filename)
        file_info = ""
        checksum = md5(filename,'../Shared_Directory')
        file_timestamp = datetime.datetime.fromtimestamp(os.path.getmtime(filename))
        file_size = os.stat(filename).st_size
        file_info += "Filename:"+ filename + "\n" + "Checksum:" + checksum + "\n" + "Timestamp:" + str(file_timestamp) + "\n" + "Size :" + str(file_size/(1000*1000))+" MB"+ "\n" +"----------------------------------------------"+"\n"
        conn1.send(file_info.encode())
        print("Sent file information")

        if command.split(' ')[1] == "TCP":
            f = open(filename, 'rb')
            size = str(os.path.getsize(filename))
            size_pkt = size + "#" + (1023 - len(size))*"%"
            conn0.send(size_pkt.encode())
            print("Start:", size)
            data = f.read(1024)
            while data:
                # print(data)
                conn0.send(data)
                data = f.read(1024)
            f.close()
            print("[+]FILE SENT")

        
        elif command.split(' ')[1] == "UDP":
            f = open(filename, 'rb')
            initiate = "true"
            print("Initiating UDP")
            addr = (conn0.getpeername()[0], 32557)                 
            udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            if initiate == "true":
                size = str(os.path.getsize(filename))
                conn0.send(size.encode())
                data = f.read(1024)
                print(size)
                while data:
                    udp.sendto(data,addr)
                    data = f.read(1024)
                f.close()
            udp.close()

    elif main_arg == "Cache":
        if command.split(' ')[1] == "verify": 
            filename = command.split(' ')[2]
            print("[SENDING FILE TO CLIENT]",filename)
            file_info = ""
            protocol = command.split(' ')[1]
            if not os.path.isfile(filename):
                error = "Enter correct file\n"
                conn1.send(error.encode())
                continue
            else:
                checksum = md5(filename,'../Shared_Directory')
                file_timestamp = datetime.datetime.fromtimestamp(os.path.getmtime(filename))
                file_size = os.stat(filename).st_size
                file_info += "Filename:"+ filename + "\n" + "Checksum:" + checksum + "\n" + "Timestamp:" + str(file_timestamp) + "\n" + "Size :" + str(file_size/(1000*1000))+" MB"+ "\n" +"----------------------------------------------"+"\n"
                conn1.send(file_info.encode())
                print("sent info")
            #--------------------------------
            f = open(filename, 'rb')
            size = str(os.path.getsize(filename))
            size_pkt = size + "#" + (1023 - len(size))*"%"
            conn0.send(size_pkt.encode())
            data = f.read(1024)
            while data:
                conn0.send(data)
                data = f.read(1024)
            f.close()
            print("file closed")

    else:
        error = "Command doesnt exist\n"
        conn0.send(error.encode())



