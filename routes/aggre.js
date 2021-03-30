const express = require('express');

const router = express.Router();

router.get('/aggre', (req, res) => {
    res.send('Excellent')
})

module.exports = router;