FROM centos/python-36-centos7:latest

# Install Dependencies
USER root

RUN adduser easybuild && echo "easybuild:easybuild" | chpasswd && usermod -aG wheel easybuild

RUN yum -y install git tar which bzip2 xz \
            epel-release make automake gcc gcc-c++ patch \
            zlib-devel openssl-devel unzip iproute file \
            pam-devel ant sudo && \
    yum -y clean all
            
RUN yum -y install lua lua-devel lua-posix lua-filesystem tcl python-keyring && \
    yum -y clean all

RUN rpm -ivh https://kojipkgs.fedoraproject.org//packages/http-parser/2.7.1/3.el7/x86_64/http-parser-2.7.1-3.el7.x86_64.rpm

# Build LMOD
ENV LMOD_VER 8.3.17

RUN mkdir -p /build
WORKDIR /build

RUN curl -LO http://github.com/TACC/Lmod/archive/${LMOD_VER}.tar.gz && \
    mv /build/${LMOD_VER}.tar.gz /build/Lmod-${LMOD_VER}.tar.gz && \
    tar xvf Lmod-${LMOD_VER}.tar.gz

WORKDIR /build/Lmod-${LMOD_VER}

RUN ./configure --prefix=/opt/apps --with-fastTCLInterp=no && \
    make install && \
    rm -rf /build && \
    ln -s /opt/apps/lmod/lmod/init/profile /etc/profile.d/z00_lmod.sh

USER 1001

WORKDIR /opt/apps

CMD /usr/bin/tail -f /dev/null
