import asyncio
import json
import logging
import subprocess
import typing as t

import aiohttp
from pydantic_core import from_json
from pytest import fixture

from jinja_cv.controler import controler as JinjaCvControler
from jinja_cv.controler.controler import Experience as JinjaCvExperience
from jinja_cv.generate import RenderContext
from jinja_cv.models.har_models import IHarFileRequest
from jinja_cv.models.new_models import DefaultBaseModel, PydanticHarFileRequest
from tests._test_json_and_http import EnhancedJSONEncoder
from tests.resources.abylsen.model import Dossier, IDossier, DDossier, IModel
from tests.resources.abylsen.model import Experience as AbylsenExperience

from tests.test_lib.deep_map import deep_map_from_raw

from devops_tools.mapping_recursive import type_wrap

from datetime import datetime

from dataclasses import asdict


@fixture(name="logger")
def fix0() -> logging.Logger:
    return logging.getLogger()


def AbyExperienceMapper(
    source: JinjaCvExperience, realisations_as_html: str
) -> AbylsenExperience:

    if len(source.resultats) > 0 :
        pass

    experience = AbylsenExperience(
        
        environnement=source.environnementTechnique.replace("\n", ""),
        entreprise=source.client.replace("\n", ""),
        fin=source.dateFin.strftime("%d/%m/%Y"),
        duree=f"{source.dureeEnMois} (mois)".replace("\n", ""),
        titre=source.intitule.replace("\n", ""),
        realisations=realisations_as_html.replace("\n", "").replace("\\n", ""),
        debut="",
        contexte=source.presentation.replace("\n", ""),
        resultats=', '.join(source.resultats).replace("\n", ""),
    )

    # experience.client = source.client
    # experience.clientService = source.intitule
    # experience.projectTitle = source.intitule
    # experience.shortDescription = source.presentation
    # experience.stack = source.environnementTechnique
    # experience.startDate = source.dateDebut
    # experience.endDate = source.dateFin

    return experience


# async def jq( jq_args: t.List[str]) -> str:

#     child = subprocess.Popen(
#         args=[
#             "/usr/bin/jq",
#             *jq_args
#         ],
#         shell=False,
#         stdout=subprocess.PIPE,
#     )

#     if child.stdout is not None:
#         lines = child.stdout.readlines()
#         json_data = "".join([line.decode("utf-8") for line in lines])
#         child.wait()

#         return json_data


T = t.TypeVar("T", bound=DefaultBaseModel)


async def flush_pipe_to_str(child: subprocess.Popen) -> dict:

    json_data_str: str
    json_data: T

    if child.stdout is not None:
        lines = child.stdout.readlines()
        json_data_str = "".join([line.decode("utf-8") for line in lines])
        child.wait()

    json_data = json.loads(json_data_str)

    return json_data


async def flush_pipe_to_type(cls: t.Type[T], child: subprocess.Popen) -> T:

    json_data_str: str
    json_data: T

    if child.stdout is not None:
        lines = child.stdout.readlines()
        json_data_str = "".join([line.decode("utf-8") for line in lines])
        child.wait()

        json_data = cls.model_construct(from_json(json_data_str, allow_partial=True))

    return json_data


async def parse_har() -> t.Tuple[IHarFileRequest, IDossier, t.Dict]:

    child = subprocess.Popen(
        args=[
            "/usr/bin/jq",
            """[ .log.entries[] | select ( .request.method == "POST" ) | .request] | first""",
            "tests/resources/abylsen/portfolio.abylsen.com.har",
        ],
        shell=False,
        stdout=subprocess.PIPE,
    )

    # har_data = t.cast(IHarFileRequest, await flush_pipe_to_str(PydanticHarFileRequest, child))
    str_json = await flush_pipe_to_str(child)
    har_data = type_wrap(str_json, IHarFileRequest)

    child = subprocess.Popen(
        args=[
            "/usr/bin/jq",
            "-rf",
            "tests/resources/abylsen/payload_from_har.jq",
            "tests/resources/abylsen/portfolio.abylsen.com.har",
        ],
        shell=False,
        stdout=subprocess.PIPE,
    )
    # pdossier = await flush_pipe_to_str(Dossier, child)
    str_json = await flush_pipe_to_str(child)
    dossier = t.cast(IDossier, type_wrap(str_json, IDossier))
    return (har_data, dossier, str_json)


async def aby_async_run(experiences: t.List[AbylsenExperience]):

    har_data, dossier, str_json = await parse_har()
    dossier.experiences = experiences
    await send_response(har_data, dossier, str_json)


async def send_response(har_data: IHarFileRequest, dossier: IDossier, str_json: t.Dict):
    async with aiohttp.ClientSession() as session:

        for header in har_data.headers:

            if header.name.lower() == "content-length":
                continue

            session.headers.add(header.name, header.value)
        
        i: int = 0
        
        # aby_experiences = t.cast(t.List[AbylsenExperience], str_json['experiences'])
        
        # for experience in dossier.experiences:
        #     i = i +1
        #     if i > 1 :
        #         break
            
        #     aby_experiences.append(experience)
        str_json['experiences'] = dossier.experiences
            
        model = asdict(IModel(dossier = str_json))
        
        json_data = json.dumps(model, cls=EnhancedJSONEncoder, ensure_ascii=False)
        
        with open("tests/resources/abylsen/result_payload.json", "w+", encoding="utf-8") as file:
            file.write(json_data)
            
        session.headers.add("Content-Length", f"{len(json_data)}")

        async with session.post(har_data.url, data=json_data) as resp:

            print(resp.status)
            print(await resp.text())


def test_schema(logger: logging.Logger):

    # Read JSON from a file
    # with open("tests/resources/abylsen/payload.json", "r", encoding="utf-8") as file:
    #     json_data = file.read()
    #     dossier = Dossier.model_validate(
    #         from_json(json_data, allow_partial=True)["dossier"]
    #     )

    #     pass

    logger.info("this is the test begin")

    aby_experiences_list: t.List[AbylsenExperience] = []

    # with open('tests/resources/sii/service_payload.json', 'r', encoding='utf-8') as file:
    with open("jinja_cv/data/cv.json", "r", encoding="utf-8") as file:
        jsonCv = json.load(file)

        experience_list = JinjaCvControler.controlFlatenExperience(
            jsonCv["curriculum"]["experiences"]
        )

        render_context = RenderContext()
        render_context.templateDir = "tests/resources/abylsen/"

        for experience in experience_list:

            realisation_list = JinjaCvControler.controlRealisation(
                experience.realisations
            )
            realisations_as_html: str = ""
            for realisation in realisation_list:
                realisation_render = render_context.renderTemplate(
                    "rea.j2.html", data=realisation
                )
                realisations_as_html = f"{realisations_as_html}{realisation_render}"

            realisations_as_html = f"<ul>{realisations_as_html}</ul>"
            
            realisations_as_html = realisations_as_html.replace('\n', '')
            realisations_as_html = realisations_as_html.replace("\n", '')
            
            aby_experience = AbyExperienceMapper(experience, realisations_as_html)
            aby_experience.realisations = realisations_as_html

            aby_experiences_list.append(aby_experience)

        asyncio.run(aby_async_run(aby_experiences_list))
