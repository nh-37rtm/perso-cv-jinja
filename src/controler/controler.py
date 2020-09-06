#! /usr/bin/python3

import logging
import os
from datetime import datetime
from dateutil import relativedelta
from collections import namedtuple

import itertools

import typing
from typing import Generic, List, Dict, Iterable, Tuple, Any, Set, MutableSequence, TypeVar
from dataclasses import dataclass

# https://stackoverflow.com/questions/54913988/python-typing-for-a-subclass-of-list


class Node(List['Node']):
    # default constructor
    def __init__(self):
        self.parentNode: Node = None

    @typing.overload
    def __getitem__(self, index: int) -> 'Node': ...
    @typing.overload
    def __setitem__(self, index: int, item: 'Node') -> None: ...
    @typing.overload
    def append(self, node: 'Node') -> None: ...

    def append(self, node: 'Node') -> None:
        return super().append(node)


class JsonNode():
    def __init__(self):
        self.jsonReference = None

class Experience(JsonNode):

    # default constructor
    def __init__(self, entries):
        self.dateDebut = None
        self.dateFin = None
        self.dureeEnMois = None
        self.depth = None
        self.intitule = None
        self.presentation = None
        self.environnementTechnique = None
        self.typeExperience = None
        self.client = None
        self.poste = None
        self.depthAsCssClass = None
        self.subExperiences: List['Experience'] = []
            #https://stackoverflow.com/questions/1305532/convert-nested-python-dict-to-object
        self.__dict__.update(entries)



def mapExperience(jsonExperience: Dict[str, object]) -> Experience:

    experience: Experience = Experience( jsonExperience )
    experience.jsonReference = jsonExperience

    if experience.jsonReference['dateDebut'] != '' and experience.jsonReference['dateFin'] != '':
        experience.dateDebut = datetime.strptime(
            jsonExperience['dateDebut'], '%Y-%m-%d')
        experience.dateFin = datetime.strptime(
            jsonExperience['dateFin'], '%Y-%m-%d')
    else:
        jsonExperience['dateDebut'] = None
        jsonExperience['dateFin'] = None

    return experience


def prepareExperience(experience: Experience):

    def compareByDateDebut(experience: Experience):
        return experience.dateDebut

    def compareByDateFin(experience: Experience):
        return experience.dateFin

    if len(experience.subExperiences) > 0:
        lastExperience = max(experience.subExperiences, key=compareByDateFin)
        firstExperience = min(experience.subExperiences, key=compareByDateDebut)

        if experience.dateFin == None:
            experience.dateFin = lastExperience.dateFin

        if experience.dateDebut == None:
            experience.dateDebut = firstExperience.dateDebut

    relDataMonth = relativedelta.relativedelta(
            experience.dateFin, experience.dateDebut)
    experience.dureeEnMois = relDataMonth.months

    experience.depthAsCssClass = 'level%s' % experience.depth


def initExperiencesLegacy(jsonExperiences: List[object]) -> Tuple[List[Experience], List[Experience]]:

    experiencesList: List[Experience] = []
    rootExperienceList: List[Experience] = []

    """ iterate over all experiences, call the control method on each and set depth"""
    for rootJsonExperience in jsonExperiences:
        rootExperience = mapExperience(rootJsonExperience)
        rootExperience.depth = 0
        rootExperienceList.append(rootExperience)
        experiencesToWalk: List[Experience] = [rootExperience]

        while (len(experiencesToWalk) > 0):
            currentExperience = experiencesToWalk.pop()
            experiencesList.append(currentExperience)
            if 'experiences' in currentExperience.jsonReference:
                for subJsonExperience in currentExperience.jsonReference['experiences']:

                    subExperience = mapExperience(subJsonExperience)
                    currentExperience.subExperiences.append(subExperience)
                    subExperience.depth=currentExperience.depth + 1
                    experiencesToWalk.append(subExperience)

    return (rootExperienceList, experiencesList)

def controlExperience(jsonExperiencesStructure: object) -> List[Experience]:
        rootExperienceList, flatenedExperienceList=initExperiencesLegacy(
            jsonExperiencesStructure)

        def compare(experience: Experience):
            return experience.depth

        flatenedExperienceList.sort(
            key = compare, reverse = True
        )

        for experience in flatenedExperienceList:
            prepareExperience(experience)

        return rootExperienceList

def control(jsonStructure: object) -> List[Experience]:

        experienceList: List[Experience]=initExperiencesLegacy(
            jsonStructure['curriculum']['experiences'])

        def compare(experience: Experience):
            return experience.depth

        experienceList.sort(
            key = compare, reverse = True
        )

        for experience in experienceList:
            prepareExperience(experience)

        return experienceList

        """ iterate over all experiences, call the control method on each and set depth"""

        # experiencesAsList = list(jsonStructure['curriculum']['experiences'])

        # experiencesAsList.sort(
        #     key=lambda experience:
        #         experience['preformated']['dateDebut']
        # )
