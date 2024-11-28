# Characteristics

This is a React project, to build small programs to optimized the way workers work with their files. 
I've been using a express server.
backend/python-scripts/utils_functions : for cleaner python code.
I started PDF to XLSX but didn't had time. Can be based on what I did with the other app.

## Folder Structure

This project is separated in two pieces : the backend and the frontend can be separally run.

backend [http://localhost:4000]
├── downloads (files that can be download by the user)
├── helpers (to run python scripts)
├── python-scripts (python scripts especially extracting files)
├── node_modules
├── routes (js logic that is linked to a router for react components)
└── uploads (files that are sent to the server by the user and collected by the backend)
    └── files (test folder if a user download a folder filled by files)

frontend [http://localhost:3000]
├── public (html basics)
├── src
│   └── components (react pages)
└── node_modules

## Available Scripts

In the project directory, you can run:

### `cd frontend`
### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)
The extension SSH Server needs to be installed.

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)
