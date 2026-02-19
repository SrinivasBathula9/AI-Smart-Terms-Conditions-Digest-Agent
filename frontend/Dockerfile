FROM node:18-slim

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

RUN npm run build
EXPOSE 3000
# Using a simpler CMD for dev/demo purposes
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
