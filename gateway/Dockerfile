FROM python:2.7
WORKDIR /app
COPY requirements.txt /app/requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/app/pynaoqi-python2.7-2.5.7.1-linux64/lib/python2.7/site-packages"
ENV PEPPER_IP "192.168.1.20"
ENV PORT = 9559
ENV FLASK_APP="main.py"
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV="development"
ENV FLASK_RUN_PORT=5000

RUN apt-get update
RUN pip install --upgrade pip
RUN apt-get install -y libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 ffmpeg flac
RUN pip install -r requirements.txt

EXPOSE 6566
EXPOSE 5000
EXPOSE 8008

# CMD [ "python", "main.py" ]
CMD [ "python", "main.py"]
# CMD ["python", "-m", "app.py"]
# CMD ["flask", "run" ]

# docker build -t pepper-flask-2 -f pepper-flask .
# docker run --rm -it -v /Users/giuseppepitruzzella/PepperGateway/:/app/ -p 5000:5000 --name pepper-flask-2 pepper-flask-2
# docker run --rm -it -p 5000:5000 --name pepper-flask-2 pepper-flask-2