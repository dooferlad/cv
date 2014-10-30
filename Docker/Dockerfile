FROM ubuntu:14.04
MAINTAINER docker@nanosheep.org
#RUN dpkg-divert --local --rename /usr/bin/ischroot && ln -sf /bin/true /usr/bin/ischroot
RUN apt-get update
RUN apt-get install -y curl
RUN curl -sL https://deb.nodesource.com/setup | sudo bash -

RUN apt-get -y upgrade
RUN apt-get install -y python python-dev git python-pip sudo vim supervisor nginx-full
RUN pip install requests flask
RUN pip install uwsgi

RUN npm install -g bower grunt less html-minifier

RUN useradd -G sudo --create-home --user-group --shell /bin/bash dooferlad
RUN echo 'dooferlad:12qwaszx'| chpasswd

USER dooferlad
RUN mkdir /home/dooferlad/srv

# always want to clone...
ADD random /home/dooferlad/
RUN git clone https://github.com/dooferlad/cv.git /home/dooferlad/srv/cv
ADD settings.py /home/dooferlad/srv/cv/
WORKDIR /home/dooferlad/srv/cv
ENV HOME /home/dooferlad

ADD uwsgi_params /home/dooferlad/srv/cv/
ADD uwsgi.ini /home/dooferlad/srv/cv/

WORKDIR /home/dooferlad/srv/cv/static
RUN find . -name '*.html' -exec html-minifier --remove-comments --conservative-collapse --keep-closing-slash '{}' -o '{}' \;

USER root
ADD cv.conf /etc/nginx/sites-enabled/
RUN rm /etc/nginx/sites-enabled/default
RUN mkdir -p /var/log/supervisor
ADD ./supervisord.conf /etc/supervisord.conf

EXPOSE 80 443

CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisord.conf"]
