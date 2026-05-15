const express = require('express');
const router = express.Router();
const multer = require('multer');
const chatController = require('../controllers/chatController');

// PRODUCTION SECURITY: Strict File Configuration
const upload = multer({ 
    storage: multer.memoryStorage(),
    limits: {
        fileSize: 20 * 1024 * 1024, // HARD LIMIT: 20MB per file
        files: 5 // LIMIT: Max 5 files per request
    },
    fileFilter: (req, file, cb) => {
        // Enforce allowed formats
        const allowedTypes = ['image/jpeg', 'image/png', 'application/pdf', 'text/plain', 'application/json'];
        if (allowedTypes.includes(file.mimetype)) {
            cb(null, true);
        } else {
            cb(new Error(`Security: File type ${file.mimetype} is not allowed.`));
        }
    }
});

// Real-time Streaming Endpoint
router.post('/stream', upload.array('files', 5), chatController.handleChatStream);

module.exports = router;
