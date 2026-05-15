import { z } from 'zod';

// Base User Schema
export const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  role: z.enum(['admin', 'operator', 'viewer']),
  tenant_id: z.string()
});

export type User = z.infer<typeof UserSchema>;

// Chat Message Schema
export const ChatMessageSchema = z.object({
  id: z.string().uuid(),
  session_id: z.string(),
  role: z.enum(['user', 'assistant', 'system']),
  content: z.string(),
  timestamp: z.string().datetime(),
  metadata: z.record(z.any()).optional()
});

export type ChatMessage = z.infer<typeof ChatMessageSchema>;

// Document Schema
export const DocumentSchema = z.object({
  id: z.string().uuid(),
  filename: z.string(),
  mimetype: z.string(),
  size: z.number(),
  status: z.enum(['pending', 'processing', 'completed', 'failed']),
  tenant_id: z.string(),
  uploaded_by: z.string(),
  created_at: z.string().datetime()
});

export type Document = z.infer<typeof DocumentSchema>;
