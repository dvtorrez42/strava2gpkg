FROM continuumio/miniconda3

RUN conda config --add channels conda-forge \
    && conda update -y conda \
    && conda install pyogrio \
    && conda install -y geopandas

WORKDIR /usr/local/strava/
WORKDIR /app

COPY ./main.py /app/

CMD ["python", "main.py"]

# . : ../usr/local/strava/