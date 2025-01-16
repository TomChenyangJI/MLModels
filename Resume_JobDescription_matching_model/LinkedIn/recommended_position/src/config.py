import os


job_description_json = "../job_description_json"
job_descriptions_en = "../job_descriptions_en"


os.makedirs(job_description_json,  exist_ok=True)
os.makedirs(job_descriptions_en,  exist_ok=True)


cookies = {
    'PLAY_LANG': 'en',
    'timezone': 'Asia/Shanghai',
    'li_theme': 'light',
    'li_theme_set': 'app',
    'lang': '"v=2&lang=en-us"',
}

headers = {
    'accept': 'application/vnd.linkedin.normalized+json+2.1',
    'referer': 'https://www.linkedin.com/jobs/collections/recommended/?currentJobId=4119475803&start=144',
    'sec-ch-prefers-color-scheme': 'light',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'empty',
    'sec-fetch-site': 'same-origin',
    'x-li-lang': 'en_US',
    'x-restli-protocol-version': '2.0.0',
}