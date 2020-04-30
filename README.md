# UFP_grades_notifier


Python web scrapper notifies UFP students by **mail** for new grades release 

<br>

### Pre-requirements
``python3``


### Installation

Use the package manager [pip3]
```shell
pip3 install yagmail
pip3 install beautifulsoup4 
pip3 install requests
pip3 install dotenv
```
<br><br><br>
## Using crontab for automation:
You can define for crontab to run the python script the times you want a day<br>
Recommended like 5 times a day, otherwise it will freeze the SIUFP servers
<br><br>
**Install crontab**
```bash
sudo apt-get update
sudo apt-get install cron
```

**Modify script.sh to your ${PATH}**<br>
with *nano or *vim<br>
```bash
#!/usr/bin/env bash
cd ${PATH}/UFP-grades-notifier
python3 Script.py
```

**Give permissions to your bash script**
```bash
chmod +x script.sh
```

**How crontab works**

```bash
.---------------- minute (0 - 59) 
|  .------------- hour (0 - 23)
|  |  .---------- day of month (1 - 31)
|  |  |  .------- month (1 - 12) OR jan,feb,mar,apr ... 
|  |  |  |  .---- day of week (0 - 6) (Sunday=0 or 7)  OR sun,mon,tue,wed,thu,fri,sat 
|  |  |  |  |
*  *  *  *  *  command to be executed
```

**Setting crontab (example)**
Enter in terminal:<br>
```bash
crontab -e
```
Enter in the file:<br>
```bash
30 8,12,15,18,20,22 * * *  sh ${PATH}/UFP-grades-notifier/script.sh
```
**This example will run the script at 8:30,12:30,15:30,18:30,20:30 and 22:30**

<br><br><br>

## Using yagmail:
Register on it
<br>
**Run in terminal:**
```bash

python3
>>> import yagmail
>>> yagmail.register('email1_equal_env.gmail.com', 'yourpass123')
```
The email inputed here is the email that will be regstered on yagmail,
is the mail the script will use to send mails (as server side) to the mail 
you want to receive the notifications. 
<br><br>
## Needed:
- Modificate your **.env** file for automation<br>
 (you decide where to receive)
 ```.env
EXAMPLE:

// SIUFP authentication
USER_LOGIN = 32732
USER_PSWD = ********

// email registered on YAGMAIL used to send the information
EMAIL_YAGMAIL = email_registered@gmail.pt
PSWD_YAGMAIL = *********

// this is the mail that will receive the notifications
EMAIL_RECEIVING_NOTIFICATIONS = email_receiving@gmail.com
```

<br>

## [PROBLEM]
#### The gmail registered in yagmail could be protected for less secure applications<br>
##### you can modify it in gmail settings
modified it here :  https://myaccount.google.com/lesssecureapps
<br><br>
![](https://github.com/PedroAlmeidacode/UFP-grades-notifier/blob/master/Captura%20de%20ecr%C3%A3%20de%202020-04-29%2022-03-45.png)
<br><br>


<br><br><br><b>
## How it works ?

- Fetches your grades from SIUFP  ( https://portal.ufp.pt )  with web scrapping
- Stores them in a ``.csv`` file
- Compares the data fetched with the data stored
- Automates the process several times for detecting new grades 
- Notification with ``yagmail`` to the email specified in ``.env``

<br><br><br><b>
### MADE BY 
Pedro Almeida
in #OneScriptPerDay personal challenge 


