
# iMessage Fetcher API
by [ClarkTribeGames, LLC](https://www.clarktribegames.com)

`iMessage Fetcher API` is a simple HTTP server that fetches and returns iMessage data from a macOS machine. You can return data for all messages, unread messages, or specific threads.

## Features

- Fetch all iMessage data from a macOS machine.

## Prerequisites

- macOS machine with iMessage configured and functional.
- `sudo` access on the macOS machine.
- Python 3.8 or later.

## Setup

We recommend cloning this repository into `/usr/local/bin` if you plan to use this as a service. You can, however, clone and run it from anywhere. Run these commands in your terminal:

```bash
cd /usr/local/bin
git clone https://github.com/AznIronMan/imessage_api.git
```

We also recommend running this within a virtual Python environment:

```bash
cd imessage_api
python3 -m venv .env
source .env/bin/activate
```

Once you have cloned the repository, run the server:

```bash
sudo python3 server.py
```

Complete the on-screen prompts to create `.env` and `start.sh.` Press `CTRL + C` to stop the server. Use `start.sh` to start the server in the future.

## Usage

The server runs on the macOS machine and listens for HTTP requests. You can send GET requests with a query parameter type to fetch the desired messages. Here are some examples of how to fetch all messages:

```bash
# Using curl on Windows:
curl -k -G http://yourserverip:5000/messages --data-urlencode "type=all"

# Using curl on macOS or Linux:
curl -G "http://yourserverip:5000/messages?type=all"
```

```bash
# Using Postman:

Set the request type to GET.
Set the URL to http://yourserverip:5000/messages.
Under Params, add a key-value pair with key type and value all.
```

## Detailed Setup

If you have trouble with the setup, you can follow these steps:

```bash
cp .env.example .env
nano .env # or use TextEdit, VIM, VS Code, etc.
touch requirements.txt
nano requirements.txt
```
Paste these contents into your `requirements.txt` file:

```makefile
blinker==1.6.2
click==8.1.3
Flask==2.3.2
Flask-SSLify==0.1.5
itsdangerous==2.1.2
Jinja2==3.1.2
MarkupSafe==2.1.3
python-dotenv==1.0.0
Werkzeug==2.3.6
```

Then install the requirements:

```bash
pip install -r requirements.txt
```

You can then use `python3 start.sh` to start the server.

If you are running this as a service, the .plist should be in the `~/Library/LaunchAgents/` folder with the appropriate permissions.

To do so, create the following `.plist` file, replacing `yourusername` and `yourcompanyname` with your own values:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.yourcompanyname.imessageapi</string>
    <key>WorkingDirectory</key>
    <string>/usr/local/bin/imessage_api</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/sh</string>
        <string>-c</string>
        <string>export PATH=/usr/local/bin:$PATH && /usr/local/bin/imessage_api/start.sh</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
```

Ensure the `.plist` and `.sh` files have the appropriate permissions:

```bash
sudo chmod +x /usr/local/bin/imessage_api/start.sh
sudo chown yourusername:staff /Library/LaunchAgents/com.yourcompany.imessageapi.plist
sudo chmod 700 ~/Library/LaunchAgents/com.yourcompany.imessageapi.plist
```

IMPORTANT: Grant `/bin/sh`, `python3`, and `Terminal` permissions of Full Disk Access in order to access the `chat.db` file.

```markdown
	NOTE: If you have another way to get full access to the chat.db file, 
		  please contact us!  Full Disk Access was the only way that seemed 
		  worked.  Would like a more secure way to do this!
```

To do so:

 - Open `System Preferences` on your Mac. Click on `Security & Privacy`.
 - Click on the `Privacy` tab. Scroll down and click on `Full Disk Access`. 
  - Click the lock icon to make changes, you will need to enter    your password.
  - Click the `+` button to add an application. In the file chooser, press `Cmd+Shift+G` to open the `Go to the folder:`dialog. 
 - Enter `/bin` and press enter. Select `sh` and click the `Open` button. Repeat the steps above and add `Terminal` and`python3` as well.

Finally, once all the above are complete, you can start the service either by restarting your MacOS or using the command:

```bash
launchctl enable gui/$(id -u yourusername)/com.yourcompany.imessageapi 
```

## License
This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).


Please note that you should replace `yourusername` and `yourcompanyname` with your actual username and your actual company name in the *XML* and *bash* commands.

## Contact

Discord:  `AznIronMan`
E-Mail:   **geoff** `at` **clark tribe games** `dot` **com** (*no spaces and replace at with @ and dot with .*)
