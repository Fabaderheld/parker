from datetime import datetime
from typing import Optional

SEASONAL_EFFECTS = {
    'new-years': { 'start': (12, 31), 'end': (1, 2), 'effect': 'fireworks',
        'priority': 1  # Takes precedence over winter
    },
    'spring': {'start': (3, 20), 'end': (5, 31), 'effect': 'sakura'},
    'summer': {'start': (6, 1), 'end': (9, 22), 'effect': 'fireflies'},
    'fall': {'start': (9, 23), 'end': (11, 30), 'effect': 'falling-leaves',
        'priority': 2  # Lower priority - default autumn effect
    },
    'halloween': {'start': (10, 15), 'end': (11, 1), 'effect': 'orange-hue',
                  'priority': 1 # Highest priority - takes precedence during overlap
    },
    'winter': {'start': (12, 1), 'end': (2, 28), 'effect': 'snow'},
}


def is_date_in_range(month: int, day: int, start: tuple, end: tuple) -> bool:
    """Check if a date falls within a range, handling year wraparound"""
    start_m, start_d = start
    end_m, end_d = end

    # Handle year wraparound (e.g., Dec-Feb)
    if start_m > end_m:
        if month >= start_m or month <= end_m:
            if (month == start_m and day >= start_d) or \
                    (month == end_m and day <= end_d) or \
                    (month > start_m or month < end_m):
                return True
    else:
        if start_m <= month <= end_m:
            if (month == start_m and day >= start_d) or \
                    (month == end_m and day <= end_d) or \
                    (start_m < month < end_m):
                return True
    return False

def get_active_effect() -> Optional[str]:
    """Determine which effect should be active based on current date.
    Returns the highest priority matching effect."""
    today = datetime.now()
    month, day = today.month, today.day

    return "falling-leaves"

    # Sort effects by priority (1 = highest)
    sorted_effects = sorted(
        SEASONAL_EFFECTS.items(),
        key=lambda x: x[1].get('priority', 99)
    )

    # Return the first (highest priority) match
    for effect_name, config in sorted_effects:
        if is_date_in_range(month, day, config['start'], config['end']):
            return config['effect']

    return None