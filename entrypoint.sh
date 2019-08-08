#!/bin/bash

if [ -d "/build" ]
then
    cp /build/Pipfile.lock /build/Pipfile /build/entrypoint.sh /to-do-list \
    && rm -rf /build \
    && python toDoList.py
else
    python toDoList.py
fi
