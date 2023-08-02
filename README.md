# Tomori Discord Bot

Tomori is a Discord bot powered by OpenAI's GPT-3.5, designed to provide conversation, reminders, and code generation capabilities. The bot uses personality traits and information to create human-like responses.

## Installation

To run Tomori Discord Bot on your system, follow these steps:

### Prerequisites

1. **Python**: Make sure you have Python installed on your machine. The code is written in Python 3.

### Clone the Repository

1. Clone this GitHub repository to your local machine.

```bash
git clone https://github.com/your-username/tomori-discord-bot.git
```

### Install Dependencies

1. Navigate to the project directory.

```bash
cd <project-name>
```

2. Install the required dependencies(if any) using `pip`.

```bash
pip install -r requirements.txt
```

### Set Up API Keys

1. Tomori Discord Bot uses OpenAI's GPT-3.5 for generating responses. You need to set up an OpenAI API key to run the bot.

2. Obtain an API key from OpenAI (if you don't have one already) by signing up on their website.

3. Create a `.env` file in the project directory and add the following lines to it:

```
BOT_TOKEN=YOUR_DISCORD_BOT_TOKEN
OPENAI_API_KEY=YOUR_OPENAI_API_KEY
```

Replace `YOUR_DISCORD_BOT_TOKEN` with the token of your Discord bot, and `YOUR_OPENAI_API_KEY` with your OpenAI API key.

### Run the Bot

1. Now you're all set! To run the bot, execute the following command in the terminal:

```bash
python bot.py
```

Tomori Discord Bot should now be running and ready to respond to commands and generate responses.

### Usage

- The bot will respond to messages starting with the `-` command prefix.
- To have a conversation with the bot, simply send a message without the `-` prefix, and it will reply based on the conversation history.
- To set a reminder, use the `-remind` command followed by the duration in hours and the reminder message.

```
-remind 2 Buy groceries
```

- The bot will remind you of the specified message after the given duration.

- To check the time left for the reminder, use the `-left` command.

```
-left
```

- The bot will reply with the remaining time for the set reminder.

### Customization

- If you wish to customize the bot's personality, modify the `personality.py` file in the project directory.

---

**Note:** This is a simple guide for setting up and running the Tomori Discord Bot. If you encounter any issues or need further assistance, feel free to open an issue on the GitHub repository.

Happy chatting with Tomori! 🤖🗣️
