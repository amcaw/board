#!/usr/bin/env python3
import json
import datetime
import os
import sys

def convert_schedule(input_file="planning.json"):
    """
    Reads planning.json file, extracts today's status,
    and creates a schedule.json file with proper Font Awesome icon.
    """
    # Define output file path
    output_file = "schedule.json"
    
    # Get today's date in YYYY-MM-DD format
    today = datetime.date.today().isoformat()
    
    try:
        # Read the planning JSON file
        with open(input_file, 'r') as f:
            planning = json.load(f)
        
        # Check if today's date exists in the schedule
        if today not in planning:
            print(f"No schedule found for today ({today})")
            return False
        
        # Get today's status
        status = planning[today]
        
        # Map status to appropriate Font Awesome icon
        icon_mapping = {
            "in": "<i class='fa-solid fa-house'></i>",
            "out": "<i class='fa-solid fa-briefcase'></i>",
            "off": "<i class='fa-solid fa-umbrella-beach'></i>"
        }
        
        # Get the icon or default to empty string if status not recognized
        icon = icon_mapping.get(status, "")
        
        # Create the output data structure
        output_data = [
            {
                "name": "schedule",
                "status": icon
            }
        ]
        
        # Write the output JSON file
        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        print(f"Successfully created {output_file}")
        print(f"Today's status: {status}")
        print(f"Icon: {icon}")
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
    # Allow specifying a different input file as command line argument
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        print(f"Using input file: {input_file}")
    else:
        input_file = "planning.json"
    
    convert_schedule(input_file)
