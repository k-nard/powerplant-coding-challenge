FROM docker.io/python:3.10-alpine
ENV TZ=Europe/Brussels

RUN apk add -U -u --no-cache tzdata alpine-sdk rsync \
&& addgroup -g 1000 -S django && adduser -h /django -G django -u 1000 -S django

COPY . /tmp
RUN rsync -a --delete --chown=django:django --chmod=D2750,F0640 /tmp/ /django/ && rm -rf /tmp && mkdir /tmp && chmod 1777 /tmp

RUN pip install --upgrade pip && pip install --upgrade -r /django/requirements.txt \
&& apk del -r --clean-protected apk-tools rsync alpine-sdk \
&& rm -rf /root/.cache /django/.git* /django/.idea /django/.cache /django/requirements.txt

USER 1000:1000
WORKDIR /django

CMD ["gunicorn", "--bind", "0.0.0.0:8888", "engie_coding_challenge.wsgi:application"]
