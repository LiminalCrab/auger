const express = require('express');
const app = express();
const port = 3050

//Import routes
const aggreRoute = require('./routes/aggre');

app.use('/aggre', aggreRoute);

// ROUTES
app.get('/', (req, res) => {
  res.send('Home');
})

app.get('/aggre', (req, res) => {
  res.send('AGGRE IS POINTING BACK TO INDEX.JS');
})

app.listen(port, () => {
  console.log(`listening at http://localhost:${port}`);
});

