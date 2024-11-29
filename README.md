
# Auto-App

This app is used for convert Edi(.txt) files into .xlsx files.
 
 ### Description
This app is built wit a react app, using Javascript for the server and Pyhton script for data conversion.
## Badges

Add badges from somewhere like: [shields.io](https://shields.io/)

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)   [![forthebadge](https://forthebadge.com/images/badges/made-with-javascript.svg)](https://forthebadge.com)
## Features

- Convert Edi to xlsx
- Multiple convert at same time
- PDF to xlsx (in Progress)


## Structure

This project is separated in two pieces : the backend and the frontend can be separally run.
```
backend [http://localhost:4000]
├── downloads (files that can be download by the user)
├── helpers (to run python scripts)
├── python-scripts (python scripts especially extracting files)
├── node_modules
├── routes (js logic that is linked to a router for react components)
└── uploads (files that are sent to the server by the user and collected by 
the backend)
    └── files (test folder if a user download a folder filled by files)

frontend [http://localhost:3000]
├── public (html basics)
├── src
│   └── components (react pages)
└── node_module
```
## Installation

Git clone the repo

```bash
  cd Cab_Martini_auto-app
  bash script.sh
```
    
The script launch the backend at port 4000 [http://localhost:4000](http://localhost:3000) and the frontend (React App) at port 3000 [http://localhost:3000](http://localhost:3000), simultaneously.