const express = require('express');
const parser = require('body-parser');
const path = require("path");

const routes = require("./routes/index");
const config = require('./routes/nhlConfig');

const app = express();

const swaggerUI = require("swagger-ui-express");
const swaggerDocument = require("./swagger.json");

const port = config.port;

app.use(parser.urlencoded({ extended: true }));
app.use(parser.json());


// connect Swagger
app.use('/rest/api', swaggerUI.serve, swaggerUI.setup(swaggerDocument));

// connect all routes to our application
app.use('/rest', routes); 

app.use(express.static(path.join(__dirname, '..', config.publicDirectory)));

app.listen(port, () => {
  console.log(`NHL Projections HTTP Server listening on port ${port}`)
})