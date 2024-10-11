const { exec } = require('child_process');

// Utility function to run a Python script and capture stdout and stderr
function runPythonScript(scriptPath) {
    return new Promise((resolve, reject) => {
        exec(`python3 ${scriptPath}`, (error, stdout, stderr) => {
            if (error) {
                // If there's an error, reject with both stderr and error message
                return reject({ message: error.message, stderr });
            }
            // Resolve with both stdout and stderr
            resolve({ stdout, stderr });
        });
    });
}

module.exports = { runPythonScript };
