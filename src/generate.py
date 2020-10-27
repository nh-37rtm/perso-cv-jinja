#! /usr/bin/python3

import logging
import os
import json
import pprint
import os
import codecs
import sys
import controler.controler
from jinja2 import FileSystemLoader, Template, Environment
from typing import Generic, List, Dict, Iterable, Tuple, Any
from pathlib import Path


def render():
    logging.info("rendering ...")

class RenderContext:
    # default constructor
    def __init__(self):
        self.jinjaTemplateLoader_ = FileSystemLoader(os.path.join(
    os.path.dirname(Path(__file__)), 'templates'))
        self.jinjaTemplateEnv_ = Environment(loader=self.jinjaTemplateLoader_)
        self.controler = controler.controler

    def renderTemplate( self, templateName : str, data : object ) -> str:
        logging.info("rendering %s ..." % templateName )
        template = self.jinjaTemplateEnv_.get_template(templateName)
        return template.render( context = self, data = data )


def writeFile(text):
    with codecs.open('out/xp.xml', "w", errors='strict') as fileDescriptor:
        fileDescriptor.write(text)


def main():
    readJson()


def readJson():
    logging.info("chargement du referentiel ...")
    os.curdir
    with open('src/data/cv.json', 'r', encoding='utf-8') as file:
        result = json.load(file)

        context = RenderContext()
        # control(result)
        # renderedCv = context.renderTemplate("cv.j2.html", result['curriculum'])
        # renderedCv = context.renderTemplate("efor/experiences.j2.xml", result['curriculum'])
        renderedCv = context.renderTemplate("altran/s_experiences.j2.xml", result['curriculum'])
        writeFile(renderedCv)


# =============================================
if __name__ == "__main__":

    logging.basicConfig(level=os.environ.get("LOGLEVEL", "DEBUG"))
    logging.info("démarage du programme ...")
    main()
