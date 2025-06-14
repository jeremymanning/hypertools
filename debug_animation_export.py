import numpy as np
import pandas as pd
import hypertools as hyp
import os

# Create test animation data
np.random.seed(42)
n_timepoints = 10
anim_data = []

for i in range(n_timepoints):
    x = np.random.randn(20) + np.sin(i/2) * 1
    y = np.random.randn(20) + np.cos(i/2) * 1  
    z = np.random.randn(20) + i * 0.2
    
    df = pd.DataFrame({'x': x, 'y': y, 'z': z}, index=[i] * 20)
    anim_data.append(df)

data_timeseries = pd.concat(anim_data)
print(f"Animation data shape: {data_timeseries.shape}")

# Test animation creation
print("\nTesting animation creation...")
try:
    fig = hyp.plot(data_timeseries, animate='window')
    print("✓ Animation created successfully")
    
    # Check animation properties
    if hasattr(fig, 'frames') and fig.frames:
        print(f"Number of frames: {len(fig.frames)}")
        print(f"Frame duration: {fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration']}ms")
    
    # Test saving animation as HTML
    html_path = "test_animation.html"
    try:
        fig.write_html(html_path)
        print(f"✓ Animation saved as HTML: {html_path}")
        if os.path.exists(html_path):
            print(f"  File size: {os.path.getsize(html_path)} bytes")
    except Exception as e:
        print(f"✗ HTML export failed: {e}")
    
    # Test animation with save_path parameter
    try:
        save_path = "test_animation_save.html"
        fig2 = hyp.plot(data_timeseries, animate='precog', save_path=save_path)
        print(f"✓ Animation with save_path parameter: {save_path}")
        if os.path.exists(save_path):
            print(f"  File size: {os.path.getsize(save_path)} bytes")
    except Exception as e:
        print(f"✗ Animation save_path failed: {e}")
        
except Exception as e:
    print(f"✗ Animation creation failed: {e}")
    import traceback
    traceback.print_exc()

# Test different animation styles
styles = ['window', 'precog']
for style in styles:
    print(f"\nTesting {style} animation export...")
    try:
        fig = hyp.plot(data_timeseries, animate=style)
        filename = f"test_animation_{style}.html"
        fig.write_html(filename)
        print(f"✓ {style} animation exported: {filename}")
        if os.path.exists(filename):
            print(f"  File size: {os.path.getsize(filename)} bytes")
    except Exception as e:
        print(f"✗ {style} animation export failed: {e}")

print("\nAnimation test complete!")
print("Files created:")
for filename in ["test_animation.html", "test_animation_save.html", "test_animation_window.html", "test_animation_precog.html"]:
    if os.path.exists(filename):
        print(f"  {filename} ({os.path.getsize(filename)} bytes)")