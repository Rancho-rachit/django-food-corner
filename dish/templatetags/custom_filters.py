from django import template
from django.utils import timezone

register = template.Library()

@register.filter
def time_ago(value):
    now = timezone.now()
    diff = now - value

    days, seconds = diff.days, diff.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60

    time_parts = []
    if days:
        time_parts.append(f"{days} day{'s' if days > 1 else ''}")
    if hours:
        time_parts.append(f"{hours} hour{'s' if hours > 1 else ''}")
    if minutes:
        time_parts.append(f"{minutes} minute{'s' if minutes > 1 else ''}")

    return ", ".join(time_parts) + " ago" if time_parts else "just now"

@register.filter
def format_revenue(value):
    if value >= 1_000_000:
        return f"₹{value / 1_000_000:.1f}m"  # Format as millions
    elif value >= 1_000:
        return f"₹{value / 1_000:.1f}k"  # Format as thousands
    return f"₹{value}"  # Return as is if less than 1000
