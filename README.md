# Pixelfarm Auto-Claim Bot

![pixelfarmautoclaim](https://github.com/user-attachments/assets/57328d4d-1aee-4460-8322-d85df25aa073)
![image](https://github.com/user-attachments/assets/29c9e34a-7834-4c9b-abb8-805246ad23d1)


Pixelfarm Airdrop Bot is a Telegram bot that automatically claims rewards from the Pixelfarm app when the farming session expires.

## Buy me a coffee

If you find this bot helpful, consider buying me a coffee:

```bash
0x12aab224FA1D30Ee44575335B7767D8c89cD70A9
```

## Requirements

- Python 3.8.1
- pip (Python package installer)

## Installation

### Step 1: Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/xietsunzao/pixelfarm-auto-claim.git
cd pixelfarm-auto-claim
```

## Step 2: Install Dependencies

Install the required Python packages using requirements.txt:

```bash
pip install -r requirements.txt
```

## Step 3: Configure config.json

Create a config.json file in the src/ directory with the following content:

```json
{
  "initData": "YOUR_TELEGRAM_INIT_DATA_HERE"
}
```

How to get initData:

1. Open the Pixelfarm web app on Telegram.
2. Open the developer tools (F12 or right-click and select "Inspect").
3. Go to the "Application" tab.
4. Expand the "Session Storage" section.
5. Click key "__telegram_initParams".
6. In the "Value" field, Copy the value of the "tgWebAppData" field with right-click and select "Copy value".
6. Paste the value into the initData field in config.json.

## Step 4: Run the Bot

Run the bot using the following command:

```bash
python main.py
```

The bot will now check for the farming session's status at regular intervals and automatically claim rewards when the session expires.

## Features

- **Dynamic Farming Session Duration** :  The bot automatically adjusts the farming session duration based on the number of trees:

    - 4 hours if the player has only one tree.
    - 12 hours if the player has more than one tree.

- **Automatic Claiming** : The bot automatically claims rewards when the farming session expires and notifies the user of the status.

- **Manual Termination** : The user can manually terminate the bot by pressing `Ctrl + C` in the terminal.

## Troubleshooting

If you encounter any issues:
- Ensure you have the correct initData in config.json.
- Verify that Python 3.8.1 is installed.
- Check that all dependencies are installed using pip install -r requirements.txt.
- Ensure the bot has network access to reach the Pixelfarm API.

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```
