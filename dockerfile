FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt && python -m textblob.download_corpora

COPY . .

CMD [ "python", "./main.py" ]
