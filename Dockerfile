FROM swernst/cauldron:current-ui-standard
LABEL Maintainer="renee.a.ernst@gmail.com"

COPY requirements.txt requirements.txt
COPY google-cloud-sdk.list /etc/apt/sources.list.d/google-cloud-sdk.list

RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg \
      | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add - \
 && apt-get update \
 && apt-get -y install \
      google-cloud-sdk \
 && pip install pip --upgrade \
 && pip install -r requirements.txt
