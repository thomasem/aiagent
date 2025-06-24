# Toy AI Coding Agent

Based on the
[AI Agent course](https://www.boot.dev/courses/build-ai-agent-python) on Boot.dev

## How to Run

It's most wise to run this in an isolated environment to limit exposure should
the LLM decide to run unexpected code when using this agent. As such, I have
developed a minimal Dockerfile to provide a simple way to spin up and run this
agent with minimal risk. First, the agent needs a Gemini API key. Copy the
sample `.env` file like so:

```bash
cp .env.sample .env
```

Then generate a Gemini API key
[from here](https://aistudio.google.com/app/apikey) and specify it in `.env`.
Then run `shell.sh` to set up the container environment.

```bash
./shell.sh
```

Within the container, you can now run the following to test your API key works and
functions can be called.

```bash
python main.py "read pkg/calculator.py and tell me how it works in one sentence"
```
