# Multi-stage Dockerfile for Next.js frontend

FROM node:18-alpine

WORKDIR /app

# Install dependencies
COPY package.json package-lock.json* ./
RUN npm ci || npm install

# Copy application code
COPY . .

# Environment variables
ENV NEXT_TELEMETRY_DISABLED 1
ENV NODE_ENV development

EXPOSE 3000

ENV PORT 3000
ENV HOSTNAME "0.0.0.0"

# Run Next.js in dev mode
CMD ["npm", "run", "dev"]
