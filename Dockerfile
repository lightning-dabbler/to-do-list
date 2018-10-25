FROM python:3.6

EXPOSE 2001

WORKDIR /to-do-list

COPY requirements.txt /to-do-list
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


# CMD [ "python", "toDoList.py" ]
