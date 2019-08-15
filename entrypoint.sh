#!/bin/bash

if [ -d "/build" ]
then
    cp /build/Pipfile.lock /build/Pipfile /to-do-list \
    && rm -rf /build \
    && python app.py
else
    python app.py
fi
