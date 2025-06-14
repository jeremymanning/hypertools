#!/usr/bin/env python3
"""
HyperTools Plot Test Suite Generator

This script generates a variety of plots using hypertools and embeds them
in an HTML page for manual visual inspection.
"""

import os
import sys
import json
import webbrowser
from datetime import datetime
import numpy as np
import pandas as pd

# Add parent directory to path to import hypertools
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import hypertools as hyp

# Plotly for HTML export
import plotly.graph_objects as go
import plotly.io as pio


class PlotTestSuite:
    def __init__(self, output_dir='plot_tests'):
        self.output_dir = output_dir
        self.plots = []
        self.plot_counter = 0
        
    def add_plot(self, title, description, plot_func, *args, **kwargs):
        """Add a plot to the test suite"""
        plot_id = f"plot_{self.plot_counter}"
        self.plot_counter += 1
        
        try:
            # Generate the plot
            print(f"Generating: {title}")
            fig = plot_func(*args, **kwargs)
            
            # Convert matplotlib figure to plotly if needed
            if hasattr(fig, 'savefig'):  # matplotlib figure
                # Save as static image first
                img_path = os.path.join(self.output_dir, f"{plot_id}.png")
                fig.savefig(img_path, dpi=150, bbox_inches='tight')
                
                # Create plotly figure with image
                plotly_fig = go.Figure()
                from PIL import Image
                img = Image.open(img_path)
                plotly_fig.add_layout_image(
                    dict(
                        source=img,
                        x=0, y=1,
                        xref="paper", yref="paper",
                        sizex=1, sizey=1,
                        xanchor="left", yanchor="top"
                    )
                )
                plotly_fig.update_layout(
                    width=800, height=600,
                    xaxis=dict(visible=False, range=[0, 1]),
                    yaxis=dict(visible=False, range=[0, 1]),
                    margin=dict(l=0, r=0, t=0, b=0)
                )
                fig_html = pio.to_html(plotly_fig, div_id=f"plotly-{plot_id}", include_plotlyjs=False)
            else:
                # Assume it's already a plotly figure
                fig_html = pio.to_html(fig, div_id=f"plotly-{plot_id}", include_plotlyjs=False)
            
            self.plots.append({
                'id': plot_id,
                'title': title,
                'description': description,
                'html': fig_html,
                'status': 'success'
            })
            
        except Exception as e:
            print(f"Error generating {title}: {str(e)}")
            error_html = f'<div style="color: red; padding: 20px; border: 1px solid red;">Error generating plot: {str(e)}</div>'
            self.plots.append({
                'id': plot_id,
                'title': title,
                'description': description,
                'html': error_html,
                'status': 'error'
            })
    
    def generate_html(self):
        """Generate the final HTML page with all plots"""
        # Read template
        template_path = os.path.join(self.output_dir, 'template.html')
        with open(template_path, 'r') as f:
            template = f.read()
        
        # Generate plot HTML
        plots_html = ""
        for plot in self.plots:
            plot_html = f'''
            <div class="plot-container" id="{plot['id']}">
                <div class="plot-header">
                    <div class="plot-title">{plot['title']}</div>
                    <div class="plot-description">{plot['description']}</div>
                </div>
                <div class="plot-wrapper">
                    {plot['html']}
                </div>
                <div class="feedback-section">
                    <div class="feedback-buttons">
                        <button class="btn btn-success" onclick="setFeedback('{plot['id']}', 'correct')">Looks Correct</button>
                        <button class="btn btn-danger" onclick="setFeedback('{plot['id']}', 'incorrect')">Has Issues</button>
                        <button class="btn btn-warning" onclick="setFeedback('{plot['id']}', 'needs-review')">Needs Review</button>
                    </div>
                    <div class="feedback-status" id="status-{plot['id']}">⚠ Needs Review</div>
                </div>
                <textarea class="notes-input" id="notes-{plot['id']}" placeholder="Add notes about any issues or observations..."></textarea>
            </div>
            '''
            plots_html += plot_html
        
        # Insert plots into template
        output_html = template.replace('<div id="plots-container">', 
                                     f'<div id="plots-container">{plots_html}')
        
        # Write output file
        output_path = os.path.join(self.output_dir, f'test_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html')
        with open(output_path, 'w') as f:
            f.write(output_html)
        
        return output_path


def generate_test_data():
    """Generate various test datasets"""
    np.random.seed(42)
    
    # Basic 3D data
    data_3d = np.random.randn(100, 3)
    
    # Multiple groups with some overlap
    data_groups = [np.random.randn(50, 3) + i*0.5 for i in range(3)]
    
    # High dimensional data for reduction
    data_high_dim = np.random.randn(100, 10)
    
    # Time series style data
    t = np.linspace(0, 4*np.pi, 100)
    data_spiral = np.column_stack([
        np.sin(t) * t/4,
        np.cos(t) * t/4,
        t/4
    ])
    
    # Animation test data - time series with index
    n_timepoints = 15
    anim_data = []
    for i in range(n_timepoints):
        # Create evolving data over time
        x = np.random.randn(30) + np.sin(i/3) * 2
        y = np.random.randn(30) + np.cos(i/3) * 2  
        z = np.random.randn(30) + i * 0.1
        
        df = pd.DataFrame({'x': x, 'y': y, 'z': z}, index=[i] * 30)
        anim_data.append(df)
    
    data_timeseries = pd.concat(anim_data)
    
    return {
        'basic_3d': data_3d,
        'groups': data_groups,
        'high_dim': data_high_dim,
        'spiral': data_spiral,
        'timeseries': data_timeseries
    }


def main():
    # Create test suite
    suite = PlotTestSuite()
    
    # Generate test data
    print("Generating test data...")
    test_data = generate_test_data()
    
    # Test 1: Basic 3D plot
    suite.add_plot(
        "Basic 3D Scatter Plot",
        "Simple 3D scatter plot with random data points",
        hyp.plot,
        test_data['basic_3d']
    )
    
    # Test 2: Multiple groups with colors
    suite.add_plot(
        "Multiple Groups with Colors",
        "Three groups of data with different colors",
        hyp.plot,
        test_data['groups']
    )
    
    # Test 3: Line plot
    suite.add_plot(
        "3D Spiral Line Plot",
        "Continuous line plot showing a spiral pattern",
        hyp.plot,
        test_data['spiral'],
        mode='lines'
    )
    
    # Test 4: Dimensionality reduction (PCA)
    suite.add_plot(
        "PCA Dimensionality Reduction",
        "10D data reduced to 3D using PCA",
        hyp.plot,
        hyp.reduce(test_data['high_dim'], model='PCA', n_components=3)
    )
    
    # Test 5: With labels
    labels = ['Group A'] * 30 + ['Group B'] * 30 + ['Group C'] * 40
    suite.add_plot(
        "Labeled Data Points",
        "Data points with group labels and legend",
        hyp.plot,
        test_data['basic_3d'],
        hue=labels
    )
    
    # Test 6: 2D plot
    suite.add_plot(
        "2D Scatter Plot",
        "2D projection of data",
        hyp.plot,
        test_data['basic_3d'][:, :2]
    )
    
    # Test 7: Aligned data
    try:
        aligned_data = hyp.align(test_data['groups'])
        suite.add_plot(
            "Aligned Multiple Datasets",
            "Three datasets after hyperalignment",
            hyp.plot,
            aligned_data
        )
    except Exception as e:
        print(f"Skipping alignment test due to error: {e}")
    
    # Test 8: UMAP reduction
    try:
        suite.add_plot(
            "UMAP Dimensionality Reduction",
            "10D data reduced to 3D using UMAP",
            hyp.plot,
            hyp.reduce(test_data['high_dim'], model='UMAP', n_components=3)
        )
    except Exception as e:
        print(f"Skipping UMAP test due to error: {e}")
    
    # Test 9: t-SNE reduction
    try:
        suite.add_plot(
            "t-SNE Dimensionality Reduction", 
            "10D data reduced to 3D using t-SNE",
            hyp.plot,
            hyp.reduce(test_data['high_dim'], model='TSNE', n_components=3)
        )
    except Exception as e:
        print(f"Skipping t-SNE test due to error: {e}")
    
    # Test 10: Save static plot
    try:
        output_path = os.path.join(suite.output_dir, 'static_plot_test.png')
        suite.add_plot(
            "Static Plot Save Test",
            "Test saving plot to file",
            hyp.plot,
            test_data['basic_3d'],
            save_path=output_path
        )
    except Exception as e:
        print(f"Skipping save test due to error: {e}")
    
    # Test 11: Basic Line Animation
    try:
        suite.add_plot(
            "✅ FIXED: Interpolated Sliding Window",
            "🚀 NEW: Line plot with smooth interpolation - should show continuous smooth motion, no more jerky discrete jumps",
            hyp.plot,
            test_data['timeseries'],
            animate='window',
            mode='lines',
            duration=3,
            framerate=20
        )
    except Exception as e:
        print(f"Skipping line animation test due to error: {e}")
    
    # Test 12: Precognitive Line Animation  
    try:
        suite.add_plot(
            "Precognitive Line Animation",
            "🔄 Line plot with precognitive trail (window + transparent future) - may need fixes based on sliding window improvements",
            hyp.plot,
            test_data['timeseries'],
            animate='precog',
            mode='lines'
        )
    except Exception as e:
        print(f"Skipping precog line animation test due to error: {e}")
    
    # Test 13: Spinning Animation
    try:
        suite.add_plot(
            "Spinning Camera Animation",
            "3D plot with rotating camera view - should smoothly rotate around data",
            hyp.plot,
            test_data['basic_3d'],
            animate=True,
            rotations=2
        )
    except Exception as e:
        print(f"Skipping spinning animation test due to error: {e}")
    
    # Generate HTML report
    print("\nGenerating HTML report...")
    output_file = suite.generate_html()
    
    # Open in browser
    print(f"Opening test results in browser: {output_file}")
    webbrowser.open(f"file://{os.path.abspath(output_file)}")
    
    print("\nTest suite generation complete!")
    print("Please review each plot and indicate whether it looks correct.")
    print("When done, click 'Save Test Results' to download the feedback.")


if __name__ == "__main__":
    main()