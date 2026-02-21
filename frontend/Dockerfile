FROM node:20-alpine

WORKDIR /app

# Enable pnpm
RUN corepack enable && corepack prepare pnpm@latest --activate

COPY package.json pnpm-lock.yaml* ./

RUN pnpm install

COPY . .

EXPOSE 80
EXPOSE 5173

# We'll use Vite's dev server running on port 80/5173 mapping
CMD ["pnpm", "run", "dev", "--host", "0.0.0.0", "--port", "80"]
