#!/usr/bin/env python3
"""
Extract feedback from the plot test page.

Instructions:
1. Open the test results HTML page in your browser
2. Mark each plot as "Looks Correct", "Has Issues", or "Needs Review"
3. Add any notes in the text areas
4. Open the browser's Developer Console (F12 or Cmd+Option+I)
5. Type: JSON.stringify(plotFeedback, null, 2)
6. Copy the output and paste it into a file called feedback.json
7. Run this script to process the feedback
"""

import json
import sys
from datetime import datetime

def process_feedback():
    try:
        with open('feedback.json', 'r') as f:
            feedback = json.load(f)
    except FileNotFoundError:
        print("Error: feedback.json not found!")
        print("Please follow the instructions in this script to extract feedback.")
        return
    
    # Process and display feedback
    total = len(feedback)
    correct = sum(1 for f in feedback.values() if f.get('status') == 'correct')
    incorrect = sum(1 for f in feedback.values() if f.get('status') == 'incorrect')
    needs_review = sum(1 for f in feedback.values() if f.get('status') == 'needs-review')
    
    print("\n=== Plot Test Feedback Summary ===")
    print(f"Total plots: {total}")
    print(f"✓ Correct: {correct}")
    print(f"✗ Incorrect: {incorrect}")
    print(f"⚠ Needs Review: {needs_review}")
    
    print("\n=== Detailed Feedback ===")
    for plot_id, data in feedback.items():
        status = data.get('status', 'unknown')
        notes = data.get('notes', '')
        
        status_symbol = {'correct': '✓', 'incorrect': '✗', 'needs-review': '⚠'}.get(status, '?')
        print(f"\n{plot_id}: {status_symbol} {status}")
        if notes:
            print(f"  Notes: {notes}")
    
    # Save processed feedback
    output = {
        'timestamp': datetime.now().isoformat(),
        'summary': {
            'total': total,
            'correct': correct,
            'incorrect': incorrect,
            'needs_review': needs_review
        },
        'feedback': feedback
    }
    
    output_file = f'processed_feedback_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\nProcessed feedback saved to: {output_file}")

if __name__ == "__main__":
    process_feedback()