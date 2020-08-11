# File-Transfer-Protocal-between-client-and-server

***Serverside code - server_final.py***

***Clientside code - client_final.py***

Command Documentation:

1)  IndexGet displayfiles
		
		-Displays the names of the files present in the shared folder of the server.

2)  IndexGet history

		-Displays the commands entered till now

3)  
    a. IndexGet shortlist start_day/start_month/start_year start_hour:start_mins:start_sec end_day/end_month/end_year end_hours:end_mins:end_sec	
			
		-Displays details(size,timestamp...) for all the modified/created files in between start_timestamp and end_timestamp

    [Bonus]        
    b. IndexGet shortlist start_day/start_month/start_year start_hour:start_mins:start_sec end_day/end_month/end_year end_hours:end_mins:end_sec *.txt	
			
		-Displays details(size,timestamp...) for only the modified/created txt files in between start_timestamp and end_timestamp

    c. IndexGet shortlist start_day/start_month/start_year start_hour:start_mins:start_sec end_day/end_month/end_year end_hours:end_mins:end_sec *.pdf	
			
		-Displays details(size,timestamp...) for only the modified/created "pdf" files in between start_timestamp and end_timestamp. 

4) IndexGet longlist

		-Displays details(size,timestamp...) for all the files in the shared folder.

5) FileHash checkall

		-Displays the filename, md5hash checksum and timestamp of all the files on servers shared folder.

6) FileHash verify <filename(no quotes)> 

		-Displays the filename, md5hash checksum and timestamp of the file "filename" on servers shared folder.

7) FileDownload UDP <filename>

		-Downloads the file "filename" from the server shared folder using "UDP" protocol 

8) FileDownload TCP <filename>

		-Downloads the file "filename" from the server shared folder using "TCP" protocol

9) Cache show

		-Displays the files present in the clients cache

10) Cache verify <filename>

		-Checks if "filename" is present in the cache, and if it exists, copies it to the client folder. If it doesnt exist, then it does "FileDownlad" for the file from the server.

-----------------------------------
**Example:  (Executed the following commands and attached the screenshots of the results in folder "results")**

IndexGet displayfiles

IndexGet longlist

IndexGet shortlist 22/04/2020 1:00:00 28/04/2020 23:00:00

IndexGet shortlist 22/04/2020 1:00:00 28/04/2020 23:00:00 *.txt

IndexGet shortlist 22/04/2020 1:00:00 28/04/2020 23:00:00 *.pdf

IndexGet history

FileHash checkall

FileHash verify a1.pdf

FileDownload UDP balayya.pdf

FileDownload TCP jai.pdf

Cache show

Cache verify jai.pdf

Cache verify dull2.pdf

FileDownload TCP Divide_Final.pptx

FileDownload TCP 1.png

Cache verify 1.png

FileDownload UDP zinda.txt

Cache verify balayya.pdf

Cache show

Cache verify balayya.pdf

Cache verify 1.png

FileDownload UDP 7.png

  


