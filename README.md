## English version
The focus of this project is to create an app that can get informations from people on their facebook profile after searching for all facebook database.
Furthermore you will be able to see people's informations with facial recognition after the research has done.

## Requirement
This app needs you install the following modules from PIP to work:
- selenium
- BeautifulSoup
- configparser
- sqlite3

## Support
Looking for help? Check out the instructions for getting support.

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
Este projeto tem como objetivo criar uma aplicacao capaz de, após percorrer os perfis do facebook, capturar informações de pessoas com base no seu perfil público. Após ter feito o perfilamento, você será capaz de trazer informações da pessoa após o reconhecimento facial. 

## Requisitos
Para o funcionamento da aplicação, é necessário instalar os seguintes módulos através do PIP
- selenium
- BeautifulSoup
- configparser
- sqlite3

## Support
Looking for help? Check out the instructions for getting support.


# Como utilizar
### 1. CapturaProfile
Este modulo é responsável por capturar perfis para os próximos módulos

```console
$ cd CaptureProfile
```
```console
$ python3 CapturaProfile.py
```

Após a execucao deste módulo, o arquivo do sqlite tera uma tabela com 2 campos preenchidos: nome e link. Dessa forma, os outros módulos irão analisar e capturar as informações 


### 2. CapturePhotos
Este modulo é responsável por capturar as fotos do perfil da pessoa, encontrar os rostos e salvar apenas os rostos em pastas separadas

```console
$ cd CapturePhotos
```
```console
$ python3 CapturePhotos.py
```

Após a execucao deste módulo, será criada uma pasta para cada perfil. E cada pasta irá conter os rostos encontrados no respectivo perfil

### 3. PhotoDataCreator [EM CONTRUÇÃO]
Este modulo é responsável mapear as caracteristicas dos rostos encontrados e armazenar uma hash.


## Limites do projeto
Segue os dados que o projeto NÃO faz:
- Compartilhar informações com terceiros
- Compartilhar qualquer tipo de informação


## Deseja contribuir mas nao sabe como?

Acompanhe a página de Issues. Lá você irá encontrar as atividades em aberto atualmente no projeto. 
Não sabe programar ainda? Não se preocupe, há outros tipos de atividades que você pode nos ajudar. 


## Arquitetura Básica
Este é um diagrama básico da aplicação

![alt text](https://raw.githubusercontent.com/hugohfsouza/GodEye/main/Documentation/DiagramGodEye.png?raw=true)
