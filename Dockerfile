FROM python:3.6

EXPOSE 2001

WORKDIR /to-do-list

COPY Pipfile /to-do-list

RUN pip install --upgrade pip \
    && pip install pipenv \
    && pipenv lock --clear

COPY Pipfile.lock /to-do-list

RUN pipenv install --system --deploy --ignore-pipfile --skip-lock --verbose

COPY . .


# CMD [ "python", "toDoList.py" ]
