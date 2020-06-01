## Backend development workflow

```json
virtualenv env
source env/bin/activate
pip install -r requirements.txt
python manage.py runserver
```

## Frontend development workflow

```json
npm i
npm start
```

## For deploying

```json
npm run build
```


## Docker
```json
docker run -t -i -p 8000:8000 backend               # run an image
docker exec -t -i container_id bash                 # connect to a running container
docker build -t backend .
docker rmi -f $(sudo docker images -a -q)           # remove all containers and images
sudo docker system prune -a -f                      # clear all the space taken by dokcer
```
