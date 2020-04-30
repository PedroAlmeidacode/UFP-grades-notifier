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

- Fetches your grades from SIUFP (https://portal.ufp.pt) with web scrapping
- Stores them in a ``.csv`` file
- Compares the data fetched with the data stored
- Automates the process several times for detecting new grades 
- Notification with ``yagmail`` to the email specified in ``.env``

<br><br><br><b>
### MADE BY 
Pedro Almeida
in #OneScriptPerDay personal challenge 


