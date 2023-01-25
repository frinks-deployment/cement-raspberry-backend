import express from 'express';
import { createServer } from 'http';
import bodyParser from 'body-parser';
import constants from './constants.js';

const app = express();

app.use(bodyParser.json({ limit: '50mb' }));
app.use(bodyParser.urlencoded({ limit: '50mb', extended: true, parameterLimit: 50000 }));

const httpServer = createServer(app);

app.post('/relay-stop', (req,res)=> {
  console.log(req.body);
  res.send("OK");
})

httpServer.listen(constants.PORT, async err => {
  if (err) {
      console.log('Cannot run!');
  } else {
      console.log(`API server listening on port: ${constants.PORT}`);
  }
});

export default app;