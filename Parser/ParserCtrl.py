from . import GlobalState


import re

def parse_messages(filename):
    pattern = re.compile(r'\{([^,]+),\s*([^,]+),\s*"(.+)"\}')

    results = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            match = pattern.match(line)
            if match:
                sender = match.group(1).strip()
                receiver = match.group(2).strip()
                message = match.group(3).strip()
                results.append((sender, receiver, message))
            else:
                print("Skipping malformed line:", line)

    return results
