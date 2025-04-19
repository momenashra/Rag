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
*  Microservice (flask-flaskegger)
### option 1 :
1. Create Venv: `python3 -m venv ~/.time`
2. edit my  `~/.bashrc.sh` to source it automatically `~/.time/bin/activate`
3. Clone my repo : `git clone https://github.com/momenashra/time-series-forecasting-CI-CD.git`
4. Run make all
5. Run `python flask_app_UI.py`
6. go to you local web browser and past `http://127.0.0.1:5000/apidocs`
7. upload test file `test.csv`
8. Now excute & Your are done!
### option 2 :
* You can also easily pull mu docker iamge from docker-hub using this command `docker pull momenamuhammed/time_series_forecasting:latest`
* It will make every thing for you!

