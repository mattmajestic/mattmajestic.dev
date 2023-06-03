#!/bin/bash

docker build -t mattmajestic-dev .
docker run -p 8000:8000 mattmajestic-dev