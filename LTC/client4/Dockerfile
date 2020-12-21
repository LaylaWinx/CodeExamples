FROM debian

RUN apt update
RUN apt-get install -y iperf
RUN apt-get install -y ssh
RUN apt install openssh-client
RUN apt install sshpass

COPY ssh_key_sasha ./ssh_key_sasha

CMD sshpass -p "user_pswd" ssh -oStrictHostKeyChecking=no -i ssh_key_sasha user_name@172.30.3.0 echo "ssh echo text" & ping 172.30.3.0 -c 10 & iperf -c 172.30.3.0 -p 8080 -t 10 & iperf -c 172.30.3.0 -u -p 8080 -t 10
