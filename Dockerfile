FROM python:3.6

ENV PYTHONUNBUFFERED 1
RUN mkdir -p /opt/omdbapi
WORKDIR /opt/omdbapi/src
RUN pip install pipenv && pipenv install --system

COPY . /opt/omdapi/
RUN pipenv install --system

RUN python manage.py collectstatic --no-input

EXPOSE 8000
CMD ["gunicorn", "-c", "config/gunicorn/conf.py", "--bind", ":8000", "--chdir", "src", "omdapi.wsgi:application"]
