# Travel Agency Scraper
Scrapes [Jalan](https://www.jalan.net/en/japan_hotels_ryokan/])  English website and 
extracts a list of hotel names, address location,
room types with its pricing options in both USD and YEN
which is then saved to a CSV file with a summary.

### Requirements
- Python 3
- Docker with engine version ^27.1.1
- docker-compose

### Technology
- Python 3
- Selenium
- Beautiful Soup
- Docker
- Squid

### Setup
#### Clone the project
```
git clone https://github.com/RyanAquino/travel-agency-scraper
```
#### Navigate to directory
```
cd travel-agency-scraper
```

#### Run Containers
```
docker-compose up
```

### Validating CSV report
```
cd results/
```
