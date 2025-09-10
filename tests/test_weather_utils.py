# Example test file for FrostByte Weather Bot
import unittest
from utils.weather_utils import get_weather

class TestWeatherUtils(unittest.TestCase):
    def test_get_weather_invalid_city(self):
        result = get_weather('InvalidCityName12345')
        self.assertIn("couldn't find", result)

if __name__ == '__main__':
    unittest.main()
