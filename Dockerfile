FROM ubuntu:20.04
ENV PATH="/root/miniconda3/bin:${PATH}"
ENV DEBIAN_FRONTEND=noninteractive

RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN apt-get update && apt-get install -y \
  make \
  cmake \
  g++ \
  nano \
  htop	\
  filezilla \
  iproute2 \
  iputils-ping \
  iptables \
  openjdk-11-jdk \
  fonts-liberation
  
RUN apt update && apt install -y \
  netcat \
  nmap \
  net-tools \
  ufw \
  git \
  curl \
  wget \
  chromium-chromedriver
  
RUN wget http://archive.ubuntu.com/ubuntu/pool/main/libu/libu2f-host/libu2f-udev_1.1.4-1_all.deb
RUN dpkg -i libu2f-udev_1.1.4-1_all.deb
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb
RUN apt -f install -y

# ADD id_rsa /root/.ssh/id_rsa
RUN wget -q https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /root/miniconda.sh
# ADD ./Miniconda3-latest-Linux-x86_64.sh /root/Miniconda3-latest-Linux-x86_64.sh
RUN chmod +x /root/miniconda.sh 
RUN /root/miniconda.sh -b
USER root
ENV PATH="/root/miniconda3/etc/profile.d:${PATH}"
RUN conda install python=3.8 matplotlib tqdm pandas notebook scikit-learn -y
RUN pip install pymongo
RUN pip install mysql-connector-python sqlalchemy pymysql
RUN pip install selenium==4.15.1 webdriver-manager

WORKDIR /home/project/work

