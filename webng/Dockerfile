FROM continuumio/anaconda3
LABEL Ali Sinan Saglam <asinansaglam@gmail.com>
ENV PS1="\[\e[0;33m\]|> webng <| \[\e[1;35m\]\W\[\e[0m\] \[\e[0m\]# "

WORKDIR /src
COPY . /src
RUN apt-get update && apt-get -y install gcc 
RUN pip install --no-cache-dir -r requirements.txt \
    && python setup.py install
WORKDIR /
ENTRYPOINT ["webng"]
