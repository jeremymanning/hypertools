#!/usr/bin/env python3
"""
Visual Verification using Matplotlib Conversion
Creates HTML page with matplotlib versions of Three.js figures for visual verification
"""

import numpy as np
import pandas as pd
import sys
import os
import matplotlib.pyplot as plt
import matplotlib
import io
import base64

# Use non-interactive backend
matplotlib.use('Agg')

# Add hypertools to path
sys.path.insert(0, '/Users/jmanning/hypertools')

import hypertools as hyp
from hypertools.core.threejs_backend import HyperToolsFigure

def create_test_figures():
    """Create a variety of test figures for visual verification"""
    
    figures = []
    
    # 1. Basic 2D scatter plot
    print("Creating 2D scatter plot...")
    np.random.seed(123)  # Force new random data
    data_2d_scatter = np.random.randn(50, 2) * 2
    fig1 = hyp.plot(data_2d_scatter, 'ro', markersize=8, alpha=0.7)
    figures.append(("2D Scatter Plot (red circles)", fig1, "Should show red circular points, not lines"))
    
    # 2. Basic 2D line plot  
    print("Creating 2D line plot...")
    t = np.linspace(0, 2*np.pi, 100)
    data_2d_line = np.column_stack([np.cos(t), np.sin(t)])
    fig2 = hyp.plot(data_2d_line, 'b-', linewidth=3)
    figures.append(("2D Line Plot (blue line)", fig2, "Should show smooth blue circle line"))
    
    # 3. 2D line + markers
    print("Creating 2D line with markers...")
    t = np.linspace(0, 4*np.pi, 50)
    data_spiral = np.column_stack([t * np.cos(t) / 10, t * np.sin(t) / 10])
    fig3 = hyp.plot(data_spiral, 'go-', linewidth=2, markersize=6)
    figures.append(("2D Spiral (green line + circles)", fig3, "Should show green spiral with both line and circle markers"))
    
    # 4. 3D scatter plot
    print("Creating 3D scatter plot...")
    np.random.seed(456)  # Force new random data
    data_3d_scatter = np.random.randn(40, 3)
    fig4 = hyp.plot(data_3d_scatter, 'mo', markersize=10, alpha=0.8)
    figures.append(("3D Scatter Plot (magenta circles)", fig4, "Should show magenta points in 3D space"))
    
    # 5. 3D line plot (helix)
    print("Creating 3D helix...")
    t = np.linspace(0, 6*np.pi, 120)
    data_3d_helix = np.column_stack([np.cos(t), np.sin(t), t/3])
    fig5 = hyp.plot(data_3d_helix, 'r-', linewidth=4)
    figures.append(("3D Helix (red line)", fig5, "Should show red helical/spiral line in 3D"))
    
    # 6. Multiple datasets
    print("Creating multiple datasets plot...")
    t = np.linspace(0, 4*np.pi, 80)
    data1 = np.column_stack([t, np.sin(t)])
    data2 = np.column_stack([t, np.cos(t)])
    data3 = np.column_stack([t, np.sin(t) * np.cos(t/2)])
    fig6 = hyp.plot([data1, data2, data3], ['r-', 'b--', 'go'], linewidth=[2, 3, 1])
    figures.append(("Multiple Datasets (sin, cos, sin*cos)", fig6, "Should show: red solid sin wave, blue dashed cos wave, green circles with sin*cos"))
    
    # 7. Dashed lines
    print("Creating dashed line...")
    x = np.linspace(0, 10, 50)
    y = np.sin(x)
    fig7 = hyp.plot(np.column_stack([x, y]), 'k--', linewidth=3)
    figures.append(("Dashed Line Style", fig7, "Should show black dashed sin wave"))
    
    # 8. Single point (should auto-convert to marker)
    print("Creating single point...")
    single_point = np.array([[3, 2]])
    fig8 = hyp.plot(single_point, 'b-', markersize=15)
    figures.append(("Single Point (auto-converted to marker)", fig8, "Should show single large blue circle (auto-converted from line to marker)"))
    
    # 9. Different marker styles
    print("Creating triangle markers...")
    np.random.seed(789)  # Force new random data
    data_markers = np.random.randn(20, 2)
    fig9 = hyp.plot(data_markers, 'r^', markersize=12, alpha=0.8)
    figures.append(("Triangle Markers", fig9, "Should show red triangle-shaped markers"))
    
    # 10. Test interpolation
    print("Creating interpolation test...")
    sparse_data = np.array([[0, 0], [1, 2], [3, 1], [5, 3], [7, 0]])
    fig10 = hyp.plot(sparse_data, 'g-', linewidth=3, interpolation_samples=100)
    figures.append(("Line Interpolation (5 points → 100)", fig10, "Should show smooth green curve through 5 control points"))
    
    return figures

def figure_to_base64(mpl_fig):
    """Convert matplotlib figure to base64 string for HTML embedding"""
    buf = io.BytesIO()
    mpl_fig.savefig(buf, format='png', dpi=150, bbox_inches='tight', 
                    facecolor='white', edgecolor='none')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(mpl_fig)
    return img_base64

def create_html_page(figures, output_path):
    """Create HTML page with matplotlib conversions of all test figures"""
    
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HyperTools Three.js Visual Verification (Matplotlib Preview)</title>
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
        .figure-images {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin: 20px 0;
        }}
        .image-section {{
            text-align: center;
        }}
        .image-section h4 {{
            margin: 10px 0;
            color: #555;
        }}
        .figure-img {{
            max-width: 100%;
            border: 1px solid #ddd;
            border-radius: 8px;
            background: white;
        }}
        .expected-behavior {{
            background: #e8f4fd;
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
            border-left: 4px solid #007acc;
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
        .note {{
            background: #fff3cd;
            border: 1px solid #ffc107;
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🎨 HyperTools Three.js Visual Verification</h1>
        <div class="note">
            <strong>📋 Testing Method:</strong> These are matplotlib conversions of the Three.js figures.<br>
            The Three.js versions should look similar but with better interactivity (3D rotation, etc.)
        </div>
        <p><strong>Date:</strong> {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>Total Figures:</strong> {len(figures)}</p>
    </div>
    
    <button class="save-results" onclick="saveResults()">💾 Save Test Results</button>
"""

    # Add each figure
    for i, (title, fig, expected) in enumerate(figures):
        
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
            Dimensionality: {fig.dimensionality}, Datasets: {fig.n_datasets}
            """
        
        # Create matplotlib version
        try:
            print(f"Converting figure {i+1}: {title}")
            mpl_fig = fig.to_matplotlib()
            img_base64 = figure_to_base64(mpl_fig)
            
            img_html = f'<img src="data:image/png;base64,{img_base64}" class="figure-img" alt="{title}">'
            conversion_status = "✅ Conversion successful"
            
        except Exception as e:
            img_html = f'''
            <div style="width: 400px; height: 300px; border: 1px solid #f00; background: #ffe6e6; display: flex; align-items: center; justify-content: center;">
                <div style="text-align: center; color: #d00;">
                    <h4>Conversion Error</h4>
                    <p>{str(e)}</p>
                </div>
            </div>
            '''
            conversion_status = f"❌ Conversion failed: {str(e)}"
        
        html_content += f"""
    <div class="figure-container" id="figure-{i}">
        <div class="figure-title">Figure {i+1}: {title}</div>
        
        <div class="figure-info">
            {dataset_info}<br>
            {style_info}<br>
            <strong>Conversion:</strong> {conversion_status}
        </div>
        
        <div class="expected-behavior">
            <strong>Expected Behavior:</strong> {expected}
        </div>
        
        <div class="figure-images">
            <div class="image-section">
                <h4>Matplotlib Conversion Preview</h4>
                {img_html}
                <p style="font-size: 12px; color: #666; margin-top: 10px;">
                    This shows how the Three.js figure converts to matplotlib
                </p>
            </div>
            <div class="image-section">
                <h4>Three.js Version</h4>
                <div style="width: 400px; height: 300px; border: 2px dashed #007acc; background: #f0f8ff; display: flex; align-items: center; justify-content: center; margin: 0 auto;">
                    <div style="text-align: center; color: #007acc;">
                        <h4>Interactive Three.js Plot</h4>
                        <p>Test in Jupyter notebook:</p>
                        <code>fig = hyp.plot(...)<br>fig.show()</code>
                        <p style="font-size: 12px; margin-top: 10px;">
                            Should look similar to matplotlib version<br>
                            but with 3D interactivity (if 3D)
                        </p>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="feedback-section">
            <p><strong>Does the matplotlib conversion look correct for this figure type?</strong></p>
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
            <textarea id="notes-{i}" placeholder="Notes about this figure (issues, suggestions, etc.)..." 
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
    """Create visual verification test page using matplotlib conversions"""
    print("🎨 CREATING VISUAL VERIFICATION TEST PAGE (MATPLOTLIB PREVIEW)")
    print("=" * 70)
    
    # Create test figures
    print("Creating test figures...")
    figures = create_test_figures()
    
    print(f"Created {len(figures)} test figures")
    
    # Create HTML page
    output_path = "/Users/jmanning/hypertools/matplotlib_visual_verification.html"
    html_path = create_html_page(figures, output_path)
    
    print("\n" + "=" * 70)
    print("📊 VISUAL VERIFICATION TEST READY")
    print(f"✅ Test page: {html_path}")
    print("\n📋 TESTING APPROACH:")
    print("   • Matplotlib conversions show how figures should look")
    print("   • Three.js versions should look similar with added interactivity")
    print("   • Focus on: colors, line styles, markers, 2D vs 3D")
    print("\n🔍 WHAT TO VERIFY:")
    print("   • Scatter plots = distinct points (not connected)")
    print("   • Line plots = smooth continuous lines")
    print("   • Colors match descriptions (red, blue, green, etc.)")
    print("   • Line styles: solid (-), dashed (--)")
    print("   • Markers: circles (o), triangles (^)")
    print("   • 3D plots show depth/perspective")
    print("   • Multiple datasets have different colors")
    print("   • Single points auto-convert to markers")
    print("   • Interpolation creates smooth curves")
    
    # Try to open in browser
    try:
        import webbrowser
        webbrowser.open(f'file://{html_path}')
        print(f"\n🌐 Opened in browser: {html_path}")
    except:
        print(f"\n📁 Please manually open: {html_path}")

if __name__ == "__main__":
    main()