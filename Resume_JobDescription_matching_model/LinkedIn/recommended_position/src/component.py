import requests
from config import *
import json
import re
import asyncio
from googletrans import Translator
from get_job_ids_from_one_response import get_job_ids_from_one_response


def out_wrapper(func):
    def wrapper(content):
        result = asyncio.run(func(content))
        return result
    return wrapper


@out_wrapper
async def translate_content(content) -> str:
    async with Translator() as translator:
        translations = await translator.translate(content, dest='en')
        return translations.text

def get_entries_in_page(page) -> requests.Response:
    response = requests.get(
        # f'https://www.linkedin.com/voyager/api/voyagerJobsDashJobCards?decorationId=com.linkedin.voyager.dash.deco.jobs.search.JobSearchCardsCollection-216&count=25&q=jobSearch&query=(origin:JOB_SEARCH_PAGE_JOB_FILTER,selectedFilters:(experience:List(2,3)),spellCorrectionEnabled:true)&start={25*page}',
        f'https://www.linkedin.com/voyager/api/graphql?variables=(count:24,jobCollectionSlug:recommended,query:(origin:GENERIC_JOB_COLLECTIONS_LANDING),start:{page*24})&queryId=voyagerJobsDashJobCards.bef088d2745c26e5851c152103cb2bd2',
        cookies=cookies,
        headers=headers,
    )

    with open(f"../pages/{page}.json", "w") as fi:
        fi.write(response.text)

    return response


def get_job_title(json_obj):
    title = json_obj['data']['title']
    return title


def get_jd(json_obj):
    # get_jd from json file, other than sending request to Linkedin server
    jd = json_obj['data']['description']['text']
    return jd


def get_job_description(job_id) -> requests.Response:
    # this method is used to get the job description with the job id as part of the request url
    response = requests.get(
        f'https://www.linkedin.com/voyager/api/jobs/jobPostings/{job_id}?decorationId=com.linkedin.voyager.deco.jobs.web.shared.WebFullJobPosting-65&topN=1&topNRequestedFlavors=List(TOP_APPLICANT,IN_NETWORK,COMPANY_RECRUIT,SCHOOL_RECRUIT,HIDDEN_GEM,ACTIVELY_HIRING_COMPANY)',
        cookies=cookies,
        headers=headers,
    )

    return response


def translate_title_and_jd(res_job_description, job_id):
    # https://www.linkedin.com/jobs/search/?currentJobId=4108121326
    # translate the title and jd
    if isinstance(res_job_description, requests.Response):
        json_obj = res_job_description.json()
    elif isinstance(res_job_description, dict):
        json_obj = res_job_description

    title = get_job_title(json_obj)
    jd = get_jd(json_obj)
    title_en = translate_content(title)
    jd_en = translate_content(jd)
    jd_en = "\n\n" + jd_en
    file_name = job_id + "-" + title_en + ".txt"
    file_name = file_name.replace("/", "|")
    job_url = f"https://www.linkedin.com/jobs/search/?currentJobId={job_id}"

    with open(f"{job_descriptions_en}/{file_name}", "w") as out_fi:
        content_en = "\n" + job_url + "\n\n" + title_en + "\n\n" + jd_en
        out_fi.write(content_en)
    # ----- translate work done -----


def convert_txt_to_pdf(in_file, out_file):
    # text file to pdf file
    from fpdf import FPDF

    pdf = FPDF()
    pdf.add_font('Times', '', "Times New Roman.ttf", uni=True)

    # Open the text file and read its contents
    with open(in_file, 'r') as f:
        text = f.read()

    # Add a new page to the PDF
    pdf.add_page()

    # Set the font and font size
    pdf.set_font('Times', size=12)

    # Write the text to the PDF
    pdf.write(5, text)

    # Save the PDF
    pdf.output(out_file)


def copy_files_to_another_folder(in_file, trg_foler="../job_descriptions_pdf/mannual_intervene/"):
    # with open("mannual_intervene.txt", "r") as infi:
    #     lines = infi.readlines()
    #     lines = [line.strip() for line in lines]
    import shutil
    # for line in lines:
    #     src = f"../job_descriptions_en/{line}"
    file_name = in_file.split("/")[-1]
    shutil.copyfile(in_file, trg_foler + file_name)


# get_entries_in_page(0)