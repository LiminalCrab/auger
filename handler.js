const fs = require('fs')

fs.readFile('./data/links.json', 'utf8', (err, fsToString) => {
    let data = JSON.parse(fsToString);
    data.map(link => console.log(link.date, link.url, link.title))
    
});