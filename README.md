## English version
The focus of this project is to create an app that can get informations from people on their facebook profile after searching for all facebook database.
Furthermore you will be able to see people's informations with facial recognition after the research has done.

## Requirement
This app needs you install the following modules from PIP to work:

- [selenium](https://pypi.org/project/selenium/)
- [BeautifulSoup](https://pypi.org/project/beautifulsoup4/)
- [configparser](https://pypi.org/project/configparser/)
- [sqlite3](https://pypi.org/project/db-sqlite3/)
- progress (https://pypi.org/project/progress/)
- flask (https://pypi.org/project/Flask/)

## Support
Looking for help? Access the [issues page](https://github.com/hugohfsouza/GodEye/issues) and check if your question has not already been asked. If not, feel free to create a new card with your question.

# How to use
### 1. CapturaProfile
This module is responsible for taking the profiles to the next modules.

```console
$ cd CaptureProfile
```
```console
$ python3 CapturaProfile.py
```

After running this module, the sqlite file will have a screen with two filled fields: "nome" and "link". As a result of it, the other modules will analyse and get the informations.

### 2. CapturePhotos
This module is responsible for capturing the profile's photos from the owner's profile, find the face and save them in separated folders.

```console
$ cd CapturePhotos
```
```console
$ python3 CapturePhotos.py
```

After running this module, a folder will be created for each profile and every folder will contain the found faces from their respectively profiles. 

### 3. PhotoDataCreator [work in progress]
This module is responsible for tracking the found face's characteristics and stored them in a hash.

## Project's Limits
Things that the project DO NOT do:
- Share informations with others
- Share any kind of information


## Are you into helping but you don't know how to?

Follow the Issues' webpage to find the current open activities on this project.
Don't you know how to develop? Don't worry, there are other ways you can contribute.

## Basic Architecture
This is the basic diagram from the app

![alt text](https://raw.githubusercontent.com/hugohfsouza/GodEye/main/Documentation/DiagramGodEye.png?raw=true)

---

## Portuguese version
Este projeto tem como objetivo criar uma aplicacao capaz de, ap??s percorrer os perfis do facebook, capturar informa????es de pessoas com base no seu perfil p??blico. Ap??s ter feito o perfilamento, voc?? ser?? capaz de trazer informa????es da pessoa ap??s o reconhecimento facial. 

## Requisitos
Para o funcionamento da aplica????o, ?? necess??rio instalar os seguintes m??dulos atrav??s do PIP
- selenium
- BeautifulSoup
- configparser
- sqlite3
- progress (https://pypi.org/project/progress/)

## Support
Looking for help? Check out the instructions for getting support.


# Como utilizar
### 1. CapturaProfile
Este modulo ?? respons??vel por capturar perfis para os pr??ximos m??dulos

```console
$ cd CaptureProfile
```
```console
$ python3 CapturaProfile.py
```

Ap??s a execucao deste m??dulo, o arquivo do sqlite tera uma tabela com 2 campos preenchidos: nome e link. Dessa forma, os outros m??dulos ir??o analisar e capturar as informa????es 


### 2. CapturePhotos
Este modulo ?? respons??vel por capturar as fotos do perfil da pessoa, encontrar os rostos e salvar apenas os rostos em pastas separadas

```console
$ cd CapturePhotos
```
```console
$ python3 CapturePhotos.py
```

Ap??s a execucao deste m??dulo, ser?? criada uma pasta para cada perfil. E cada pasta ir?? conter os rostos encontrados no respectivo perfil

### 3. PhotoDataCreator [EM CONTRU????O]
Este modulo ?? respons??vel mapear as caracteristicas dos rostos encontrados e armazenar uma hash.


## Limites do projeto
Segue os dados que o projeto N??O faz:
- Compartilhar informa????es com terceiros
- Compartilhar qualquer tipo de informa????o


## Deseja contribuir mas nao sabe como?

Acompanhe a p??gina de Issues. L?? voc?? ir?? encontrar as atividades em aberto atualmente no projeto. 
N??o sabe programar ainda? N??o se preocupe, h?? outros tipos de atividades que voc?? pode nos ajudar. 


## Arquitetura B??sica
Este ?? um diagrama b??sico da aplica????o

![alt text](https://raw.githubusercontent.com/hugohfsouza/GodEye/main/Documentation/DiagramGodEye.png?raw=true)
