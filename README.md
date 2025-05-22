# WebSocket Joke Translator

A demo system featuring a **FastAPI WebSocket server** that sends random jokes to clients, and a **Python client** that translates jokes to German using Google Translate and returns the translations. The server includes a live dashboard for monitoring activity and statistics.

---

## Features

- **FastAPI WebSocket Server**: Sends jokes and receives translations from clients.
- **OpenAI Integration**: Uses OpenAI's GPT-4o to generate random jokes.
- **Live Dashboard**: Real-time stats and joke/translation history at [http://localhost:8000/](http://localhost:8000/).
- **Python Client**: Connects to the server, translates jokes to German, and sends back translations.
- **Dockerized**: Easily run both server and client with Docker Compose.

---

## Project Structure

```
.
├── client/           # Python client for translating jokes
├── server/           # FastAPI server and dashboard
├── docker-compose.yml
├── .env              # Environment variables (OpenAI API key)
├── .env.template     # Template for .env
└── README.md
```

---

## Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/)
- OpenAI API key (for joke generation)

---

## Setup

### 1. Clone the Repository

```sh
git clone <repo>
cd websockets
```

### 2. Configure Environment Variables

Copy the template and add your OpenAI API key:

```sh
cp .env.template .env
# Edit .env and set your GEMINI_API_KEY
```

Example `.env`:

```
GEMINI_API_KEY="sk-..."
```

---

## Running the Project

### Using Docker Compose

**On the first run**, build the images with:

```sh
docker-compose up --build
```

For subsequent runs, start the server and client containers with:

```sh
docker-compose up
```

- The **server** will be available at [http://localhost:8000/](http://localhost:8000/)
- The **client** will connect to the server automatically and start translating jokes.

### Stopping

Press `Ctrl+C` in the terminal, then run:

```sh
docker-compose down
```

---

## How It Works

1. **Server**:
   - Generates a random joke using OpenAI.
   - Sends the joke to the client via the `/ws` WebSocket endpoint.
   - Receives the translated joke from the client.
   - Updates the dashboard with stats and history.
2. **Client**:
   - Connects to the server's `/ws` WebSocket endpoint.
   - Receives jokes, translates them to German using Google Translate, and sends translations back.
3. **Dashboard**:
   - Visit [http://localhost:8000/](http://localhost:8000/) to see live stats and joke/translation history.

---

## Development

### Server

- Source: [`server/`](server/)
- Main entry: [`server/main.py`](server/main.py)
- WebSocket logic: [`server/routes/websocket.py`](server/routes/websocket.py)
- Joke generation: [`server/utils/generate_joke.py`](server/utils/generate_joke.py)

### Client

- Source: [`client/`](client/)
- Main entry: [`client/main.py`](client/main.py)
- WebSocket logic: [`client/services/client.py`](client/services/client.py)
- Translation logic: [`client/utils/translator.py`](client/utils/translator.py)

---

## Customization

- **Change translation language**: Edit the `"tl"` parameter in [`client/utils/translator.py`](client/utils/translator.py).
- **Change joke model**: Edit the `model` parameter in [`server/utils/generate_joke.py`](server/utils/generate_joke.py).

---

## Troubleshooting

- **OpenAI API errors**: Ensure your API key is correct and has sufficient quota.
- **Port conflicts**: Make sure port 8000 is free.
- **Logs**: Check `server/server_run.log` and `client/client_run.log` for detailed logs.

---

## License

MIT License

---

## Credits

- [FastAPI](https://fastapi.tiangolo.com/)
- [OpenAI](https://openai.com/)
- [Google Translate](https://translate.google.com/)
