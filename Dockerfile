FROM python:3.8
LABEL maintainer="andymin"

COPY ./techtrends/requirements.txt ./
COPY ./techtrends/init_db.py ./
COPY ./techtrends/schema.sql ./
COPY ./techtrends/app.py ./

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt
RUN python init_db.py
#CMD [ "python", "init_db.py" ]

EXPOSE 3111

# command to run on container start
CMD [ "python", "app.py" ]
# RUN python app.py
