FROM python:2.7

WORKDIR /app 
COPY requirements.txt /app/requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/app/pynaoqi-python2.7-2.5.5.5-linux64/lib/python2.7/site-packages"
ENV PEPPER_IP "192.168.1.20"
ENV PORT = 9559

RUN apt-get update
# RUN apt-get install libasound-dev libportaudio2 libportaudiocpp0 portaudio19-dev python-pyaudio -y 
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 6566

CMD python /app/main.py