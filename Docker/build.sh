docker stop $(docker ps | grep eat_the_smoke:latest | cut -f 1 -d ' ')
shred -s10 - > random
docker build -t eat_the_smoke . && docker run --dns=192.168.0.2 -p 80:80 -t eat_the_smoke
