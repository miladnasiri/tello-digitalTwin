"""
Tello specifications from manual
"""

FLIGHT = {
    'MAX_SPEED': {
        'SLOW_MODE': 14.4,  # km/h
        'FAST_MODE': 28.8   # km/h
    },
    'MAX_HEIGHT': 10.0,     # meters
    'MAX_RANGE': 100.0      # meters
}

VISION = {
    'HEIGHT_RANGE': {
        'MIN': 0.3,        # meters
        'MAX': 10.0,       # meters
        'OPTIMAL_MIN': 0.3,# meters
        'OPTIMAL_MAX': 6.0 # meters
    }
}

BATTERY = {
    'VOLTAGE': 3.8,        # V
    'CAPACITY': 1100,      # mAh
    'TYPE': 'LiPo',
    'ENERGY': 4.18         # Wh
}
