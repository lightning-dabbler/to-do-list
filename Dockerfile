FROM python:3.6

EXPOSE 2001

WORKDIR /build

COPY Pipfile Pipfile.* /build/

# COPY entrypoint.sh /build

RUN pip install --upgrade pip \
    && pip install pipenv \
    && pipenv lock --clear

RUN pipenv install --system --deploy --ignore-pipfile --skip-lock --verbose

# RUN chmod +x /build/entrypoint.sh

# CMD [ "python", "toDoList.py" ]
