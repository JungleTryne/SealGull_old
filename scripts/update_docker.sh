# stopping our bot

CONTAINER_ID=$(sudo docker ps -q --filter ancestor=sealgull)
if [ -n "$CONTAINER_ID" ];
    then sudo docker stop $CONTAINER_ID || true
fi

# updating docker image

sudo docker build --tag sealgull .
yes | sudo docker image prune
yes | sudo docker container prune
