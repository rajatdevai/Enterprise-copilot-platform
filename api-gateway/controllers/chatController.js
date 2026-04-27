const axios = require('axios');
const FormData = require('form-data');
const AI_SERVICE_URL = process.env.AI_SERVICE_URL || 'http://ai-service:8000';

/**
 * Handles real-time streaming chat orchestration.
 * Pipes the SSE stream from the AI service directly to the client.
 */
exports.handleChatStream = async (req, res) => {
    try {
        const { query, history } = req.body;
        const files = req.files;

        // 1. Efficiency: Preparing multipart form for internal transmission
        const form = new FormData();
        form.append('query', query || '');
        form.append('history_json', JSON.stringify(history || []));

        if (files && files.length > 0) {
            files.forEach(file => {
                form.append('files', file.buffer, {
                    filename: file.originalname,
                    contentType: file.mimetype,
                });
            });
        }

        console.log(`[Stream Orchestrator] Forwarding query to AI Service...`);

        // 2. High-Performance Stream Proxy: Use { responseType: 'stream' }
        const response = await axios.post(`${AI_SERVICE_URL}/chat/stream`, form, {
            headers: {
                ...form.getHeaders(),
            },
            responseType: 'stream',
            maxContentLength: Infinity,
            maxBodyLength: Infinity,
        });

        // 3. Set SSE headers for the client
        res.setHeader('Content-Type', 'text/event-stream');
        res.setHeader('Cache-Control', 'no-cache');
        res.setHeader('Connection', 'keep-alive');

        // 4. Pipe the stream directly to the response object
        response.data.pipe(res);

        // Handle stream closing
        response.data.on('end', () => {
            console.log('[Stream] Finished streaming to client.');
        });

    } catch (error) {
        console.error('Streaming Proxy Error:', error.message);
        res.status(500).json({ error: 'Orchestration failure', details: error.message });
    }
};
