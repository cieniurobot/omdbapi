FROM python:3.6
RUN apt-get update -y && apt-get upgrade -y && apt-get install -y netcat
ENV PYTHONUNBUFFERED 1
RUN mkdir -p /opt/omdbapi
WORKDIR /opt/omdbapi/src
COPY . /opt/omdbapi/
RUN pip install --upgrade pip
RUN pip install pipenv && pipenv install --system
RUN python manage.py collectstatic --clear --no-input
RUN chmod +x ../config/entrypoint.sh
EXPOSE 8000
CMD ["../config/entrypoint.sh"]
