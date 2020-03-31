#!/usr/bin/env python
# coding: utf-8

# ---IMPORTS ---
import os 
import pandas as pd 
from re import sub
from json import dump
from bs4 import BeautifulSoup 
from urllib import error
from urllib.request import Request, urlopen
from functools import reduce


# --- GLOBAL VARIABLES ---
HTML_DIR = 'raw_html'
CSV_DIR = 'csv_files'
JSON_DIR = 'json_files'
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

def download_html_intrel():
    """ Downloads the UVA International Relationships' FAQs """
    print("Downloading 'intrel' HTML files...")
    for lang in LANGUAGES:       
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

def download_html_doctorate():
    """ Downloads the UVA Doctorate School's FAQs """
    print("Downloading 'intrel' HTML files...")
    for lang in LANGUAGES:   
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

def extract_qa_pairs_intrel():
    """ Extracts all the QA pairs of doctorateX.html file and 
        creates a list of dicts with 'answer', 'question' and 'section' values
    """
    print("Extracting QA pairs from 'intrel' pages...")
    for lang in LANGUAGES:
        intrel_qa_pairs =[]       
        for i in range(len(INTREL_URLS[lang])):
            # Read HTML file   
            file_path = gen_file_path(HTML_DIR, lang, INTREL_ROOT_NAME, i+1)
            with open(file_path, "r") as fin:
                page = fin.read()            

            # Extract QA pairs from HTML file 
            page_qa_pairs = []     
            content = BeautifulSoup(page, "html.parser")   
            sec_titles = list(map(lambda x : x.get_text(), 
                            content.find_all('div', class_='elementor-clearfix')))
            sec_contents = content.find_all('div', {'data-accordion-type':'accordion'})   

            for sec in range(len(sec_titles)):
                q_is = sec_contents[sec].find_all('i', class_='fa-accordion-icon')
                q_spans = reduce(lambda a, b: a+b, list(map(lambda x : x.find_parents('span'), q_is)))
                sec_questions = list(map(lambda x : x.get_text(), q_spans))

                sec_answers = list(map(lambda x : str(x.contents[0])
                                                    .replace('<p>', '')
                                                    .replace('</p>', '\n')
                                                    .replace('<ul>', '\n')
                                                    .replace('</ul>', '')
                                                    .replace('<li>', '\n\t<b>+</b> ')
                                                    .replace('</li>', '')
                                                    .replace('<br/>', '\n'), 
                                                sec_contents[sec]\
                                                    .find_all('div', class_=['eael-accordion-content', 'clearfix'])))

                for p in range(len(sec_questions)):
                    page_qa_pairs.append({'question': sec_questions[p], 
                                    'answer': sec_answers[p], 
                                    #'section': sec_titles[sec]
                                    })
            intrel_qa_pairs.append(page_qa_pairs)
    
        intrel_qa_pairs = list(reduce(lambda x,y: x+y, intrel_qa_pairs)) 

        # Save as JSON 
        save_as_json('{}/{}/{}'.format(JSON_DIR, lang, INTREL_ROOT_NAME), intrel_qa_pairs)
        # Save as CSV 
        save_as_csv('{}/{}/{}'.format(CSV_DIR, lang, INTREL_ROOT_NAME), intrel_qa_pairs) 


def extract_qa_pairs_doctorate():
    """ Extracts all the QA pairs of doctorateX.html file and 
        creates a list of dicts with 'answer', 'question' and 'section' values
    """
    print("Extracting QA pairs from 'doctorate' pages...")
    for lang in LANGUAGES:
        doctorate_qa_pairs =[]       
        for i in range(len(DOCTORATE_URLS[lang])):
            # Read HTML file   
            file_path = gen_file_path(HTML_DIR, lang, DOCTORATE_ROOT_NAME, i+1)
            with open(file_path, "r") as fin:
                page = fin.read()            

            # Extract QA pairs from HTML file 
            page_qa_pairs = []        
            content = BeautifulSoup(page, "html.parser")
            
            sec_title = content.find_all('div', class_='headline')[1].get_text()\
                                .replace('Frequently asked questions about ', '')\
                                .replace('Frequently Asked Questions about ', '')
            
            sec_content = content.find_all('div', class_='panel-group acc-v2')[1]  

            sec_questions = list(map(lambda x: sub('\n[\t]+[\s]+', '', x.get_text()),
                                    sec_content.find_all('a', class_='accordion-toggle')))
            #process_a_tags(sec_content)
            sec_answers = list(map(lambda x: str(x.contents[1].contents[0])
                                            .replace('<p style=\"text-align: justify;\">', '')
                                            .replace('<p>', '')
                                            .replace('</p>', '\n')
                                            .replace('<ul>', '\n')
                                            .replace('</ul>', '')
                                            .replace('<li>', '\n\t<b>+</b> ')
                                            .replace('</li>', '')
                                            .replace('<br/>', '\n'), 
                                        sec_content.find_all('div', class_='panel-body')))
            
            for p in range(len(sec_questions)):
                page_qa_pairs.append({'question': sec_questions[p], 
                                'answer': sec_answers[p],
                                #'section': sec_title,
                                })
            doctorate_qa_pairs.append(page_qa_pairs)
    
        doctorate_qa_pairs = list(reduce(lambda x,y: x+y, doctorate_qa_pairs)) 

        # Save as JSON 
        save_as_json('{}/{}/{}'.format(JSON_DIR, lang, DOCTORATE_ROOT_NAME), doctorate_qa_pairs)
        # Save as CSV 
        save_as_csv('{}/{}/{}'.format(CSV_DIR, lang, DOCTORATE_ROOT_NAME), doctorate_qa_pairs) 

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
    download_html_intrel()
    download_html_doctorate()
    extract_qa_pairs_doctorate()
    extract_qa_pairs_intrel()

if __name__ == '__main__':
    main()
