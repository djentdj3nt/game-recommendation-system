
Создать образ:
```
 docker run -it --name my-dev --user $(id -u):$(id -g) -v $(pwd):/app -w /app -p 4321:4321 node:22-alpine sh
```

Запустить и зайти:
```
docker start --p 4321:4321 ai my-dev 
```


Удалить:
```
docker rm my-dev 
```


Запустить сайт на порте 4321. Если не передать `-- --host` то будет виден только внутри контейнера:
```
npm run dev -- --host
```
