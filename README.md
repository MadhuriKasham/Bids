WSL 
--> Windows Subsystem for Linux is virtual machine that runs on windows
--> https://allthings.how/how-to-use-linux-terminal-in-windows-10/

Install - sudo apt install 
Unix Commands: 

Who - User Info
pwd - Print working directory/Current directory
ls – listing directories
ls – l – to see the list 
cd.. – navigate back to previous directory
ls – la - list all the files in a directory and permissions
clear  - clears all the shell commands
ls /mnt - all the mounted directories
mv - file moving/Renaming file of txt files
-	mv file1.text file2.text(Copy data of one file to another)
-	mv text.txt test.txt(replacing)
-	mv filename dir (moving file to directory)
-	mv -i filename dir (overriding file)
-	mv dir1 dir2 (moving directory from 1 to 2)
-	man mv (help)

cd /mnt/c – files with in C- directory
touch – create a new empty file add content/modify timestamp
 --> touch hello world
nano – modifications in file
sudo apt-get update 
sudo apt-get upgrade 
nano ~/.bashrc-alias winhome = ‘’(retruns to this directory when winhome command used in bash)
source ~/.bashrc 
cat – display/ merge two files and copy into file3/ create file a enter the data into file
-	cat -->file1.txt
-	control D to exit 
-	cat file1 file2>file
-	cat – display the contents of file
ls *.txt – lists all files with the given extension
-	ls *.c, ls *.py
cp – copy a file or directory
-->	cp file1.txt file2.txt
vi file1.txt
-->	press I to insert
head – gives fiest ten lines of code
-->	head file1.txt
tail – gives last 10 lines of the code
-->	tail tail.txt
tac – reverse order the code
-->	tac file.txt
more – displays all the files
-->	more file1.txt
id – diplays id  or group
-->	id
vi – text editor
diff – differentiate two files
history – fetch all the previous commands 

grep -ni "Hi" text.txt – Used to find text within the file/ search patterns in the given content
-	rm – remove files/ delete files
-	rm filename
-	cat >filename.txt (creates file)
-	rm file1.txt file2.txt
-	mkdir dir1 (create directory)
-	rm –r dir1 (deletes directory)
-	rm –i file.txt



Shell scripting: 
Create folder - mkdir PrimeNumbers (foldername)
cd PrimeNumbers
 code . – opens default editor with the system
To execute -  ./Helloworld.sh
touch Helloworld.sh     touch command requires permission to execute the script.
Give permissions to file: chmod +X hello.sh
# To use comments in the script

--> Variables – System Varibles, User defined Variables
--> System – These are case sensitive (Uppercase)
User Defined – Lowercases
echo $BASH
echo $BASH_VERSION
echo $PWD
echo $HOME

curl:
sudo apt-get install curl
curl –version
hit url - curl https://www.howtogeek.com/447033/how-to-use-curl-to-download-files-from-the-linux-command-line/
output - curl -o bbc.html https://www.howtogeek.com/447033/how-to-use-curl-to-download-files-from-the-linux-command-line/
speed info - curl –x -o bbc.html https://www.howtogeek.com/447033/how-to-use-curl-to-download-files-from-the-linux-command-line/
hit multiple  urls -xargs -n 1 curl -o < urls-to-download.txt
request headers - curl -I https://www.howtogeek.com/447033/how-to-use-curl-to-download-files-from-the-linux-command-line/
json data - curl https://api.ipify.org?format=json

wget:
download - wget https://pdfs.semanticscholar.org/4297/626dad995612a5bec4cbd9c41d2a2f6f0146.pdf
continue incomplete download - wget https://pdfs.semanticscholar.org/4297/626dad995612a5bec4cbd9c41d2a2f6f0146.pdf
download data from ftp server: wget -r ftp://pdfs.semanticscholar.org/4297/626dad995612a5bec4cbd9c41d2a2f6f0146.pdf
--noparent if you want to avoid downloading folders and files above the current level.
Download all - wget -i download.txt

Scp – command line that help to share files between two computer remotely
-	scp C:\Users\madhury\Desktop\PrimeNumbers\pdfs.semanticscholar.org\4297 [ip]
-	scp – r C:\Users\madhury\Desktop\PrimeNumbers\pdfs.semanticscholar.org\4297 [ip]
-	Ubuntu ip address
-	ssh username@[ip]
client server model:
Sever-> central location_>multiple clients(devices, computers)
Fortnight(central server)
-> connected to central server(faster than each client)
-> connected to other client server(slower)
->info transferred from c1 to server, info passed to other clients
IN local network
Modem: connected to internet has one public ip address (physical address) 
->devices connected to router(devices are connected) wirelessly, has a local ip address 
-> client, each device is shared with a Ip address(IPV4), local client ip address is visible to the clients connected to the same router

--> Pick the port
--> Pick the server
--> Bind the socket to the ip address (which ip to accept, standard way to send data)
--> AF_INET- family of ipv4
--> Sock_stream – establishment of connection to TCP default connection

Configuring Nginx:
Resource --> https://www.maketecheasier.com/install-nginx-server-windows/
