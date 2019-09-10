FROM python:3.7-alpine

RUN apk update
RUN pip install --no-cache-dir pipenv

WORKDIR /usr/src/app
COPY Pipfile Pipfile.lock authorize.sh operations ./
COPY src ./src

RUN pipenv install

EXPOSE 5000
CMD ["sh", "./authorize.sh"]
