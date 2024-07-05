FROM python:3.10-slim

RUN apt-get update

RUN apt-get install libmariadb-dev -y 
RUN apt-get install gcc -y

ENV LD_LIBRARY_PATH=/usr/lib/mariadb
ENV PYTHONPATH=/app
ENV TZ="Asia/Kolkata"

WORKDIR /app

RUN pip install fastapi==0.111.0 SQLAlchemy==2.0.30 mariadb==1.1.10

COPY . .

ENTRYPOINT ["uvicorn", "mcube_sizing_api:app"]

CMD [ "--host", "0.0.0.0", "--port", "8000"]