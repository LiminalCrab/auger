const express = require('express')
const app = express()
const port = 3050

const aggreRoute = require('./routes/aggre');

//Import routes


// ROUTES
app.get('/', (req, res) => {
  res.send('af')
})

app.get('/aggre', (req, res) => {
  res.send('the aggregator')
})

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
})

