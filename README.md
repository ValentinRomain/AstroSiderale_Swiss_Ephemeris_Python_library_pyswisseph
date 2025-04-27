# Sidereal Astrology Chrome Extension

A Chrome extension and web application for calculating precise sidereal astrology birth charts.

## Features

- Calculate accurate birth charts using sidereal zodiac calculations
- Choice of different ayanamsha systems (Lahiri, Fagan-Bradley, Krishnamurti, Raman)
- Display planet positions by sign, degrees, and house placement
- Free to use with no API key required - calculations are done with Swiss Ephemeris

## Technology Stack

- **Frontend**: React, Tailwind CSS
- **Backend**: FastAPI, PySwissEph (Swiss Ephemeris Python binding)
- **Database**: MongoDB for storing calculation history
- **Chrome Extension**: Vanilla JavaScript

## Using the Chrome Extension

1. Download the extension package (`sidereal-astrology-extension.zip`)
2. Unzip the file
3. In Chrome, go to `chrome://extensions/`
4. Enable "Developer mode" in the top-right corner
5. Click "Load unpacked" and select the unzipped folder
6. The extension icon will appear in your browser toolbar
7. Click the icon to open the extension popup
8. Enter birth details (date, time, location) and calculate your sidereal birth chart

## Web Application

The web application provides the same functionality as the Chrome extension but with a larger, more detailed interface. Access it at: https://11bc0d6b-635a-418a-aab1-c1c7088ce225.preview.emergentagent.com

## About Sidereal Astrology

Sidereal astrology uses the actual positions of constellations in the sky, taking into account the precession of the equinoxes. This is different from the more commonly used Western tropical system, which is based on seasons. Sidereal astrology is widely used in Vedic (Indian) astrology.

The main difference between sidereal and tropical zodiac systems is that there is approximately a 24-degree difference between them due to the precession of the equinoxes over the past 2,000 years. This means that your Sun sign (and other planetary placements) may be different in sidereal astrology compared to tropical astrology.

## Credits

- Calculations powered by the Swiss Ephemeris
- Built with React and FastAPI
