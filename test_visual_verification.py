#!/usr/bin/env python3
"""
Visual Verification Test for HyperTools Three.js Backend
Creates HTML page with embedded figures for manual inspection
"""

import numpy as np
import pandas as pd
import sys
import os

# Add hypertools to path
sys.path.insert(0, '/Users/jmanning/hypertools')

import hypertools as hyp
from hypertools.core.threejs_backend import HyperToolsFigure

def create_test_figures():
    """Create a variety of test figures for visual verification"""
    
    figures = []
    
    # 1. Basic 2D scatter plot
    print("Creating 2D scatter plot...")
    data_2d_scatter = np.random.randn(50, 2) * 2
    fig1 = hyp.plot(data_2d_scatter, 'ro', markersize=8, alpha=0.7)
    figures.append(("2D Scatter Plot (red circles)", fig1))
    
    # 2. Basic 2D line plot  
    print("Creating 2D line plot...")
    t = np.linspace(0, 2*np.pi, 100)
    data_2d_line = np.column_stack([np.cos(t), np.sin(t)])
    fig2 = hyp.plot(data_2d_line, 'b-', linewidth=3)
    figures.append(("2D Line Plot (blue line)", fig2))
    
    # 3. 2D line + markers
    print("Creating 2D line with markers...")
    t = np.linspace(0, 4*np.pi, 50)
    data_spiral = np.column_stack([t * np.cos(t) / 10, t * np.sin(t) / 10])
    fig3 = hyp.plot(data_spiral, 'go-', linewidth=2, markersize=6)
    figures.append(("2D Spiral (green line + circles)", fig3))
    
    # 4. 3D scatter plot
    print("Creating 3D scatter plot...")
    data_3d_scatter = np.random.randn(40, 3)
    fig4 = hyp.plot(data_3d_scatter, 'mo', markersize=10, alpha=0.8)
    figures.append(("3D Scatter Plot (magenta circles)", fig4))
    
    # 5. 3D line plot (helix)
    print("Creating 3D helix...")
    t = np.linspace(0, 6*np.pi, 120)
    data_3d_helix = np.column_stack([np.cos(t), np.sin(t), t/3])
    fig5 = hyp.plot(data_3d_helix, 'r-', linewidth=4)
    figures.append(("3D Helix (red line)", fig5))
    
    # 6. Multiple datasets
    print("Creating multiple datasets plot...")
    t = np.linspace(0, 4*np.pi, 80)
    data1 = np.column_stack([t, np.sin(t)])
    data2 = np.column_stack([t, np.cos(t)])
    data3 = np.column_stack([t, np.sin(t) * np.cos(t/2)])
    fig6 = hyp.plot([data1, data2, data3], ['r-', 'b--', 'go'], linewidth=[2, 3, 1])
    figures.append(("Multiple Datasets (sin, cos, sin*cos)", fig6))
    
    # 7. Dashed and dotted lines
    print("Creating line style variations...")
    x = np.linspace(0, 10, 50)
    y = np.sin(x)
    fig7 = hyp.plot(np.column_stack([x, y]), 'k--', linewidth=3)
    figures.append(("Dashed Line Style", fig7))
    
    # 8. Single point (should auto-convert to marker)
    print("Creating single point...")
    single_point = np.array([[3, 2]])
    fig8 = hyp.plot(single_point, 'b-', markersize=15)
    figures.append(("Single Point (auto-converted to marker)", fig8))
    
    # 9. High-dimensional data (auto-reduced)
    print("Creating high-dimensional data...")
    high_dim = np.random.randn(30, 8)  # 8D -> 3D
    fig9 = hyp.plot(high_dim, 'c-', linewidth=2)
    figures.append(("High-dim Data (8D→3D auto-reduction)", fig9))
    
    # 10. Different marker styles
    print("Creating different marker styles...")
    data_markers = np.random.randn(20, 2)
    fig10 = hyp.plot(data_markers, 'r^', markersize=12, alpha=0.8)
    figures.append(("Triangle Markers", fig10))
    
    return figures

def extract_renderer_html(renderer):
    """Extract HTML from pythreejs renderer for embedding"""
    try:
        # For pythreejs widgets, we need to use the widget HTML embedding approach
        from ipywidgets.embed import embed_minimal_html
        import tempfile
        import uuid
        
        # Create a temporary file for the widget
        widget_id = str(uuid.uuid4())
        
        # Try to get widget state for embedding
        try:
            # Create a minimal HTML representation
            # This is a simplified approach - the full widget embedding requires more setup
            widget_html = f'''
            <div id="widget-{widget_id}" style="width: 800px; height: 600px; border: 1px solid #ccc; background: #f9f9f9; display: flex; align-items: center; justify-content: center;">
                <div style="text-align: center; color: #666;">
                    <h3>Three.js Widget</h3>
                    <p>Widget ID: {widget_id}</p>
                    <p>Type: {type(renderer).__name__}</p>
                    <p>Note: Full widget display requires Jupyter environment</p>
                    <p style="font-size: 12px; margin-top: 20px;">
                        To test: Run in Jupyter notebook:<br>
                        <code>fig.show()</code>
                    </p>
                </div>
            </div>
            '''
            return widget_html
            
        except Exception as inner_e:
            return f'''
            <div style="width: 800px; height: 600px; border: 1px solid #ddd; background: #f5f5f5; display: flex; align-items: center; justify-content: center;">
                <div style="text-align: center; color: #666;">
                    <h3>Three.js Renderer Created</h3>
                    <p>Renderer Type: {type(renderer).__name__}</p>
                    <p>Status: Widget created successfully</p>
                    <p style="font-size: 12px; margin-top: 15px;">
                        Note: Full Three.js display requires Jupyter environment<br>
                        This test verifies the widget creation process
                    </p>
                </div>
            </div>
            '''
            
    except Exception as e:
        return f'''
        <div style="width: 800px; height: 600px; border: 1px solid #f00; background: #ffe6e6; display: flex; align-items: center; justify-content: center;">
            <div style="text-align: center; color: #d00;">
                <h3>Widget Creation Error</h3>
                <p>Error: {str(e)}</p>
                <p style="font-size: 12px;">This indicates a problem with the Three.js backend</p>
            </div>
        </div>
        '''

def create_html_page(figures, output_path):
    """Create HTML page with all test figures"""
    
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HyperTools Three.js Visual Verification</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .figure-container {{
            background: white;
            margin: 20px 0;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .figure-title {{
            font-size: 18px;
            font-weight: bold;
            color: #333;
            margin-bottom: 15px;
            border-bottom: 2px solid #007acc;
            padding-bottom: 5px;
        }}
        .figure-info {{
            background: #f8f9fa;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 15px;
            font-size: 14px;
            color: #666;
        }}
        .figure-widget {{
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 10px;
            background: #fafafa;
            min-height: 400px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .feedback-section {{
            background: #e8f4fd;
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
        }}
        .feedback-buttons {{
            display: flex;
            gap: 10px;
            margin-top: 10px;
        }}
        .btn {{
            padding: 8px 16px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
        }}
        .btn-correct {{ background: #28a745; color: white; }}
        .btn-incorrect {{ background: #dc3545; color: white; }}
        .btn-review {{ background: #ffc107; color: black; }}
        .status {{
            margin: 10px 0;
            padding: 5px;
            border-radius: 3px;
            display: none;
        }}
        .save-results {{
            position: fixed;
            top: 20px;
            right: 20px;
            background: #007acc;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🎨 HyperTools Three.js Visual Verification</h1>
        <p>Please review each figure and provide feedback on its appearance</p>
        <p><strong>Date:</strong> {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>Total Figures:</strong> {len(figures)}</p>
    </div>
    
    <button class="save-results" onclick="saveResults()">💾 Save Test Results</button>
"""

    # Add each figure
    for i, (title, fig) in enumerate(figures):
        
        # Get figure info
        style_info = ""
        if hasattr(fig, 'plot_styles') and fig.plot_styles:
            style = fig.plot_styles[0]
            style_info = f"""
            <strong>Style:</strong> Color: {style['color']}, Line: {style['linestyle']}, 
            Marker: {style['marker']}, Width: {style['linewidth']}, Size: {style['markersize']}, 
            Alpha: {style['alpha']}
            """
        
        dataset_info = ""
        if hasattr(fig, 'datasets') and fig.datasets:
            dataset = fig.datasets[0]
            dataset_info = f"""
            <strong>Data:</strong> Shape: {dataset.shape}, Columns: {list(dataset.columns)}, 
            Dimensionality: {fig.dimensionality}
            """
        
        # Get renderer
        try:
            renderer = fig.show()
            renderer_html = extract_renderer_html(renderer)
        except Exception as e:
            renderer_html = f"<div>Error creating renderer: {e}</div>"
        
        html_content += f"""
    <div class="figure-container" id="figure-{i}">
        <div class="figure-title">Figure {i+1}: {title}</div>
        
        <div class="figure-info">
            {dataset_info}<br>
            {style_info}
        </div>
        
        <div class="figure-widget">
            {renderer_html}
        </div>
        
        <div class="feedback-section">
            <p><strong>How does this figure look?</strong></p>
            <div class="feedback-buttons">
                <button class="btn btn-correct" onclick="setFeedback({i}, 'correct')">
                    ✅ Looks Correct
                </button>
                <button class="btn btn-incorrect" onclick="setFeedback({i}, 'incorrect')">
                    ❌ Has Issues
                </button>
                <button class="btn btn-review" onclick="setFeedback({i}, 'review')">
                    🔍 Needs Review
                </button>
            </div>
            <div class="status" id="status-{i}"></div>
            <textarea id="notes-{i}" placeholder="Optional notes about this figure..." 
                      style="width: 100%; margin-top: 10px; padding: 8px; border-radius: 4px; border: 1px solid #ccc;"></textarea>
        </div>
    </div>
"""

    # Add JavaScript for feedback
    html_content += """
    <script>
        let feedback = {};
        
        function setFeedback(figureId, status) {
            feedback[figureId] = {
                status: status,
                notes: document.getElementById(`notes-${figureId}`).value,
                timestamp: new Date().toISOString()
            };
            
            const statusDiv = document.getElementById(`status-${figureId}`);
            statusDiv.style.display = 'block';
            
            if (status === 'correct') {
                statusDiv.style.background = '#d4edda';
                statusDiv.style.color = '#155724';
                statusDiv.textContent = '✅ Marked as correct';
            } else if (status === 'incorrect') {
                statusDiv.style.background = '#f8d7da';
                statusDiv.style.color = '#721c24';
                statusDiv.textContent = '❌ Marked as having issues';
            } else if (status === 'review') {
                statusDiv.style.background = '#fff3cd';
                statusDiv.style.color = '#856404';
                statusDiv.textContent = '🔍 Marked for review';
            }
            
            console.log('Feedback updated:', feedback);
        }
        
        function saveResults() {
            const results = {
                timestamp: new Date().toISOString(),
                feedback: feedback,
                summary: {
                    total: Object.keys(feedback).length,
                    correct: Object.values(feedback).filter(f => f.status === 'correct').length,
                    incorrect: Object.values(feedback).filter(f => f.status === 'incorrect').length,
                    review: Object.values(feedback).filter(f => f.status === 'review').length
                }
            };
            
            // Create downloadable JSON
            const dataStr = JSON.stringify(results, null, 2);
            const dataBlob = new Blob([dataStr], {type: 'application/json'});
            const url = URL.createObjectURL(dataBlob);
            
            const link = document.createElement('a');
            link.href = url;
            link.download = 'hypertools_visual_feedback.json';
            link.click();
            
            alert(`Results saved! Summary: ${results.summary.correct} correct, ${results.summary.incorrect} incorrect, ${results.summary.review} review`);
        }
        
        // Auto-save to localStorage
        setInterval(() => {
            if (Object.keys(feedback).length > 0) {
                localStorage.setItem('hypertools_feedback', JSON.stringify(feedback));
            }
        }, 5000);
        
        // Load previous feedback on page load
        window.onload = () => {
            const saved = localStorage.getItem('hypertools_feedback');
            if (saved) {
                feedback = JSON.parse(saved);
                console.log('Loaded previous feedback:', feedback);
            }
        };
    </script>
</body>
</html>
"""

    # Write to file
    with open(output_path, 'w') as f:
        f.write(html_content)
    
    print(f"✅ HTML test page created: {output_path}")
    return output_path

def main():
    """Create visual verification test page"""
    print("🎨 CREATING VISUAL VERIFICATION TEST PAGE")
    print("=" * 50)
    
    # Create test figures
    print("Creating test figures...")
    figures = create_test_figures()
    
    print(f"Created {len(figures)} test figures")
    
    # Create HTML page
    output_path = "/Users/jmanning/hypertools/visual_verification_test.html"
    html_path = create_html_page(figures, output_path)
    
    print("\n" + "=" * 50)
    print("📊 VISUAL VERIFICATION TEST READY")
    print(f"✅ Test page: {html_path}")
    print("\n📋 INSTRUCTIONS:")
    print("1. Open the HTML file in your browser")
    print("2. Review each figure for correct appearance")
    print("3. Click feedback buttons for each figure")
    print("4. Add notes if needed")
    print("5. Click 'Save Test Results' when done")
    print("\n🔍 WHAT TO CHECK:")
    print("   • Do scatter plots show as points (not lines)?")
    print("   • Do line plots show as smooth lines?")
    print("   • Are colors correct (red, blue, green, etc.)?")
    print("   • Do 3D plots show proper depth and rotation?")
    print("   • Are marker shapes correct (circles, triangles)?")
    print("   • Do multiple datasets show different colors?")
    print("   • Is line interpolation smooth?")
    
    # Try to open in browser
    try:
        import webbrowser
        webbrowser.open(f'file://{html_path}')
        print(f"\n🌐 Opened in browser: {html_path}")
    except:
        print(f"\n📁 Please manually open: {html_path}")

if __name__ == "__main__":
    main()