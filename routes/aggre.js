const express = require('express');

const router = express.Router();

router.get('/', (req, res) => {
    res.send('ROUTES SCREAMING INTO MY EAR');
});

router.post('/',  (req, res) => {
    console.log("AHHH")
})

module.exports = router;