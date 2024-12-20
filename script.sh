#!/bin/bash

# This script is used to start the backend and frontend servers
source "auto-app/bin/activate"
set -x

cd backend
node server.js &
BACKEND_PID=$! 

npm start 
FRONTEND_PID=$!

echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
wait $BACKEND_PID  $FRONTEND_PID

kill $BACKEND_PID $FRONTEND_PID

deactivate