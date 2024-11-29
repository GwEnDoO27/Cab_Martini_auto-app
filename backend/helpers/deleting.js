const fs = require("fs")
const path = require("path")

export function deletingFolder(folder_path) {
    fs.readdir(folder_path, (err, files) => {
        if (err) throw err;
        for (const file of files) {
            fs.unlink(path.join(folder_path, file), (err) => {
                if (err) throw err;
            })
        }
    })
}