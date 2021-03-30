const fs = require('fs')

// getting json data
function getLinks(){ 
    fs.readFile('./data/links.json', 'utf8', (err, fsToString) => {
    let data = JSON.parse(fsToString);
    let links = data.map(link => (link.date, link.url, link.title));
    return links;
    }); 
}

getLinks();