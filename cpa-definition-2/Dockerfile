# Copyright 2021 The Custom Pod Autoscaler Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Pull in Python build of CPA
# Install dependencies for debugging
#RUN apt-get update
#RUN apt-get install jq curl -y
# Set up aliases for easy debugging
#RUN echo 'alias metrics="curl -X GET http://localhost:5000/api/v1/metrics | jq ."' >> ~/.bashrc
#RUN echo 'alias evaluation="curl -X POST http://localhost:5000/api/v1/evaluation | jq ."' >> ~/.bashrc
# Add config, evaluator and metric gathering Py scripts
# RUN apt update && \
#     apt install -yq --no-install-recommends \
#         python \
#         python-pip \
#     && apt-get clean && rm -rf /var/lib/apt/lists/*
FROM ubuntu:18.04

FROM custompodautoscaler/python:latest

WORKDIR /tmp

RUN apt update && \
    apt install -yq --no-install-recommends \
        python \
        python-pip \
        libglib2.0-0 \
        libsm6 \
        libxext6 \
        libxrender-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip\
    setuptools \
    wheel

COPY ./requirements.txt .

RUN pip install -r requirements.txt

ADD RandomForest_and_PCA.sav /tmp

ADD Regression_SVM_KNN_NB.sav /tmp

ADD config.yaml evaluate.py metric.py /

