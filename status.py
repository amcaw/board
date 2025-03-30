#!/usr/bin/env python3
import json
import datetime
import os
import sys

def convert_schedule(input_file="planning.json"):
    """
    Reads planning.json file, extracts today's and tomorrow's status,
    and creates a schedule.json file with appropriate Font Awesome icons.
    """
    output_file = "schedule.json"
    
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)

    today_str = today.isoformat()
    tomorrow_str = tomorrow.isoformat()
    
    try:
        with open(input_file, 'r') as f:
            planning = json.load(f)

        icon_mapping = {
            "in": "<i class='fa-solid fa-house'></i>",
            "out": "<i class='fa-solid fa-briefcase'></i>",
            "off": "<i class='fa-solid fa-umbrella-beach'></i>"
        }

        # Get today's and tomorrow's status
        today_status = planning.get(today_str, "")
        tomorrow_status = planning.get(tomorrow_str, "")
        
        # Get icons
        today_icon = icon_mapping.get(today_status, "")
        tomorrow_icon = icon_mapping.get(tomorrow_status, "")
        
        # Combine the icons
        combined_icons = today_icon + tomorrow_icon

        output_data = [
            {
                "name": "schedule",
                "status": combined_icons
            }
        ]
        
        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        print(f"Successfully created {output_file}")
        print(f"Today's status: {today_status} → {today_icon}")
        print(f"Tomorrow's status: {tomorrow_status} → {tomorrow_icon}")
        return True

    except FileNotFoundError:
        print(f"Error: The file {input_file} was not found.")
        return False
    except json.JSONDecodeError:
        print(f"Error: {input_file} is not a valid JSON file.")
        return False
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return False

if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "planning.json"
    print(f"Using input file: {input_file}")
    convert_schedule(input_file)
