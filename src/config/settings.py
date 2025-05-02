# API Configuration
API_KEYS = {
    'attom': {
        'api_key': os.getenv('ATTOM_API_KEY'),
        'base_url': 'https://api.attomdata.com',
        'endpoints': {
            'property': '/property/v1',
            'neighborhood': '/neighborhood/v1',
            'school': '/school/v1'
        }
    },
    'google_maps': {
        'api_key': os.getenv('GOOGLE_MAPS_API_KEY'),
        'base_url': 'https://maps.googleapis.com/maps/api',
        'endpoints': {
            'geocode': '/geocode/json',
            'places': '/place/textsearch/json',
            'static_maps': '/staticmap'
        }
    },
    'schooldigger': {
        'api_key': os.getenv('SCHOOLDIGGER_API_KEY'),
        'base_url': 'https://api.schooldigger.com/v1',
        'endpoints': {
            'schools': '/schools',
            'districts': '/districts'
        }
    },
    'climatecheck': {
        'api_key': os.getenv('CLIMATECHECK_API_KEY'),
        'base_url': 'https://api.climatecheck.com/v1',
        'endpoints': {
            'risk': '/risk',
            'hazards': '/hazards'
        }
    }
}

# API Rate Limits (requests per minute)
API_RATE_LIMITS = {
    'attom': 60,
    'google_maps': 50,
    'schooldigger': 30,
    'climatecheck': 20
}

# API Cache Settings (in seconds)
API_CACHE_TTL = {
    'attom': 86400,  # 24 hours
    'google_maps': 604800,  # 1 week
    'schooldigger': 604800,  # 1 week
    'climatecheck': 86400  # 24 hours
} 