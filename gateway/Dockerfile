FROM python:2.7

ENV FLASK_APP=/gateway/app.py
ENV FLASK_ENV=development

RUN pip install --upgrade pip
RUN pip install Flask
RUN pip install flask_sqlalchemy

RUN export FLASK_APP=${FLASK_APP}
RUN export FLASK_ENV=${FLASK_ENV}

ENTRYPOINT ["flask", "run"]