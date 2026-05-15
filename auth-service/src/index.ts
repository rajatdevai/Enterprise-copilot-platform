import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import morgan from 'morgan';
import dotenv from 'dotenv';
import authRoutes from './routes/authRoutes.js';

dotenv.config();

const app = express();
const port = process.env.PORT || 3001;

app.use(express.json());
app.use(cors());
app.use(helmet());
app.use(morgan('dev'));

app.use('/auth', authRoutes);

app.get('/health', (req, res) => {
  res.json({ status: 'OK', service: 'Auth Service' });
});

app.listen(port, () => {
  console.log(`Auth Service running on port ${port}`);
});
