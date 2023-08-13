const express = require('express');
const app = express();
const port = 5000;
var path = require('path');
const bodyParser=require('body-parser')
const cookieParser=require("cookie-parser");
app.set('view engine', 'ejs');
app.use(express.urlencoded());
app.use(express.json());
app.set('views','./views');
app.use(cookieParser());
app.use(express.static('./assets'));
app.use('/', require('./routes'));
app.use('/services', require('./routes'));
app.use('/contact', require('./routes'));
app.listen(port,'0.0.0.0',function(err){
    if(err)
    {
        console.log('Error: ',err);
        console.log(`Error: ${err}`);
    }
    console.log(`Server is running on port: ${port}`);
});