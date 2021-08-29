FROM amd64/ubuntu

ENV DEBIAN_FRONTEND=noninteractiv

RUN  apt-get update &&  apt-get install -y  \
    git wget pkg-config build-essential cmake autoconf libtool zlib1g-dev lsb-release

RUN apt-get update && apt-get install -y glpk-utils  && \
    apt-get install -y coinor-cbc

RUN apt -y install swig

RUN apt-get update && apt-get install -y python3-dev python3-pip python3-venv python3-six

RUN git clone https://github.com/google/or-tools

WORKDIR /or-tools
RUN  make third_party

RUN apt-get update && apt-get install -y libglpk-dev glpk-utils glpk-doc  libgmp10 libgmpxx4ldbl
 
RUN sed -i "1 a UNIX_GLPK_DIR = \/usr\/lib\/x86_64-linux-gnu\n" ./Makefile.local

RUN find . -type f -exec sed -i 's/$(UNIX_GLPK_DIR)\/lib\/libglpk.a/-L$(UNIX_GLPK_DIR) -lglpk/g' {} +


RUN make python 

RUN make install_python
# RUN make test_python

 
