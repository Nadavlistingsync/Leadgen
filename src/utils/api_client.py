import os
import requests
import time
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import json
from functools import wraps
import logging
from config.settings import API_KEYS, API_RATE_LIMITS, API_CACHE_TTL

class APIClient:
    def __init__(self):
        self.cache = {}
        self.last_request_time = {}
        self.logger = logging.getLogger(__name__)
        
    def _check_rate_limit(self, service: str) -> None:
        """Check and enforce rate limits for API calls"""
        current_time = time.time()
        if service in self.last_request_time:
            time_since_last = current_time - self.last_request_time[service]
            if time_since_last < 60 / API_RATE_LIMITS[service]:
                sleep_time = (60 / API_RATE_LIMITS[service]) - time_since_last
                time.sleep(sleep_time)
        self.last_request_time[service] = current_time

    def _get_cached_data(self, service: str, key: str) -> Optional[Dict]:
        """Get cached data if available and not expired"""
        if service in self.cache and key in self.cache[service]:
            cached_data = self.cache[service][key]
            if datetime.now() - cached_data['timestamp'] < timedelta(seconds=API_CACHE_TTL[service]):
                return cached_data['data']
        return None

    def _cache_data(self, service: str, key: str, data: Dict) -> None:
        """Cache API response data"""
        if service not in self.cache:
            self.cache[service] = {}
        self.cache[service][key] = {
            'data': data,
            'timestamp': datetime.now()
        }

    def _make_request(self, service: str, endpoint: str, params: Dict = None) -> Dict:
        """Make an API request with proper error handling"""
        try:
            self._check_rate_limit(service)
            
            config = API_KEYS[service]
            url = f"{config['base_url']}{config['endpoints'][endpoint]}"
            
            if params is None:
                params = {}
            params['api_key'] = config['api_key']
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"API request failed for {service}: {str(e)}")
            return {'error': str(e)}

    def get_property_data(self, address: str) -> Dict:
        """Get comprehensive property data from ATTOM"""
        cache_key = f"property_{address}"
        cached_data = self._get_cached_data('attom', cache_key)
        if cached_data:
            return cached_data
            
        data = self._make_request('attom', 'property', {'address': address})
        if 'error' not in data:
            self._cache_data('attom', cache_key, data)
        return data

    def get_neighborhood_data(self, lat: float, lng: float) -> Dict:
        """Get neighborhood data from ATTOM"""
        cache_key = f"neighborhood_{lat}_{lng}"
        cached_data = self._get_cached_data('attom', cache_key)
        if cached_data:
            return cached_data
            
        data = self._make_request('attom', 'neighborhood', {'lat': lat, 'lng': lng})
        if 'error' not in data:
            self._cache_data('attom', cache_key, data)
        return data

    def get_school_data(self, address: str) -> Dict:
        """Get school data from SchoolDigger"""
        cache_key = f"school_{address}"
        cached_data = self._get_cached_data('schooldigger', cache_key)
        if cached_data:
            return cached_data
            
        data = self._make_request('schooldigger', 'schools', {'address': address})
        if 'error' not in data:
            self._cache_data('schooldigger', cache_key, data)
        return data

    def get_climate_risk(self, address: str) -> Dict:
        """Get climate risk data from ClimateCheck"""
        cache_key = f"climate_{address}"
        cached_data = self._get_cached_data('climatecheck', cache_key)
        if cached_data:
            return cached_data
            
        data = self._make_request('climatecheck', 'risk', {'address': address})
        if 'error' not in data:
            self._cache_data('climatecheck', cache_key, data)
        return data

    def geocode_address(self, address: str) -> Dict:
        """Geocode address using Google Maps API"""
        cache_key = f"geocode_{address}"
        cached_data = self._get_cached_data('google_maps', cache_key)
        if cached_data:
            return cached_data
            
        data = self._make_request('google_maps', 'geocode', {'address': address})
        if 'error' not in data:
            self._cache_data('google_maps', cache_key, data)
        return data

    def get_nearby_businesses(self, lat: float, lng: float, radius: int = 5000) -> Dict:
        """Get nearby businesses using Google Maps API"""
        cache_key = f"businesses_{lat}_{lng}_{radius}"
        cached_data = self._get_cached_data('google_maps', cache_key)
        if cached_data:
            return cached_data
            
        data = self._make_request('google_maps', 'places', {
            'location': f"{lat},{lng}",
            'radius': radius,
            'type': 'business'
        })
        if 'error' not in data:
            self._cache_data('google_maps', cache_key, data)
        return data 