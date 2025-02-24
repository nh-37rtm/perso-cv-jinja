# !/bin/bash


set -eux

docker exec -it dev_container_python /bin/bash -c \
    "export PYTHONPATH=:./controler; cd /app/perso-cv-jinja;  \
    /opt/python/venv/bin/python3 ./jinja_cv/generate.py -o ./out/cv.html -t ./jinja_cv/templates/html/cv.j2.html"
