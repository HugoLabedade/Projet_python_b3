from os import path
import requests
from io import BytesIO
from typing import Any
from fastapi import FastAPI, Request, Depends, Response
import pandas as pd
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from . import crud, models, schemas
from .database import SessionLocal, engine
from typing import List
from sqlalchemy.orm import Session
import json
from fastapi.responses import HTMLResponse
import matplotlib.pyplot as plt
import numpy as np
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from starlette.responses import StreamingResponse

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")


app = FastAPI()

# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.mount("/static", StaticFiles(directory="static"), name="static")

csv_dataset = pd.read_csv("./csv_dataset.csv", delimiter=";", on_bad_lines='skip',
                          usecols=["dataset.title", "dataset.url", "url", "title"])

lien1 = "https://www.data.gouv.fr/fr/datasets/r/b09da629-e48a-4baa-8d43-9ae28b3248da"
lien2 = "https://www.data.gouv.fr/fr/datasets/r/f4d7c0bd-8dc7-49af-8333-ec9d6abfdbee"
csv1 = "vacsi-pc-a_fra.csv"
csv2 = "covid-cedc-quot.csv"

if path.exists('vacsi-pc-a_fra.csv') == False & path.exists('covid-cedc-quot.csv') == False:
    response = requests.get(lien1)
    csv_file = open(f'./csv/{csv1}', "wb").write(response.content)

    response = requests.get(lien2)
    csv_file2 = open(f'./csv/{csv2}', "wb").write(response.content)


csv_dataset = pd.read_csv("./csv_dataset.csv", delimiter=";",
                          on_bad_lines='skip', usecols=["dataset.title", "dataset.url", "url"])


data_covid1 = pd.read_csv("./csv/covid-cedc-quot.csv", delimiter=";",
                          usecols=[
                              "clage_vacsi",
                              "jour",
                              "pc_vac_dose1",
                              "pc_vac_dose2",
                              "pc_vac_cum_dose1",
                              "pc_vac_cum_dose2"
                          ])

data_covid1 = data_covid1.rename(columns={"clage_vacsi": "classe_age", "pc_vac_dose1": "premiere_dose",
                                 "pc_vac_dose2": "deuxieme_dose", "pc_vac_cum_dose1": "premiere_dose_cum", "pc_vac_cum_dose2": "deuxieme_dose_cum"})

data_covid1.to_sql('Morbid', con=engine, if_exists='replace')
engine.execute("SELECT * FROM Morbid").fetchall()

data_covid2 = pd.read_csv("./csv/vacsi-pc-a_fra.csv", delimiter=";",
                          usecols=[
                              "reg",
                              "cl_age90",
                              "Dc_Elec_Covid_cum",
                              "jour"
                          ])

data_covid2 = data_covid2.rename(columns={"reg": "region", "cl_age90": "classe_age", "Dc_Elec_Covid_cum": "deces_covid"})
data_covid2.to_sql('Deces', con=engine, if_exists='replace')


def table1():
    df = pd.read_sql_query("SELECT * FROM Morbid", con=engine).to_json()
    parsed = json.loads(df)
    return parsed


@app.route('/', methods=("POST", "GET"))
async def index(request: Request):
    ekip = "ekip"
    return templates.TemplateResponse('index.html', {"request": request, "ekip": ekip})


@app.get("/morbid/", response_model=List[schemas.Morbid])
def read_morbid(skip: int = 0, db: Session = Depends(get_db)):
    items = crud.get_morbid(db, skip=skip)
    return items


@app.route('/test', methods=("POST", "GET"))
async def index(request: Request):
    df = pd.read_sql_query("SELECT * FROM Morbid", con=engine)
    return Response(df.to_json(orient="records"), media_type="application/json")
    # return HTMLResponse(content=df.to_html(), status_code=200)


@app.route('/graph', methods=("POST", "GET"))
async def graph(request: Request):
    df = pd.read_sql_query("SELECT * FROM Morbid", con=engine)
    plot = plt.plot(df.jour, df.deuxieme_dose_cum, c="blue", marker=",")
    plt.xticks(np.arange(0, 80, 15.0))
    plt.xlabel("Jour")
    plt.ylabel("Cumul du nombre de vaccin??s 1??re dose")
    plt.title("Evolution du nombre de vaccin??s (1??re dose) au cours du temps")
    plt.plot
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")


@app.route('/graph2', methods=("POST", "GET"))
async def graph2(requesti: Request):
    df2 = pd.read_sql_query("SELECT * FROM Deces", con=engine)
    plt.figure(figsize=(12, 12))
    plt.scatter(df2.region, df2.deces_covid, c="blue", marker=".")
    plt.xticks(df2.region)
    plt.xlabel("R??gions")
    plt.ylabel("Nombre de d??c??s")
    plt.title("Nombre de d??c??s en fonction de la r??gion")
    plt.plot
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")


@app.route('/graph3', methods=("POST", "GET"))
async def graph3(requesti: Request):
    df3 = pd.read_sql_query("SELECT * FROM Deces", con=engine)
    plt.figure(figsize=(10, 10))
    plt.scatter(df3.jour, df3.deces_covid, c="blue", marker=".")
    plt.xticks(np.arange(0, 100, 10.0))
    plt.xlabel("Date")
    plt.ylabel("Nombre de d??c??s")
    plt.title("Nombre de d??c??s dans le temps et par r??gion")
    plt.plot
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")
