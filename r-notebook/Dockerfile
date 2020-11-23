FROM quay.io/guimou/s2i-minimal-centos-notebook:3.6

USER root

COPY . /tmp/src

RUN rm -rf /tmp/src/.git* && \
    chown -R 1001 /tmp/src && \
    chgrp -R 0 /tmp/src && \
    chmod -R g+w /tmp/src && \
    rm -rf /tmp/scripts && \
    mv /tmp/src/.s2i/bin /tmp/scripts
    
# Setup EPEL
RUN yum -y --disableplugin=subscription-manager install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
RUN yum -y --disableplugin=subscription-manager update 

# set locales
RUN echo "LANG=en_US.utf8" >> /etc/locale.conf
RUN localedef -c -f UTF-8 -i en_US en_US.UTF-8
RUN export LC_ALL=en_US.UTF-8

# Install R
RUN yum -y --disableplugin=subscription-manager install R-core R-core-devel R-java R-cpp openssl-devel libcurl-devel \
  && echo 'options(repos = c(CRAN = "https://cran.rstudio.com/"), download.file.method = "libcurl")' >> /usr/lib64/R/etc/Rprofile.site

# There isn't a stringr package in EPEL 
RUN mkdir -p /usr/share/doc/R-3.6.0/html
RUN cp /usr/lib64/R/library/stats/html/R.css /usr/share/doc/R-3.6.0/html/
RUN R -e "install.packages(c('littler','stringr'))"

# chmod for litter execution
RUN chmod 755 /usr/lib64/R/library/littler/examples/install.r 
RUN chmod 755 /usr/lib64/R/library/littler/examples/install2.r 
RUN chmod 755 /usr/lib64/R/library/littler/examples/installGithub.r 
RUN chmod 755 /usr/lib64/R/library/littler/examples/testInstalled.r 

# set library to default (used in install.r from littler)
ENV LIBLOC /usr/lib64/R/library

# From rocker, authors Carl and Dirk, modified for centos/rh/fedora
RUN  ln -s /usr/lib64/R/library/littler/examples/install.r /usr/local/bin/install.r \
  && ln -s /usr/lib64/R/library/littler/examples/install2.r /usr/local/bin/install2.r \
  && ln -s /usr/lib64/R/library/littler/examples/installGithub.r /usr/local/bin/installGithub.r \
  && ln -s /usr/lib64/R/library/littler/examples/testInstalled.r /usr/local/bin/testInstalled.r \
  && ln -s /usr/lib64/R/library/littler/bin/r /usr/local/bin/r \
  && install.r docopt 
# end from rocker

USER 1001
    
RUN /tmp/scripts/assemble


CMD [ "/opt/app-root/builder/run" ]
