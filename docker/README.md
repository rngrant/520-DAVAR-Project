## Run the below commands to get started with the docker image :

## Linux
```
cd docker
docker load < ubuntu-fairkit.tar.gz
docker run -p 8888:8888 --net=host -it ubuntu-fairkit bash
```

## If the above command doesnt work for MAC, try this :
```
cd docker
docker load < ubuntu-fairkit.tar.gz
docker run -p 8888:8888 -it ubuntu-fairkit bash
```
