cd ../src
screen -X -S SealGull-prod quit
screen -S SealGull-prod -d -m python3 main.py --env_path ../.env
