# docker

### docker build

docker build -t [image_name] -f setting/dockerfile .

/ex
docker build -t climate_spiral -f setting/dockerfile .

### docker run

/ex
docker run -d -p 3000:8888 --rm --name con_climate -v "$(pwd)":/workspace cliate_spiral

# .sh

chmod +x deploy.sh

./deploy.sh
