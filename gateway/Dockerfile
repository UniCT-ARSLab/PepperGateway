FROM python:2.7
WORKDIR /app
COPY requirements.txt /app/requirements.txt

# ENV PYTHONPATH "${PYTHONPATH}:/pynaoqi-python2.7-2.5.5.5-linux64/lib/python2.7/site-packages"
ENV PYTHONPATH "${PYTHONPATH}:/app/pynaoqi-python2.7-2.5.5.5-linux64/lib/python2.7/site-packages"
ENV PEPPER_IP "192.168.1.20"
ENV PORT = 9559

RUN apt-get update
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 6566

CMD ["python", "main.py"]
# CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]
# CMD ["python", "-m", "app.py"]
# CMD ["flask", "run", "--host=0.0.0.0"]

# docker build -t pepper-flask-2 -f pepper-flask .
# docker run --rm -it -v /Users/giuseppepitruzzella/PepperGateway/:/app/ -p 5000:5000 --name pepper-flask-2 pepper-flask-2
# docker run --rm -it -p 5000:5000 --name pepper-flask-2 pepper-flask-2