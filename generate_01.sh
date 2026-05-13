# !/bin/bash


set -eux

output_file="${1:-./out/cv.html}"
template_file="${2:-./jinja_cv/templates/html/cv.j2.html}"

docker exec -i dev_container_python /bin/bash -c \
    "export PYTHONPATH=:./controler; cd /app/perso-cv-jinja;  \
    /opt/python/venv/bin/python3 ./jinja_cv/generate.py -o ${output_file} -t ${template_file}"

