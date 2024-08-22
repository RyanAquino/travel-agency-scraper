FROM --platform=linux/amd64 python:3.12

WORKDIR /src

RUN apt-get update

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

RUN apt-get install ./google-chrome-stable_current_amd64.deb -y && rm ./google-chrome-stable_current_amd64.deb

COPY ./requirements.txt /src/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /src/requirements.txt

COPY . /src/

CMD ["python", "main.py"]
