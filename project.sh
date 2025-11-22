#!/bin/sh

run(){
    uv run src/main.py
}

reload(){
    uvicorn main:app --reload --port 8080
}

docker-run(){
    docker compose build
    docker compose up
}