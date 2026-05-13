# perso-cv-jinja
jinja cv/resume generator

this is a jinja based generated and customisable resume

parameters :
````
./src/generate.py --help
INFO:root:démarage du programme ...
INFO:root:script start
usage: generate.py [-h] [-i INPUT] -o OUTPUT -t TEMPLATE [-d TEMPLATEDIR]

generate a resume from json data

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
  -o OUTPUT, --output OUTPUT
  -t TEMPLATE, --template TEMPLATE
  -d TEMPLATEDIR, --templateDir TEMPLATEDIR
````

running exemple :
````
python3 ./src/generate.py -o ./out/cv.html -t ./src/templates/cv.j2.html

python3 ./jinja_cv/generate.py -o ./out/cv.html -t ./jinja_cv/templates/html/cv.j2.html

ssh localhost bash /usr/local/src/nheim/perso-cv-jinja/generate_01.sh ./out/objectware_experiences.xml ./jinja_cv/templates/objectware/dc.j2.xml
scp localhost:/usr/local/src/nheim/perso-cv-jinja/out/objectware_experiences.xml objectware_experiences.xml
experiences.xml                                                                       100%  492KB   6.8MB/s   00:00

python3 ./jinja_cv/generate.py -o ./out/cv.html -t ./jinja_cv/templates/html/cv.j2.html


ssh localhost bash /usr/local/src/nheim/perso-cv-jinja/generate_01.sh ./out/merck_experiences.xml jinja_cv/templates/abylsen/merck/dc.j2.xml
scp localhost:/usr/local/src/nheim/perso-cv-jinja/out/merck_experiences.xml merck_experiences.xml

datamodel-codegen  --input tests/resources/abylsen/payload.json.schema --input-file-type jsonschema --output tests/resources/abylsen/model.py --snake-case-field --use-default-kwarg --strict-nullable --set-default-enum-member


ssh 10.1.231.15 bash /usr/local/src/nheim/perso-cv-jinja/generate_01.sh ./out/soprasteria2025_experiences_word.xml ./jinja_cv/templates/soprasteria2025/dc.j2.xml
scp 10.1.231.15:/usr/local/src/nheim/perso-cv-jinja/out/soprasteria2025_experiences_word.xml soprasteria2025_experiences_word.xml


# not working ?
wkhtmltopdf ./out/cv.html ./out/cv.pdf
````


## dependecies 

pip install pytest pydantic jinja2 python-dateutil aiohttp jsonpath_ng

## Get files

C:\Users\heimn>scp local-debian:/home/nheim/src/perso-cv-jinja/out/cv.* .


python3 ./jinja_cv/generate.py -o ./out/dc.html -t ./jinja_cv/templates/dossier_competence/dc.j2.html

wkhtmltopdf --enable-local-file-access --encoding "utf-8" ./dc.html ./dc.pdf

C:\Users\nheim>scp localhost:/home/nheim/src/perso-cv-jinja/out/dc_stork.xml .
dc_stork.xml                                                                          100%  809KB   9.3MB/s   00:00
