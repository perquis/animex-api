FROM alpine:3.12

RUN apk add --no-cache \
  npm \
  nodejs

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm ci

COPY . .

RUN npm run build

CMD ["npm", "start"]