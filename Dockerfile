# docker run -p 8888:8888 jupyter/minimal-notebook
# docker ps
# as root, otherwise ommit -u 0
# docker exec -u 0 it c77d76c7c275 /bin/bash

# Download base image
FROM jupyter/minimal-notebook:latest

USER root

# Note: Change the branch below to what you want/need

# install dependencies
RUN conda install -y numpy &&\
    conda install -y cython


# install ipywidgets for the notebook (not a strict requirement)
# and pillow to be able to expoert jpeg's
RUN conda install -y ipywidgets pillow

RUN [ "/bin/bash", "-c", "apt-get update"]
RUN [ "/bin/bash", "-c", "apt-get install -y libblas{3,-dev} liblapack{3,-dev} cmake build-essential gfortran"]
# Didn't find this, but not necessary: batlas{3-base,-dev}

# Needed for latex support of a font in Matplotlib in the notebook
RUN [ "/bin/bash", "-c", "apt-get install dvipng texlive-latex-extra texlive-fonts-recommended "]

RUN yes | pip install pymultinest
RUN git clone https://github.com/JohannesBuchner/MultiNest.git
RUN [ "/bin/bash", "-c", "cd MultiNest/build/ && cmake .. && make && cd ../../" ]
ENV LD_LIBRARY_PATH=/home/jovyan/MultiNest/lib/:$LD_LIBRARY_PATH

USER $NB_USER
# Due to some cache issue with Mybinder we ought to use COPY instead
# of git clone.
COPY --chown=1000:100 . this_repo
# REMBEBER TO checkout the BRANCH you want
RUN cd this_repo/ompy &&\
    # git submodule update --init --recursive &&\ # now in hooks/post_checkout
    pip install -e .
