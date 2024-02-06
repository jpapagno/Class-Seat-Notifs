# README: Selenium Seat Checker with SMTP Notification

This Python script utilizes Selenium to automatically check for the availability of seats in specified classes and sends an email notification using the SMTP protocol if a seat becomes available. The script is designed to work with the UC3M (Universidad Carlos III de Madrid) registration system.

## Prerequisites

- Python 3.x installed on your machine.
- Required Python packages can be installed using the following command:
  ```
  pip install selenium google-auth-oauthlib google-auth-httplib2 google-api-python-client
  ```

## Setup

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/your-username/seat-checker.git
   ```

2. Download the appropriate ChromeDriver executable for your Chrome browser version from [here](https://sites.google.com/chromium.org/driver/) and place it in the same directory as the script.

3. Update the following variables in the script:

   - `user`: Your UC3M username.
   - `passkey`: Your UC3M password.
   - `email_to_courses`: Dictionary mapping email addresses to a list of tuples representing courses to monitor. Each tuple should contain the course code, course name, and an optional list of specific group numbers to monitor.

4. If you intend to use Gmail for sending notifications, you'll need to set up a Gmail API project and download the credentials.json file. Follow the instructions [here](https://developers.google.com/gmail/api/quickstart) to set up the Gmail API.

   - Place the `credentials.json` file in the same directory as the script.
   - Ensure that the `token.json` file (generated during Gmail API setup) is also present in the same directory.

## Usage

Run the script using the following command:

```bash
python seat_checker.py
```

The script will continuously monitor the specified courses for seat availability and send email notifications when seats become available.

## Notes

- The script runs in an infinite loop, checking for seat availability every 5 minutes (`time.sleep(300)`).
- Ensure that the Chrome browser is installed on your machine and the ChromeDriver version matches your browser version.
- Make sure to keep your UC3M credentials and Gmail API credentials secure.

Feel free to customize the script to suit your specific needs and requirements.

Some class examples for UC3M:
- ("780", "Latin American Spain")
- ("13200", "Supply chain")
- ("13515", "Film Nar")
- ("10529", "American Expression 3 hour")
- ("10974", "International trade of works of art 3 hour online")
- ("11686", "Women in sci")
- ("13206", "Family business management")
- ("12884", "Middle East conflict and cinme")
- ("13018", "Classical Sociological Theory")
- ("11692", "What does it all mean")
- 19504	Strategic Design and Management
- 19809	Financial Management
- ("16641", "Culture and identity in globalization")
