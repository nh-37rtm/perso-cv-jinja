#! /usr/bin/python3

import logging
import os
from datetime import datetime
from dateutil import relativedelta

import itertools

from typing import Generic, List, Dict, Iterable, Tuple, Any, Set

class Experience:

    # default constructor
    def __init__(self):
        self.dateDebut = None
        self.dateFin = None
        self.dureeEnMois = None
        self.depth = None
        self.__parentExperience = None

    def __setParentExperience( self, parentExperience):
        self.__parentExperience = parentExperience

    def __getParentExperience( self ) :
        return self.__parentExperience
    
    parentExperience = property( __getParentExperience, __setParentExperience )



def mapExperience(jsonExperience : Dict[str,object], jsonParentExperience : Dict[str, object]):

    experience =  Experience()
    jsonExperience['preformated'] = experience

    if 'dateDebut' in jsonExperience and 'dateFin' in jsonExperience:
        experience.dateDebut = datetime.strptime(jsonExperience['dateDebut'], '%Y-%m-%d')
        experience.dateFin = datetime.strptime(jsonExperience['dateFin'], '%Y-%m-%d')
        relDataMonth = relativedelta.relativedelta(
            experience.dateDebut, experience.dateDebut)
        experience.dureeEnMois = relDataMonth.months
    experience.parentExperience = jsonParentExperience['preformated']

    experience.depth = 'level%d' % experience.parentExperience.depth + 1


def control(jsonStructure: object):
    
        
        """ iterate over all experiences, call the control method on each and set depth"""
        for rootExperience in jsonStructure['curriculum']['experiences']:

            experiencesStack = [ rootExperience ]
            rootExperience['preformated'] = {}
            rootExperience['preformated']['depth'] = 0

            while ( len(experiencesStack) > 0 ):
                currentExperience = experiencesStack.pop()
                # controlExperience(currentExperience)
                if 'experiences' in currentExperience :
                    for subExperience in currentExperience['experiences'] :
                        if not 'preformated' in subExperience:
                            subExperience['preformated'] = {}
                        experiencesStack.append(subExperience)
                        mapExperience( currentExperienceObj,  subExperience, currentExperience )

        # experiencesAsList = list(jsonStructure['curriculum']['experiences'])

        # experiencesAsList.sort(
        #     key=lambda experience:
        #         experience['preformated']['dateDebut']
        # )
