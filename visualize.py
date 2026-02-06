import json
from collections import Counter
import matplotlib.pyplot as plt

# Load JSON log data from file
with open('logs/attempts.json') as f:
    attempts = [json.loads(line) for line in f]

# Extract all IP addresses of login attempts
ips = [a['ip'] for a in attempts]

# Count the number of attempts per IP
counts = Counter(ips)

# Create bar chart using keys and values
plt.bar(counts.keys(), list(counts.values()))

# Add axis labels and title
plt.xlabel('Attacker IP Address')
plt.ylabel('Number of Login Attempts')
plt.title(' Honeypot Login Attempts Per IP')

# Rotate x-axis labels for better readability
plt.xticks(rotation=45, ha='right')

# Adjust layout to prevent clipping
plt.tight_layout()

# Display the plot in a window
plt.show()
