const fs = require('fs')

fs.readFile('./data/links.json', 'utf8', (err, fsToString) => {
    let data = JSON.parse(fsToString);
    console.log(data.map(link => console.log(link[0].date, link[0].url, link[0].title)))
});