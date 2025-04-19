[![Test Multiple Python Versions](https://github.com/momenashra/time-series-forecasting-CI-CD/actions/workflows/Continous_integration.yml/badge.svg)](https://github.com/momenashra/time-series-forecasting-CI-CD/actions/workflows/Continous_integration.yml)

# Multimodal RAG application with web dev environment
![ci-cd](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*QPH4dpcdC-BwA_eQykLu2Q.png)

## Create a project scaffold
* Create devlopment environment thai is cloud-based 
### Colab Notebook
* Project : Machine Learning and Deep learning Models for Predicting Sales in 3 different cities
* Project Description This project uses machine learning algorithms to predict sales for retail products based on historical data. The model leverages various features such as product category, location, and time of year.
* Technologies Used :
* ‎requirements.txt [https://github.com/momenashra/time-series-forecasting-CI-CD/blob/46227957f717f42140f1844ce96e27f582704d81/requirements.txt]
### Github Codespaces 
build out python project scaffold :
*  Makefile
*  requirments.txt
*  test_library.py
*  Dockerfile
*  Command-line=tool
*  Microservice (fast api-uvicorn)
### setup environment variables
```bash
$ cp .env.example .env
```
## Run Docker Compose Services

```bash
$ cd docker
$ cp .env.example .env
```

- update `.env` with your credentials

set you environment variables in the `.env` file like api keys
### option 1 :
1. Create Venv
 ```bash
 conda create -n mini-rag 
```
2. edit my  `~/.bashrc.sh` to source it automatically by adding
 ```bash
 conda activate mini-rag 
```
3. Clone my repo :
```bash
 git clone https://github.com/momenashra/RAG.git 
```
4. Run `make all`
5. Run this command to start app
 ```bash
 uvicorn main:app --reload --host 0.0.0.0 --port 5000
```
6. go to you local web browser and paste
 ```bash
  http:/localhost:5000/
``` 
7. upload test file `test.csv`
8. Now excute & Your are done!
### option 2 :
* You can also easily pull mu docker iamge from docker-hub using this command `docker pull momenamuhammed/time_series_forecasting:latest`
* It will make every thing for you!

