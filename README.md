# omdbapi
Movie database.


## Requirements:
- Python 3.6
- docker
- docker-compose
- pipenv



## Usage 
All api routes are in OMDb api.postman_collection.json. You can import file to postman.

Install locally:

Setup settings.py and run commands:
```bash
$ pipenv install
$ python src/manage.py migrate
$ python src/manage.py runserver
```

Run build in docker:
```bash
$ fab build && docker-compose -f build/docker-compose.yml up --build --force-recreate
```

Create superuser in docker build:
```bash
docker-compose -f build/docker-compose.yml exec omdbapi python src/manage.py createsuperuser
```

Deploy to server by ssh:
```bash
$ fab deploy --hosts <here host which is configured in ~/.ssh/config>
```
Get token:
```
POST /api/token/ HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
  "username": "admin",
  "password": "admin"
}
```

Search Movies:
```
GET /api/v1/movie?search=star wars&page=1 HTTP/1.1
Host: localhost:8000
Authorization: Bearer <JWT token here>

```

Add favourite movie:
```bash
POST /api/v1/my-user-favourite-movie/ HTTP/1.1
Host: localhost:8000
Authorization: Bearer <JWT token here>
Content-Type: application/json

{
    "title": "Star Wars: Episode VI - Return of the Jedi",
    "year": "1983",
    "imdb_id": "tt0086190",
    "type": "movie",
    "poster": "https://m.media-amazon.com/images/M/MV5BOWZlMjFiYzgtMTUzNC00Y2IzLTk1NTMtZmNhMTczNTk0ODk1XkEyXkFqcGdeQXVyNTAyODkwOQ@@._V1_SX300.jpg"
}
```

Delete favourite movie:
```bash
DELETE /api/v1/my-user-favourite-movie/<favMovieId> HTTP/1.1
Host: localhost:8000
Authorization: Bearer <JWT token here>
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW


```