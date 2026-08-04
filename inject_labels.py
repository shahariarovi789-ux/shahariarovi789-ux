import datetime
import xml.etree.ElementTree as ET
import os

# Register namespace to prevent ns0 prefix
ET.register_namespace('', 'http://www.w3.org/2000/svg')

# Use relative pathing so it runs correctly both locally and in GitHub Actions
svg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'github-contribution-grid-snake.svg')
tree = ET.parse(svg_path)
root = tree.getroot()

# Determine dates for each column to place months
today = datetime.date.today()
# Sunday is row 0. Find the Sunday of the current week.
days_to_sunday = (today.weekday() + 1) % 7
last_sunday = today - datetime.timedelta(days=days_to_sunday)

# We have 53 columns (indexes 0 to 52).
# Let's find the starting date of each column (Sunday of that week).
col_months = {}
for col in range(53):
    col_sunday = last_sunday - datetime.timedelta(weeks=(52 - col))
    col_months[col] = col_sunday

# Find columns where a new month starts
month_labels = []
last_month = None
for col in range(53):
    date = col_months[col]
    current_month_str = date.strftime('%b') # e.g. "Jan", "Feb"
    if current_month_str != last_month:
        # Avoid putting labels too close to each other
        if not month_labels or (col - month_labels[-1][0]) >= 3:
            month_labels.append((col, current_month_str))
            last_month = current_month_str

# Style for the labels (light grey text that is visible on dark mode)
text_style = 'font-size: 9px; fill: #7d8590; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;'

# Create month elements
for col, month_str in month_labels:
    # x coordinate matches the column start: x = 2 + col * 16
    x = 2 + col * 16
    text_elem = ET.Element('text', {
        'x': str(x),
        'y': '-10',
        'style': text_style
    })
    text_elem.text = month_str
    root.append(text_elem)

# Create weekday elements (Mon, Wed, Fri)
# Row 1 is Mon (y = 18 + 12/2 = 24), Row 3 is Wed (y = 50 + 12/2 = 56), Row 5 is Fri (y = 82 + 12/2 = 88)
weekdays = [('Mon', 27), ('Wed', 59), ('Fri', 91)]
for day_str, y in weekdays:
    text_elem = ET.Element('text', {
        'x': '-15',
        'y': str(y),
        'style': text_style + ' text-anchor: end;'
    })
    text_elem.text = day_str
    root.append(text_elem)

# Create legend text elements ("Less" and "More")
less_elem = ET.Element('text', {
    'x': '2',
    'y': '132',
    'style': text_style
})
less_elem.text = 'Less'
root.append(less_elem)

more_elem = ET.Element('text', {
    'x': '846',
    'y': '132',
    'style': text_style + ' text-anchor: end;'
})
more_elem.text = 'More'
root.append(more_elem)

# Save the updated SVG
tree.write(svg_path, encoding='utf-8', xml_declaration=True)
print("Injected month and weekday labels successfully!")
