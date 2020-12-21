FROM debian

RUN apt update
RUN apt-get install -y iperf
RUN apt install -y iperf openssh-server

RUN useradd -rm -d /home/user_folder -s /bin/bash -g root -G sudo -u 1000 user_name
RUN echo 'user_name:user_pswd' | chpasswd
RUN mkdir -p /home/user_folder/.ssh
COPY ssh_key_sasha.pub /home/user_folder/.ssh/ssh_key_sasha.pub
RUN chown -R user_name /home/user_folder/.ssh

COPY script ./script
RUN chmod +x script

CMD ./script && iperf -su -p 8080 & iperf -s -p 8080


