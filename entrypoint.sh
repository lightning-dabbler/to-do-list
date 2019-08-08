#!/bin/bash

cp /build/Pipfile.lock /build/Pipfile /to-do-list \
    && rm -rf /build \
    && python toDoList.py