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

# not working ?
wkhtmltopdf ./out/cv.html ./out/cv.pdf
````


## Get files

C:\Users\heimn>scp local-debian:/home/nheim/src/perso-cv-jinja/out/cv.* .


python3 ./jinja_cv/generate.py -o ./out/cv.html -t ./jinja_cv/templates/dossier_competence/dc.j2.html
