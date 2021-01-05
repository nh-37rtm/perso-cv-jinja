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
./src/generate.py -o ./toto.html -t ./src/templates/cv.j2.html
````

