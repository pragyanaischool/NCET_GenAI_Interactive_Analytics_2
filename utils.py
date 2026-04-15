import json
import re

def extract_json(text):
    """
    Extract valid JSON from LLM response safely
    """

    # Try direct parse
    try:
        return json.loads(text)
    except:
        pass

    # Extract JSON block
    match = re.search(r'\{.*\}', text, re.DOTALL)

    if match:
        json_str = match.group(0)

        try:
            return json.loads(json_str)
        except:
            pass

    return None
