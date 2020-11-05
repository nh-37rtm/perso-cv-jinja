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
        #self.dateDebut = None
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
        # https://stackoverflow.com/questions/1305532/convert-nested-python-dict-to-object
        self.__dict__.update(entries)

class Realisation(JsonNode):

    # default constructor
    def __init__(self, entries):
        self.description = None
        self.realisations: List['Realisation'] = []
        self.depth = None
        self.jsonReference = None
        # https://stackoverflow.com/questions/1305532/convert-nested-python-dict-to-object
        # self.__dict__.update(entries)

def mapExperience(jsonExperience: Dict[str, object]) -> Experience:

    experience: Experience = Experience(jsonExperience)
    experience.jsonReference = jsonExperience

    if 'dateDebut' in experience.jsonReference \
        and experience.jsonReference['dateDebut'] != '':
        experience.dateDebut = datetime.strptime(
            jsonExperience['dateDebut'], '%Y-%m-%d')
    else:
        experience.dateDebut = None

    if 'dateFin' in experience.jsonReference \
        and experience.jsonReference['dateFin'] != '':
        experience.dateFin = datetime.strptime(
            jsonExperience['dateFin'], '%Y-%m-%d')
    else:
        experience.dateFin = None

    return experience


def mapRealisation(jsonRealisation: Dict[str, object]) -> Realisation:

    realisation: Realisation = Realisation(jsonRealisation)
    realisation.jsonReference = jsonRealisation
    realisation.description = jsonRealisation['description']

    return realisation


def getFirstExperience( experiencesAsList : List[Experience]) -> Experience:

    def compareByDateDebut(experience: Experience):
        return experience.dateDebut

    subExperiencesWithDateDebut = [ experience for experience in experiencesAsList if experience.dateDebut != None ]

    if len (subExperiencesWithDateDebut) <= 0 :
        return None

    return min(subExperiencesWithDateDebut, key=compareByDateDebut)

def getLastExperience( experiencesAsList : List[Experience]) -> Experience:

    def compareByDateFin(experience: Experience):
        return experience.dateFin

    subExperiencesWithDateFin = [ experience for experience in experiencesAsList if experience.dateFin != None ]

    if len (subExperiencesWithDateFin) <= 0 :
        return None
    return max(subExperiencesWithDateFin, key=compareByDateFin)


def prepareExperience(experience: Experience):

    if len(experience.subExperiences) > 0:

        if experience.dateFin == None:
            
            lastExperience = getLastExperience( experience.subExperiences )
            experience.dateFin = None if lastExperience == None else lastExperience.dateFin

        if experience.dateDebut == None:
            
            firstExperience = getFirstExperience( experience.subExperiences )
            experience.dateDebut = firstExperience.dateDebut

    relDataMonth = relativedelta.relativedelta(
        experience.dateFin, experience.dateDebut)
    experience.dureeEnMois = relDataMonth.months + relDataMonth.years * 12

    if experience.dureeEnMois <= 0:
        logging.debug("durée de l'experience (%s) <= 0" % experience.intitule)

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
                    subExperience.depth = currentExperience.depth + 1
                    experiencesToWalk.append(subExperience)

    return (rootExperienceList, experiencesList)


def initRealisationLegacy(jsonRealisations: List[object]) -> Tuple[List[Realisation], List[Realisation]]:

    realisationsList: List[Realisation] = []
    rootRealisationList: List[Realisation] = []

    """ iterate over all Realisations, call the control method on each and set depth"""
    for rootJsonRealisation in jsonRealisations:
        rootRealisation = mapRealisation(rootJsonRealisation)
        rootRealisation.depth = 0
        rootRealisationList.append(rootRealisation)
        RealisationsToWalk: List[Realisation] = [rootRealisation]

        while (len(RealisationsToWalk) > 0):
            currentRealisation = RealisationsToWalk.pop()
            realisationsList.append(currentRealisation)
            if 'realisations' in currentRealisation.jsonReference:
                for subJsonRealisation in currentRealisation.jsonReference['realisations']:

                    subRealisation = mapRealisation(subJsonRealisation)
                    currentRealisation.realisations.append(subRealisation)
                    subRealisation.depth = currentRealisation.depth + 1
                    RealisationsToWalk.append(subRealisation)

    return (rootRealisationList, realisationsList)

def dateLoop(experiences: List[Experience]) -> None:

    def filterByDate(experience: Experience):
        if experience.dateDebut != None:
            return True
        else:
            return False

    experiencesWithDateDebut = filter(filterByDate, experiences)
    sortedExperiencesWithDate = sorted(experiencesWithDateDebut,
                                       key=lambda experience:
                                       experience.dateDebut, reverse=True)

    dateCourante = None
    for experience in sortedExperiencesWithDate:
        if experience.dateFin == None:
            experience.dateFin = dateCourante
        dateCourante = experience.dateDebut


def controlExperience(jsonExperiencesStructure: object) -> List[Experience]:
    rootExperienceList, flatenedExperienceList = initExperiencesLegacy(
        jsonExperiencesStructure)

    dateLoop(flatenedExperienceList)

    def compare(experience: Experience):
        return experience.depth

    flatenedExperienceList.sort(
        key=compare, reverse=True
    )

    for experience in flatenedExperienceList:
        prepareExperience(experience)

    return rootExperienceList

def controlFlatenExperience(jsonExperiencesStructure: object) -> List[Experience]:

    rootExperienceList, flatenedExperienceList = initExperiencesLegacy(
        jsonExperiencesStructure)

    dateLoop(flatenedExperienceList)

    def compareMissions(experience: Experience):
        logging.debug( ( "comparing with dateDebut : %s, on %s" % (experience.dateFin, experience.intitule) ))
        return experience.dateDebut

    def compare(experience: Experience):
        return experience.depth

    flatenedExperienceList.sort(
        key=compare, reverse=True
    )

    for experience in flatenedExperienceList:
        prepareExperience(experience)


    for experience in flatenedExperienceList:
        prepareExperience(experience)


    flatenedMissionList = [ experience for experience in flatenedExperienceList if experience.typeExperience != 'group' ]
    flatenedMissionList.sort(
        key=compareMissions, reverse=True
    )

    return flatenedMissionList


def controlRealisation(jsonStructure: object) -> List[Realisation] :
    rootRealisationsList, flatenedRealisationsList = initRealisationLegacy(jsonStructure)
    return rootRealisationsList
    

def control(jsonStructure: object) -> List[Experience]:

    experienceList: List[Experience] = initExperiencesLegacy(
        jsonStructure['curriculum']['experiences'])

    def compare(experience: Experience):
        return experience.depth

    experienceList.sort(
        key=compare, reverse=True
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
