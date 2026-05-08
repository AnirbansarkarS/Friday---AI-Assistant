#!/usr/bin/env bash
set -e

uvicorn backend.main:app --host 0.0.0.0 --port 8000 &
UVICORN_PID=$!

streamlit run frontend/app.py --server.address 0.0.0.0 --server.port 8501 &
STREAMLIT_PID=$!

wait -n $UVICORN_PID $STREAMLIT_PID
kill $UVICORN_PID $STREAMLIT_PID
