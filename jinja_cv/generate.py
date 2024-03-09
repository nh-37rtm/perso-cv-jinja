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

import argparse


def render():
    logging.info("rendering ...")


class RenderContext:
    # default constructor
    def __init__(self):
        # self.jinjaTemplateLoader_ = FileSystemLoader(os.path.join(
    # os.path.dirname(Path(__file__)), os.getcwd()))
        self.jinjaTemplateLoader_ = FileSystemLoader(os.getcwd())
        self.jinjaTemplateEnv_ = Environment(loader=self.jinjaTemplateLoader_)
        self.controler = controler.controler
        self.templateDir = None

    def renderTemplate(self, templateName: str, data: object) -> str:
        templateFileName : str = os.path.join(self.templateDir, templateName)
        logging.info("rendering %s ..." % templateFileName)
        template = self.jinjaTemplateEnv_.get_template(templateFileName)
        return template.render(context=self, data=data)


def writeFile(text, fileName: str):
    with codecs.open(fileName, "w", errors='strict') as fileDescriptor:
        fileDescriptor.write(text)


def main(args: Dict):
    readJson(args)


def readJson(args: Dict):
    logging.info("chargement du referentiel ...")
    os.curdir
    with open(args.input, 'r', encoding='utf-8') as file:
        result = json.load(file)

        context = RenderContext()
        context.templateDir = args.templateDir
        

        # control(result)
        renderedCv = context.renderTemplate(
            args.template, result['curriculum'])
        # renderedCv = context.renderTemplate("efor/experiences.j2.xml", result['curriculum'])
        # renderedCv = context.renderTemplate("altran/experiences.j2.xml", result['curriculum'])
        # renderedCv = context.renderTemplate("tns/experiences.j2.xml", result['curriculum'])
        writeFile(renderedCv, fileName=args.output)


# =============================================
if __name__ == "__main__":

    logging.basicConfig(level=os.environ.get("LOGLEVEL", "DEBUG"))
    logging.info("démarage du programme ...")
    logging.getLogger().setLevel(logging.DEBUG)

    logging.info("script start")
    parser = argparse.ArgumentParser(
        description='generate a resume from json data')


    currentFileDir :str = os.path.join(os.path.dirname(Path(__file__)))


    parser.add_argument('-i', '--input', required=False,
        default=currentFileDir + '/data/cv.json')
    parser.add_argument('-o', '--output', required=True)
    parser.add_argument('-t', '--template', required=True)
    # parser.add_argument('-d', '--templateDir', required=False, default=currentFileDir + 'templates/')
    parser.add_argument('-d', '--templateDir', required=False)
    args=parser.parse_args()
    

    if ( args.templateDir == None ) :
        args.templateDir = os.path.dirname(args.template)
        args.template = os.path.basename(args.template)
    else :
        template : str =  args.template
        args.template = template.replace( os.path.commonprefix( [ args.templateDir, args.template ] ), '' )

    logging.info( "common path :" + os.path.commonpath( [ args.templateDir, args.template ] ) )


    pp = pprint.PrettyPrinter(depth=6)
    logging.info(pprint.pformat( args ))

    logging.info("script end")
    main(args)
