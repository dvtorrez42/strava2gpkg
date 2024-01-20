FROM continuumio/miniconda3

RUN conda config --add channels conda-forge \
    && conda update -y conda \
    && conda install -y geopandas

WORKDIR /app

COPY ./main.py /app/

CMD ["python", "main.py"]