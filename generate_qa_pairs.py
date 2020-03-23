#!/usr/bin/env python
# coding: utf-8

# IMPORTS
import os 
import pandas as pd 
from re import sub
from json import dump
from bs4 import BeautifulSoup 
from urllib import error
from urllib.request import Request, urlopen
from functools import reduce


# GLOBAL VARIABLES
HTML_DIR = 'raw_html'
CSV_DIR = 'csv_files'
JSON_DIR = 'json_files'

OUTPUT_ROOT_NAME = "qa_pairs"
INTREL_ROOT_NAME = "intrel"
DOCTORATE_ROOT_NAME = "doctorate"
LANGUAGES =['en', 'es'] 
INTREL_URLS = {
    'en':[ 'https://relint.uva.es/internacional/english/students/welcome-guide/faq/'],

    'es':['https://relint.uva.es/internacional/espanol/estudiantes/guia-bienvenida/preguntas-frecuentes/']  
} 
DOCTORATE_URLS = {
    'en': [ 'https://escueladoctorado.uva.es/export/sites/doctorado/faqs/AAFF/?lang=en', 
            'https://escueladoctorado.uva.es/export/sites/doctorado/faqs/admisionYMatricula/?lang=en',
            'https://escueladoctorado.uva.es/export/sites/doctorado/faqs/PD/?lang=en',
            'https://escueladoctorado.uva.es/export/sites/doctorado/faqs/tesis/?lang=en',
            'https://escueladoctorado.uva.es/export/sites/doctorado/faqs/financiacion/?lang=en',
        ],

    'es':[
        'https://escueladoctorado.uva.es/export/sites/doctorado/faqs/AAFF/?lang=es', 
        'https://escueladoctorado.uva.es/export/sites/doctorado/faqs/admisionYMatricula/?lang=es',
        'https://escueladoctorado.uva.es/export/sites/doctorado/faqs/PD/?lang=es',
        'https://escueladoctorado.uva.es/export/sites/doctorado/faqs/tesis/?lang=es',
        'https://escueladoctorado.uva.es/export/sites/doctorado/faqs/financiacion/?lang=es',
    ] 
} 


def make_dirs():
    """ Creates the different directories if they don't already exist """
    print("Creating directories...")
    for lang in LANGUAGES:
        # Create directory        
        try:
            os.makedirs('{}/{}'.format(HTML_DIR, lang))
            os.makedirs('{}/{}'.format(JSON_DIR, lang))
            os.makedirs('{}/{}'.format(CSV_DIR, lang))
        except FileExistsError:
            # Directory already exists
            pass

def gen_file_path(main_dir, lang, root, i):
    """ Combines a root name and an index into an HTML file name """
    return "{}/{}/{}{}.html".format(main_dir, lang, root, i)

def download_html_files():
    """ Downloads html files if they don't exist and saves
        them in the specified directory.
    """
    print("Downloading HTML files...")
    for lang in LANGUAGES:       
        # Download UVA International Relationships FAQs
        for i, url in enumerate(INTREL_URLS[lang]):
            file_path = gen_file_path(HTML_DIR, lang, INTREL_ROOT_NAME, i+1)

            try:
                fin = open(file_path, 'rb')
                fin.close()
            except FileNotFoundError:
                # File doesn't exist
                req = Request(url,  headers={'User-Agent': 'Mozilla/5.0'})
                webContent = urlopen(req).read()
                fout = open(file_path, 'wb')
                fout.write(webContent)
                fout.close() 

        # Download UVA Doctorate School FAQs
        for i, url in enumerate(DOCTORATE_URLS[lang]):
            file_path = gen_file_path(HTML_DIR, lang, DOCTORATE_ROOT_NAME, i+1)

            try:
                fin = open(file_path, 'rb')
                fin.close()
            except FileNotFoundError:
                # File doesn't exist
                req = Request(url,  headers={'User-Agent': 'Mozilla/5.0'})
                webContent = urlopen(req).read()
                fout = open(file_path, 'wb')
                fout.write(webContent)
                fout.close() 


def process_a_tags(content):
    """ Processes each <a> tag extracting its 'href' attribute and adding 
        it between parenthesis after the text. It considers the existence
        of a <base> tag.
    """
    base = content.find('base')
  
    for a in content.find_all('a'):
        if a.previousSibling:
            href = a['href']
            text = a.get_text()
            if base != None:
                url = urljoin(base['href'], href)
            else:
                url = href            
            a.previousSibling.replaceWith(a.previousSibling + " {} ({}) ".format(text, url)) 
            a.extract() 

def extract_qa_pairs_intrel(page):
    """ Extracts all the QA pairs of a intrelX.html file and 
        creates a list of dicts with 'answer', 'question' and 'section' values
    """
    qa_pairs = [] 
    content = BeautifulSoup(page, "html.parser")
    #process_a_tags(content)
    
    sec_titles = list(map(lambda x : x.get_text(), 
                            content.find_all('div', class_='elementor-clearfix')))
    sec_contents = content.find_all('div', {'data-accordion-type':'accordion'})   

    for sec in range(len(sec_titles)):
        q_is = sec_contents[sec].find_all('i', class_='fa-accordion-icon')
        q_spans = reduce(lambda a, b: a+b, list(map(lambda x : x.find_parents('span'), q_is)))
        sec_questions = list(map(lambda x : x.get_text(), q_spans))

        sec_answers = list(map(lambda x : str(x.contents[0]).replace('<p>', '').replace('</p>', '').replace('</p>', ' ')
                        .replace('<ul>', '').replace('</ul>', '').replace('<li>', ' ').replace('</li>', ',').replace('<br/>', ' '), 
                        sec_contents[sec].find_all('div', class_=['eael-accordion-content', 'clearfix'])))

        for p in range(len(sec_questions)):
            qa_pairs.append({'question': sec_questions[p], 
                            'answer': sec_answers[p], 
                            #'page': 'relint',
                            #'section': sec_titles[sec]
                            })
    
    return qa_pairs


def extract_qa_pairs_doctorate(page):
    """ Extracts all the QA pairs of doctorateX.html file and 
        creates a list of dicts with 'answer', 'question' and 'section' values
    """
    qa_pairs = []        
    content = BeautifulSoup(page, "html.parser")
    
    sec_title = content.find_all('div', class_='headline')[1].get_text()\
                        .replace('Frequently asked questions about ', '')\
                        .replace('Frequently Asked Questions about ', '')
    
    sec_content = content.find_all('div', class_='panel-group acc-v2')[1]  

    sec_questions = list(map(lambda x: sub('\n[\t]+[\s]+', '', x.get_text()),
                            sec_content.find_all('a', class_='accordion-toggle')))

    #process_a_tags(sec_content)

    sec_answers = list(map(lambda x: str(x.contents[1].contents[0]).replace('<p style=\"text-align: justify;\">', '').replace('</p>', ' ')
                    .replace('<ul>', '').replace('</ul>', '').replace('<li>', ' ').replace('</li>', ',').replace('<br/>', ' '),
                    sec_content.find_all('div', class_='panel-body')))
    
    for p in range(len(sec_questions)):
        qa_pairs.append({'question': sec_questions[p], 
                        'answer': sec_answers[p],
                        #'page': 'doctorate', 
                        #'section': sec_title,
                         })
    return qa_pairs


def extract_qa_pairs():
    """ Extracts all the QA pairs and creates a list of dicts with 
        'answer', 'question' and 'section' values
    """
    qa_pairs = [] 
    
    for i in range(len(INTREL_URLS)):
        file_path = gen_file_path(INTREL_ROOT_NAME, i+1)
        with open(file_path, "r") as fin:
            page = fin.read()            
        qa_pairs.append(extract_qa_pairs_intrel(page))
    
    for i in range(len(DOCTORATE_URLS)):
        file_path = gen_file_path(DOCTORATE_ROOT_NAME, i+1)
        with open(file_path, "r") as fin:
            page = fin.read()            
        qa_pairs.append(extract_qa_pairs_doctorate(page))

    return list(reduce(lambda x,y: x+y, qa_pairs)) 


def save_as_json(file_name, data):
    """ Saves the provided data as a json file """
    with open('{}.json'.format(file_name), 'w', encoding='utf8') as fout:
        dump(data , fout, indent=4, sort_keys=True, ensure_ascii=False)


def save_as_csv(file_name, data):
    """ Saves the provided data as a csv file """ 
    questions = list(map(lambda p: p['question'], data))
    answers = list(map(lambda p: p['answer'], data))
    #sections = list(map(lambda p: p['section'], data))
    # d = {'Section': sections, 'Question': questions, 'Answer': answers }
    d = {'Question': questions, 'Answer': answers }
    df = pd.DataFrame(data=d)
    df.to_csv('{}.csv'.format(file_name), sep=',', index=False)


def main():
    """ MAIN """
    make_dirs() 
    download_html_files()
    # download_files()
    # qa_pairs = extract_qa_pairs()
    # save_as_json(OUTPUT_ROOT_NAME, qa_pairs)
    # save_as_csv(OUTPUT_ROOT_NAME, qa_pairs)


if __name__ == '__main__':
    main()