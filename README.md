# Årim API

## Description

Simple API to mqtt for Årim

## How to setup
1. Navigate to (Link)[https://arim.no/#pickupDayAddress]
2. Inspect element before entering your address
3. Go network tab
4. Search you address
5. You should now have an entry thats starts with ```pickupDays?days=365&region_id=```
6. Double press it and copy the url to the config
7. Edit the config to your MQTT settings
8. Instal needed requirements ```pip install -r requirements.txt```