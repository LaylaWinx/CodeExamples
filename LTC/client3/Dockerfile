FROM debian

RUN apt update
RUN apt-get install -y iperf
RUN apt-get install -y ssh
RUN apt install openssh-client
RUN apt install sshpass

COPY ssh_key_sasha ./ssh_key_sasha
COPY runnig_queries_clients ./runnig_queries_clients

CMD bash ./runnig_queries_clients
