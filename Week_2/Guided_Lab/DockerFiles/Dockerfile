FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y openssh-server sudo cron

RUN useradd -m -s /bin/bash ctf && \
    useradd --no-create-home -s /bin/bash ctf-cracked && \
    echo 'ctf:ctf' | chpasswd
    
RUN echo 'root:123456' | chpasswd

WORKDIR /home/ctf

RUN chown -R root:root . && \
    chmod o+rx .
COPY challenge/flag.txt .
COPY challenge/user.txt .
COPY challenge/my_ls .
COPY challenge/perms /etc/sudoers

RUN chown root:ctf-cracked flag.txt && chmod 440 flag.txt
RUN chown root:ctf-cracked flag.txt && chmod 555 my_ls

RUN chown ctf:ctf /etc/shadow && chmod 777 /etc/shadow

RUN echo "*/15 * * * * root	rm -rf /tmp/*" >> /etc/crontab 
RUN chmod -r /tmp /var/tmp /run/lock
RUN chmod go-rx /usr/bin/passwd

EXPOSE 22

ENTRYPOINT service cron start \
	    && service ssh start \
	    && tail -f /dev/null

