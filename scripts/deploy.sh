CONTAINER_ID=$(sudo docker ps -q --filter ancestor=sealgull)
if [ -n "$CONTAINER_ID" ];
    then sudo docker restart $CONTAINER_ID
    else sudo docker run -d --env-file .env --mount "type=bind,source=/home/jungletryne/SealGull/src,target=/app/src" --mount "type=volume,source=sealgull-vol,dst=/app/data" sealgull
fi


