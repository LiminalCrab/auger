const fs = require('fs')


fs.readFile('./data/links.json', 'utf8', (err, fsToString) => {
    let data = JSON.parse(fsToString);
    console.log(data.map(link => link.url))
})