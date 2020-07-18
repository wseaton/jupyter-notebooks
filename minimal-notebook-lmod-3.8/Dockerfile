FROM centos/python-38-centos7:latest

# Install Dependencies
USER root

RUN yum -y --disableplugin=subscription-manager install  git tar which bzip2 xz \
            epel-release make automake gcc gcc-c++ patch \
            zlib-devel openssl-devel unzip iproute && \
    yum -y clean all
            
RUN yum -y install lua lua-devel lua-posix lua-filesystem tcl python-keyring http-parser && \
    yum -y clean all

#RUN rpm -ivh https://kojipkgs.fedoraproject.org//packages/http-parser/2.7.1/3.el7/x86_64/http-parser-2.7.1-3.el7.x86_64.rpm

# Build LMOD
ENV LMOD_VER 8.3.17

RUN mkdir -p /build
WORKDIR /build

RUN curl -LO http://github.com/TACC/Lmod/archive/${LMOD_VER}.tar.gz && \
    mv /build/${LMOD_VER}.tar.gz /build/Lmod-${LMOD_VER}.tar.gz && \
    tar xvf Lmod-${LMOD_VER}.tar.gz

WORKDIR /build/Lmod-${LMOD_VER}

RUN ./configure --prefix=/opt/apps --with-fastTCLInterp=no
RUN make install

# Cleanup
RUN rm -rf /build

# Jupyter config
COPY . /tmp/src

RUN rm -rf /tmp/src/.git* && \
    chown -R 1001 /tmp/src && \
    chgrp -R 0 /tmp/src && \
    chmod -R g+w /tmp/src && \
    rm -rf /tmp/scripts && \
    mv /tmp/src/.s2i/bin /tmp/scripts

USER 1001

ENV JUPYTER_INSTALL_LAB true

RUN /tmp/scripts/assemble

LABEL io.k8s.description="S2I builder for custom Jupyter notebooks." \
      io.k8s.display-name="Jupyter Notebook" \
      io.openshift.expose-services="8080:http" \
      io.openshift.tags="builder,jupyter" \
      io.openshift.s2i.scripts-url="image:///opt/app-root/builder"

USER 1001

WORKDIR /opt/app-root/src

CMD [ "/opt/app-root/builder/run" ]