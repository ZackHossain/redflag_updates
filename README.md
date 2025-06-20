# Red Flag Updates

A python-based tool to notify when new articles are posted to the [Red Flag Website](https://redflag.org.au)

## Usage

### 1. Start Flask Server

    source bin/activate

    cd src/main/notifier

    python3 notifier.py

If you are running this in test mode:

    python3 notifier.py -t

### 2. Run Scraper

    cd ..

    cd src/main/scraper

    python3 scraper.py

### 3. Set Up Scheduled running for scraper.py

Not yet implemented