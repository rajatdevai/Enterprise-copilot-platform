const express = require('express');
const cors = require('cors');
const morgan = require('morgan');
const chatRoutes = require('./routes/chatRoutes');

const app = express();

app.use(cors());
app.use(express.json());
app.use(morgan('dev'));

app.use('/api/chat', chatRoutes);

app.get('/health', (req, res) => {
    res.json({ status: 'API Gateway is healthy' });
});

module.exports = app;
