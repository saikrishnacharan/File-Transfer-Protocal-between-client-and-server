#!/usr/bin/env python
# coding: utf-8

import socket                   
import os
import sys
import json
import datetime
import shutil



global csocket0

port0 = 51020
dataport0 = 51021
cache_path = "./cache"
shared_path = "./"
csocket0 = socket.socket()
csocket0.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host = socket.gethostname() 
csocket0.connect((host, port0))    
csocket0_d = socket.socket()
csocket0_d.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
csocket0_d.connect((host,dataport0))

while True: 
    command = input("$$$---*Enter command*---$$$ : ")
    print("User entered ", command)
    main_arg = command.split(' ')[0]
    args = command.split(' ')
    if main_arg == "IndexGet":
        if len(args) > 1:
            csocket0.send(command.encode()) 
            print("Command successfully transferred :)")
            data = csocket0.recv(4096)
            if command.split(' ')[1] == "displayfiles":
                list_names=data.decode()
                list_names = " "+list_names[1:len(list_names)]
                shared_list = list_names[0:len(list_names)-1].split(',')
                for i in range(len(shared_list)):
                    print("File ",i+1,"--->", shared_list[i])
            if command.split(' ')[1] == "history":
                list_commands=data.decode()
                print(list_commands)
            if command.split(' ')[1] == "shortlist":
                list_info = data.decode()
                
                list_info = ","+" "+list_info[1:len(list_info)-1]
                files_info = list_info.split('\'#\'')
                x=files_info[0].split(", ")
                # print(x)
                for i in files_info:
                    count = 0
                    k=i.split(",")
                    # print(k[0])
                    # print(k[1])
                    for j in k:
                        if count == 1 :
                            print("File name: ", j)
                        elif count == 2 :
                            # print(count,j)
                            print("Time Stamp:",datetime.datetime.fromtimestamp(float(j)))
                        elif count == 3 :
                            print("Size:",j)
                        elif count == 4:
                            print("Type:", j)
                        count += 1
                    print("----------------------------")
            if command.split(' ')[1] == "longlist":
                list_info = data.decode()
                # print(list_info)
                list_info = ","+" "+list_info[1:len(list_info)-1]
                files_info = list_info.split('\'#\'')
                x=files_info[0].split(", ")
                # print(x)
                for i in files_info:
                    count = 0
                    k=i.split(",")
                    # print(k[0])
                    # print(k[1])
                    for j in k:
                        if count == 1 :
                            print("File name: ", j)
                        elif count == 2 :
                            # print(count,j)
                            print("Time Stamp:",datetime.datetime.fromtimestamp(float(j)))
                        elif count == 3 :
                            print("Size:",j)
                        elif count == 4:
                            print("Type:", j)
                        count += 1
                    print("----------------------------")
        else:
            print("Error: Give arguments\n")

    elif main_arg == "FileHash":
        if len(args) > 1:

            csocket0.send(command.encode()) 
            desc = csocket0.recv(4096)
            print(desc.decode())

    elif main_arg == "FileDownload":
        if len(args) == 3:
            csocket0.send(command.encode())
            print("\n----------------FILE INFO------------------") 
            desc = csocket0_d.recv(1024)
            print(desc.decode())

        else:
            print("Enter correct command format: FileDownload mode \"filename\" \n")
            continue

        protocol = command.split(' ')[1]
        filename = command.split(' ')[2]
        
        if protocol == "UDP":
            print("Protcol for transfer: UDP")
            udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            listen_addr = ("",32557)

            try:
                udp.bind(listen_addr)
            except:
                print("Failed to bind UDP socket")

            with open(filename,'wb') as f:
                size = csocket0.recv(1024).decode()
                size = int(size)
                print(size)
                while True:
                    # udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    # listen_addr = ("",21347)

                    if size <= 0:
                        break
                    try:
                        udp.settimeout(20)
                        data,addr = udp.recvfrom(1024)
                        f.write(data)
                    except socket.timeout:
                        print("Timed out")
                        f.close()
                        udp.close()

                    size -= 1024
                    
            f.close()
            udp.close()

        elif protocol == "TCP":
            with open(filename,'wb') as f:
                print("Mode:- TCP")  
                pass_bytes = csocket0.recv(1024).decode()
                end_bytes = pass_bytes.rfind('#')
                total_bytes = pass_bytes[0:end_bytes]
                total_bytes = int(total_bytes)
                print("Start:",total_bytes)
                while True:
                    if total_bytes <= 0:
                        print("End",total_bytes)
                        break
                    data = csocket0.recv(1024) 
                    total_bytes -= 1024
                    f.write(data)
            print("[Download Successful!] ", filename)
            f.close() 

    elif main_arg == "Cache":
        if not (os.path.isdir(cache_path)):
            print("Cache missing! :(")
            os.mkdir(cache_path)
            print("Hence created one :)")  
        if command.split(' ')[1] == "verify":
            filename = command.split(' ')[2]
            source_path = cache_path + "/" + filename
            target_path = shared_path + filename
            
            if os.path.isfile(cache_path + "/" + filename):
                print("File exists in Cache :)")
                try:
                    shutil.copyfile(source_path,target_path)
                    print("Copied to shared path successfully!")
                except shutil.SameFileError:
                    print("File already exists in shared path")
                except:
                    print("Error occurred while copying file from cache to share")


            else: 
                print("Doesnt exist in cache :( \nDownloading....")
                csocket0.send(command.encode())
                print("\n----------------FILE INFO------------------") 
                desc = csocket0_d.recv(1024)
                print(desc.decode())
                # with open(filename,'wb') as f:
                #     print("Mode:- TCP")  
                #     pass_bytes = csocket0.recv(1024).decode()
                #     end_bytes = pass_bytes.rfind('#')
                #     total_bytes = pass_bytes[0:end_bytes]
                #     total_bytes = int(total_bytes)
                #     while True:
                #         if total_bytes <= 0:
                #             break
                #         data = csocket0.recv(1024)
                #         total_bytes -= 1024 
                #         f.write(data)
                # print("[Download Successful!] ", filename)
                # f.close() 
                with open(filename,'wb') as f:
                    print("Mode:- TCP")  
                    pass_bytes = csocket0.recv(1024).decode()
                    end_bytes = pass_bytes.rfind('#')
                    total_bytes = pass_bytes[0:end_bytes]
                    total_bytes = int(total_bytes)
                    print("Start:",total_bytes)
                    while True:
                        if total_bytes <= 0:
                            print("End",total_bytes)
                            break
                        data = csocket0.recv(1024)
                        # total_bytes -= sys.getsizeof(data) 
                        total_bytes -= 1024
                        f.write(data)
                        # print(data)
                print("[Download Successful!] ", filename)
                f.close() 

                cache_size = 0
                for path, dirs, files in os.walk(cache_path):
                    for f in files:
                        fp = os.path.join(path, f)
                        cache_size += os.path.getsize(fp)
                print("size:", cache_size/(1000*1000)," MB")
                if (cache_size/(1000*1000))+os.path.getsize(target_path)/(1000*1000) < 7 :
                    try:
                        shutil.copyfile(target_path,source_path)
                        print("Copied downloaded file to cache path as well!")
                    except shutil.SameFileError:
                        print("File already exists in shared path")
                    except:
                        print("Error occurred while copying file from cache to share")
                else:
                    
                    while (cache_size/(1000*1000))+os.path.getsize(target_path)/(1000*1000) >= 7:
                        path = cache_path + "/"
                        oldest_file=min(os.listdir(path), key=lambda p: os.path.getmtime(os.path.join(path, p)))
                        delete_path = path + oldest_file
                        os.remove(delete_path)
                        print("Oldest file:",oldest_file," deleted")
                        cache_size = 0
                        for path, dirs, files in os.walk(cache_path):
                            for f in files:
                                fp = os.path.join(path, f)
                                cache_size += os.path.getsize(fp)
                        print("size:", cache_size/(1000*1000)," MB")
                    try:
                        shutil.copyfile(target_path,source_path)
                        print("Copied downloaded file to cache path as well!")
                    except shutil.SameFileError:
                        print("File already exists in shared path")
                    except:
                        print("Error occurred while copying file from cache to share")
        elif command.split(' ')[1] == "show":
            count = 0
            print("----------------Cache Info---------------")
            for f in os.listdir(cache_path):
                cfile_size = os.path.getsize(os.path.join(cache_path,f))/(1000000)
                print("File->",f," Size(in MB)->",cfile_size)


csocket0.close()
csocket0_d.close()

