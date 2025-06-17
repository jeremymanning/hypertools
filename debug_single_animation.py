#!/usr/bin/env python3
"""
Single Animation Debug - Focus on interpolated sliding window only
"""

import os
import sys
import webbrowser
from datetime import datetime
import numpy as np
import pandas as pd

# Add parent directory to path to import hypertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hypertools as hyp

import plotly.io as pio

def create_test_data():
    """Create simple test trajectory for debugging"""
    data_trajectory = []
    for t in range(4):
        # Simple moving line: each timepoint shifts right
        x_values = np.array([t*2, t*2+1, t*2+2])  # [0,1,2], [2,3,4], [4,5,6], [6,7,8]
        y_values = np.array([0, 1, 2])            # Consistent diagonal
        
        df = pd.DataFrame({'x': x_values, 'y': y_values}, index=[t] * 3)
        data_trajectory.append(df)
    
    return pd.concat(data_trajectory)

def create_debug_html(fig):
    """Create simple HTML page with just this one animation"""
    
    # Convert to HTML
    html_div = pio.to_html(fig, include_plotlyjs=True, div_id="animation-plot")
    
    html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Debug: Interpolated Sliding Window Animation</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .debug-info {{ background: #f0f0f0; padding: 15px; margin: 10px 0; border-radius: 5px; }}
        .animation-container {{ margin: 20px 0; }}
    </style>
</head>
<body>
    <h1>🔧 Debug: Interpolated Sliding Window Animation</h1>
    
    <div class="debug-info">
        <h3>What to Look For:</h3>
        <ul>
            <li><strong>✅ GOOD:</strong> Lines should smoothly grow and slide across the plot</li>
            <li><strong>✅ GOOD:</strong> Each frame should show different X coordinates progressing smoothly</li>
            <li><strong>✅ GOOD:</strong> No jerky discrete jumps - should be continuous motion</li>
            <li><strong>❌ BAD:</strong> Frames don't change (static plot)</li>
            <li><strong>❌ BAD:</strong> Only discrete jumps every many frames</li>
        </ul>
    </div>
    
    <div class="debug-info">
        <h3>Expected Behavior:</h3>
        <p><strong>Frame 1:</strong> Line starts at x=[0,1,2]</p>
        <p><strong>Frame 10:</strong> Line has grown to show x=[0,1,2,3] approximately</p>
        <p><strong>Frame 20:</strong> Line slides to show x=[2,3,4,5] approximately</p>
        <p><strong>Final Frame:</strong> Line ends at x=[6,7,8]</p>
    </div>
    
    <div class="animation-container">
        {html_div}
    </div>
    
    <div class="debug-info">
        <h3>Manual Test Instructions:</h3>
        <ol>
            <li>Click the ▶ play button to start animation</li>
            <li>Watch carefully - do the line coordinates change smoothly?</li>
            <li>Use the slider to manually scrub through frames</li>
            <li>Check if early frames vs late frames show different data</li>
        </ol>
    </div>
    
    <script>
        console.log("Debug page loaded. Check browser developer tools for any errors.");
    </script>
</body>
</html>
"""
    
    return html_template

def main():
    print("=== CREATING SINGLE ANIMATION DEBUG PAGE ===")
    
    # Create test data
    trajectory = create_test_data()
    print(f"Test trajectory:")
    for t in trajectory.index.unique():
        subset = trajectory[trajectory.index == t]
        print(f"  Time {t}: x={list(subset.x)}")
    
    # Generate the interpolated sliding window animation
    print(f"\n=== GENERATING INTERPOLATED ANIMATION ===")
    try:
        fig = hyp.plot(trajectory, 
                      animate='window', 
                      mode='lines',
                      duration=2,     # Short duration for easier debugging
                      framerate=10)   # Moderate frame rate
        
        print(f"✅ Animation generated successfully!")
        print(f"✅ Total frames in animation: {len(fig.frames) if hasattr(fig, 'frames') else 'Unknown'}")
        
        # Create debug HTML
        html_content = create_debug_html(fig)
        
        # Save and open
        output_file = 'debug_interpolated_animation.html'
        with open(output_file, 'w') as f:
            f.write(html_content)
        
        print(f"✅ Debug page saved: {output_file}")
        
        # Open in browser
        webbrowser.open(f'file://{os.path.abspath(output_file)}')
        print(f"✅ Debug page opened in browser")
        
    except Exception as e:
        print(f"❌ Animation generation failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()