#!/usr/bin/env python3
import json
import datetime
import os
import sys

def get_icon_for_date(planning, date_str):
    """Return the icon HTML for a given date string based on the planning."""
    icon_mapping = {
        "in": "<i class='fa-solid fa-house'></i>",
        "out": "<i class='fa-solid fa-briefcase'></i>",
        "off": "<i class='fa-solid fa-umbrella-beach'></i>"
    }
    status = planning.get(date_str, None)
    if not status:
        return None, None
    return icon_mapping.get(status, ""), status

def convert_schedule(input_file="planning.json"):
    try:
        # Load planning JSON
        with open(input_file, 'r') as f:
            planning = json.load(f)

        # Prepare dates
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)

        # Convert both dates
        for i, date in enumerate([today, tomorrow], start=1):
            date_str = date.isoformat()
            icon, status = get_icon_for_date(planning, date_str)
            if icon is None:
                print(f"No schedule found for {date_str}")
                continue

            output_data = [
                {
                    "name": "schedule",
                    "status": icon
                }
            ]

            output_filename = f"{i}.json"
            with open(output_filename, 'w') as out_f:
                json.dump(output_data, out_f, indent=2)

            print(f"Created {output_filename} for {date_str} ({status})")

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
    convert_schedule(input_file)
