const fs = require('fs')
const express = require('express');
const router = express.Router();

// getting json data

fs.readFile('./data/links.json', 'utf8', (err, fsToString) => {
    let data = JSON.parse(fsToString);
    let links = data.map(link => (link.date, link.url, link.title));
});

router.get('/', (req, res) => {
    res.send('');
});



module.exports = router;