from homeassistant.helpers import config_validation as cv
from datetime import timedelta
from datetime import datetime
import voluptuous as vol
from . import _LOGGER
from . import DOMAIN
import logging
import aiohttp
import asyncio
import time

async def get_data(url):
    headers = {"Accept": "application/json"}
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            try:
                data = (await response.json())["fetchDays"]
                return data
            except Exception as e:
                _LOGGER.error(f"Error getting data from {url}: {e}")
                return None

async def parse(hass, url):
    while True:
        frak_dict = {
            1: "waste",
            2: "cardboard",
            3: "food",
            4: "metal"
        }
        icon_dict = {
            "waste": "mdi:delete",
            "cardboard": "mdi:package-variant-closed",
            "food": "mdi:food-apple-outline",
            "metal": "mdi:recycle-variant"
        }
        data = await get_data(url)
        _LOGGER.debug(f"Data received: {data}")
        
        pattern = '%Y-%m-%d'
        current_date = datetime.now()
        for entry in data:
            if entry["fraksjonId"] not in frak_dict:
                continue

            frak = entry["fraksjonId"]
            date = entry["tommedatoer"][0].split("T")[0]
            date = datetime.strptime(date, pattern)
            _LOGGER.debug(f"date: {date}")
            days_until = (date - current_date).days + 1
            _LOGGER.info(f"days_until {frak_dict[frak]}: {days_until}")

            hass.states.async_set(
                f"sensor.arim_{frak_dict[frak]}_in_days",
                days_until,
                attributes={
                    "friendly_name": f"{frak_dict[frak].capitalize()}",
                    "icon": icon_dict[frak_dict[frak]],
                },
            )                

        await asyncio.sleep(3600)
       

async def async_setup(hass, config):
    if DOMAIN in config:
        url = config[DOMAIN].get("url")
        
        if not url:
            _LOGGER.error("No URL provided in configuration for ARIM integration.")
            return False

        # Start the update_car_data task in the asyncio loop
        hass.async_create_task(parse(hass, url))

        # Return boolean to indicate that initialization was successful.
        return True

