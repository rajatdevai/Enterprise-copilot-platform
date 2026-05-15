import express from 'express';
import axios from 'axios';
import cors from 'cors';
import helmet from 'helmet';
import morgan from 'morgan';
import dotenv from 'dotenv';
import { authMiddleware } from './middleware/auth.js';

dotenv.config();

const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());
app.use(cors());
app.use(helmet());
app.use(morgan('dev'));

// Proxy to Auth Service
app.post('/auth/*', async (req, res) => {
  try {
    const response = await axios({
      method: req.method,
      url: `${process.env.AUTH_SERVICE_URL}${req.url}`,
      data: req.body,
    });
    res.status(response.status).json(response.data);
  } catch (error: any) {
    const status = error.response?.status || 500;
    res.status(status).json(error.response?.data || { error: 'Internal Server Error' });
  }
});

// Protected AI Routes
app.use('/ai/*', authMiddleware);

app.all('/ai/*', async (req, res) => {
  try {
    const response = await axios({
      method: req.method,
      url: `${process.env.ORCHESTRATOR_URL}${req.url.replace('/ai', '')}`,
      data: req.body,
      headers: {
        'x-user-id': (req as any).user.id,
        'x-tenant-id': (req as any).user.tenant_id,
      },
    });
    res.status(response.status).json(response.data);
  } catch (error: any) {
    const status = error.response?.status || 500;
    res.status(status).json(error.response?.data || { error: 'Internal Server Error' });
  }
});

app.get('/health', (req, res) => {
  res.json({ status: 'OK', service: 'Gateway Service' });
});

app.listen(port, () => {
  console.log(`Gateway Service running on port ${port}`);
});
