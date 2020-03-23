# Preguntas frecuentes de la Universidad de Valladolid (UVA) (English below)
Obtención y procesamiento de las preguntas frecuentes (FAQs) de la [página de Relaciones Internacionales](https://relint.uva.es/internacional/espanol/estudiantes/guia-bienvenida/preguntas-frecuentes/) y la [paǵina de Escuela de Doctorado](https://escueladoctorado.uva.es/export/sites/doctorado/faqs/AAFF/?lang=es) de la Universidad de Valladolid en **Español** e **Inglés**. 

Las preguntas son almacenadas tanto en formato CSV como en formato JSON. Cada fichero posee los siguientes 2 campos:

- **Question**: contiene la pregunta.
- **Answer**: contiene la respuesta.

Descomentando las líneas de código comentadas, existe la posibilidad de añadir a mayores:

- **Section**: indica la sección a la que pertenece la pregunta.

### Ejecución
El fichero [main.py](./main.py) descarga las paǵinas HTML, extrae los pares de preguntas y respuestas y los almacena en el formato descrito en ficheros CSV y JSON. Este repositorio ya contiene los ficheros HTML, así como los pares pregunta-respuesta extraidos en ficheros CSV y JSON resultantes de la ejecución de [main.py](./main.py).

Si desea ejecutar el fichero [main.py](./main.py) para volver a extraer los pares pregunta-respuesta, instale las dependencias y ejecute en la consola el comando
```
python main.py 
```
situándose en el directorio raíz del repositorio.

### Dependencias 
```
pandas==1.0.3
bs4==0.0.1
```
<hr>

# University of Valladolid (UVA) FAQS 
Obtaining and processing of the frequently asked questions (FAQs) from the [International Relations page](https://relint.uva.es/internacional/english/students/welcome-guide/faq/) and the [School Doctorate page](https://escueladoctorado.uva.es/export/sites/doctorado/faqs/AAFF/?lang=en) of the University of Valladolid in **Spanish** and **English**.

The questions are stored in both CSV and JSON formats. Each file has the following 2 fields:

- **Question**: contains the question.
- **Answer**: contains the answer.

Uncommenting the commented lines of code, there is the possibility of adding:

- **Section**: indicates the section to which the question belongs.


### Execution
The [main.py](./main.py)  file fetches the HTML pages, extracts the question-answer pairs and stores them in the format specified in CSV and JSON. This repository already contains the HTML data, as well as the question-answer pairs extracted in CSV and JSON terms results of the execution of [main.py](./main.py).

If you want to run the [main.py](./main.py) file to re-extract the question-answer pairs, install the requirements and run in console the command
```
python main.py
```
being located in the root directory of the repository.

### Requirements
```
pandas == 1.0.3
bs4 == 0.0.1
```
