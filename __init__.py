import logging

# __init__.py
DOMAIN = "arim"
_LOGGER = logging.getLogger(__name__)
_LOGGER.error("Loading custom component %s", DOMAIN)
from .setup import async_setup  # Import async_setup from setup.py

# Your other code remains the same
