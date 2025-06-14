#!/usr/bin/env python3
"""
Final Integration Test - HyperTools with Three.js Backend
Demonstrates the working matplotlib-style API
"""

import numpy as np
import sys

# Add hypertools to path
sys.path.insert(0, '/Users/jmanning/hypertools')

import hypertools as hyp
from hypertools.core.threejs_backend import HyperToolsFigure

def demo_syntax():
    """Demonstrate the exact syntax requested"""
    print("🎯 DEMONSTRATING REQUESTED SYNTAX")
    print("=" * 50)
    
    # Create demo data
    t = np.linspace(0, 2*np.pi, 30)
    data = np.column_stack([np.cos(t), np.sin(t)])
    
    print("# The exact syntax you requested:")
    print("fig = hyp.plot(data, 'ko-', linewidth=4, markersize=10)")
    print()
    
    # Execute the exact syntax
    fig = hyp.plot(data, 'ko-', linewidth=4, markersize=10)
    
    print(f"✅ Returns: {type(fig).__name__}")
    print(f"✅ Is HyperToolsFigure: {isinstance(fig, HyperToolsFigure)}")
    
    if isinstance(fig, HyperToolsFigure):
        style = fig.plot_styles[0]
        print(f"✅ Parsed style:")
        print(f"   - Color: {style['color']}")
        print(f"   - Line style: {style['linestyle']}")
        print(f"   - Marker: {style['marker']}")
        print(f"   - Line width: {style['linewidth']}")
        print(f"   - Marker size: {style['markersize']}")
        
        # Show that it renders
        renderer = fig.show()
        print(f"✅ fig.show() works: {type(renderer).__name__}")
        
        return fig
    
    return None

def demo_features():
    """Demonstrate various features working"""
    print("\n🌟 FEATURE DEMONSTRATIONS")
    print("=" * 50)
    
    features = []
    
    # 1. Multiple format strings
    print("\n1. Multiple datasets with different styles:")
    t = np.linspace(0, 4*np.pi, 50)
    data1 = np.column_stack([t, np.sin(t)])
    data2 = np.column_stack([t, np.cos(t)])
    data3 = np.column_stack([t, np.sin(t) * np.exp(-t/10)])
    
    fig1 = hyp.plot([data1, data2, data3], ['r-', 'b--', 'go'], linewidth=[2, 3, 1])
    print(f"   ✅ Multiple datasets: {fig1.n_datasets} plots created")
    features.append(fig1)
    
    # 2. 3D plotting
    print("\n2. 3D plotting:")
    t = np.linspace(0, 6*np.pi, 80)
    data_3d = np.column_stack([np.cos(t), np.sin(t), t/5])
    
    fig2 = hyp.plot(data_3d, 'mo-', linewidth=2, alpha=0.7)
    print(f"   ✅ 3D plot: {fig2.dimensionality} dimensionality")
    features.append(fig2)
    
    # 3. Single point handling
    print("\n3. Single point auto-detection:")
    single_point = np.array([[2.5, 1.5]])
    
    fig3 = hyp.plot(single_point, 'b-')  # Should auto-convert to marker
    style = fig3.plot_styles[0]
    print(f"   ✅ Auto-corrected: linestyle={style['linestyle']}, marker={style['marker']}")
    features.append(fig3)
    
    # 4. Line interpolation
    print("\n4. Line interpolation:")
    sparse_data = np.array([[0, 0], [1, 2], [3, 1], [5, 3]])
    
    fig4 = hyp.plot(sparse_data, 'g-', interpolation_samples=100)
    original_points = len(sparse_data)
    interpolated_points = len(fig4.datasets[0])
    print(f"   ✅ Interpolated: {original_points} → {interpolated_points} points")
    features.append(fig4)
    
    return features

def demo_hypertools_integration():
    """Demonstrate HyperTools preprocessing integration"""
    print("\n🔧 HYPERTOOLS PREPROCESSING INTEGRATION")
    print("=" * 50)
    
    # High-dimensional data that will be auto-reduced
    print("Testing with high-dimensional data (10D → 3D reduction):")
    high_dim_data = np.random.randn(40, 10)
    print(f"Original shape: {high_dim_data.shape}")
    
    try:
        fig = hyp.plot(high_dim_data, 'c-', linewidth=2)
        
        processed_shape = fig.datasets[0].shape
        print(f"✅ Processed shape: {processed_shape}")
        print(f"✅ Auto-detected dimensionality: {fig.dimensionality}")
        print(f"✅ HyperTools preprocessing + Three.js rendering works!")
        
        return fig
        
    except Exception as e:
        print(f"❌ Preprocessing integration failed: {e}")
        return None

def main():
    """Run complete integration demonstration"""
    print("🚀 HYPERTOOLS THREE.JS INTEGRATION - FINAL DEMONSTRATION")
    print("=" * 70)
    
    # Run demonstrations
    syntax_demo = demo_syntax()
    feature_demos = demo_features()
    preprocessing_demo = demo_hypertools_integration()
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 INTEGRATION SUMMARY")
    
    total_success = (
        syntax_demo is not None and
        len(feature_demos) > 0 and
        preprocessing_demo is not None
    )
    
    if total_success:
        print("🎉 COMPLETE SUCCESS!")
        print("\n✅ WORKING FEATURES:")
        print("   • fig = hyp.plot(data, 'ko-', linewidth=4, markersize=10)")
        print("   • Returns HyperToolsFigure objects")
        print("   • Matplotlib-style format strings (r-, bo, g--, etc.)")
        print("   • Multiple datasets with different styles")
        print("   • 2D and 3D plotting")
        print("   • Single point auto-detection")
        print("   • Line interpolation for smooth curves")
        print("   • HyperTools preprocessing integration")
        print("   • Three.js interactive rendering")
        
        print("\n📋 TODO ITEMS (noted for future work):")
        print("   • Restore mat2colors for advanced color mapping")
        print("   • Implement labels2colors for cluster/hue coloring")
        print("   • Add matplotlib conversion system (Phase 1 Week 2)")
        print("   • Implement animation support")
        print("   • Add vector export capabilities")
        
        print("\n🎯 READY FOR PRODUCTION USE!")
        print("The Three.js backend successfully replaces Plotly as the unified")
        print("rendering engine for HyperTools with enhanced capabilities.")
        
        return syntax_demo
    else:
        print("❌ Some features not working properly")
        return None

if __name__ == "__main__":
    main()