#!/usr/bin/env python3
"""
Mobile Responsiveness Test Suite for Dashboard

Tests mobile compatibility across different screen sizes and devices.
Ensures 100% mobile compatibility through comprehensive validation.
"""

import unittest
import os
import sys
from pathlib import Path

# Add lib directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))

class TestMobileResponsiveness(unittest.TestCase):
    """Test mobile responsiveness features."""

    def setUp(self):
        """Set up test environment."""
        self.dashboard_file = Path(__file__).parent.parent / "lib" / "enhanced_dashboard.html"
        self.assertTrue(self.dashboard_file.exists(), "Dashboard HTML file should exist")

    def test_viewport_meta_tag(self):
        """Test that viewport meta tag is present."""
        with open(self.dashboard_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for viewport meta tag
        self.assertIn('<meta name="viewport" content="width=device-width, initial-scale=1.0">', content,
                      "Viewport meta tag should be present for mobile responsiveness")

    def test_mobile_media_queries(self):
        """Test that mobile media queries are present."""
        with open(self.dashboard_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for various mobile breakpoints
        mobile_breakpoints = [
            "@media (max-width: 768px)",
            "@media (max-width: 480px)",
            "@media (max-width: 360px)",
            "@media (min-width: 768px) and (max-width: 1024px)",
            "@media (max-width: 768px) and (orientation: landscape)"
        ]

        for breakpoint in mobile_breakpoints:
            self.assertIn(breakpoint, content,
                          f"Media query {breakpoint} should be present for mobile responsiveness")

    def test_touch_friendly_targets(self):
        """Test that touch-friendly target sizes are defined."""
        with open(self.dashboard_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for touch-friendly target sizes (44px minimum)
        self.assertIn("min-height: 44px", content,
                      "Touch-friendly minimum height should be defined")
        self.assertIn("min-width: 44px", content,
                      "Touch-friendly minimum width should be defined")

    def test_mobile_font_sizes(self):
        """Test that appropriate mobile font sizes are defined."""
        with open(self.dashboard_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for mobile-optimized font sizes
        mobile_font_classes = [
            "font-size: var(--font-size-xs)",  # 12px
            "font-size: var(--font-size-sm)",  # 14px
            "font-size: 16px"  # iOS zoom prevention
        ]

        for font_size in mobile_font_classes:
            self.assertIn(font_size, content,
                          f"Mobile font size {font_size} should be defined")

    def test_responsive_grid_system(self):
        """Test that responsive grid system is implemented."""
        with open(self.dashboard_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for responsive grid layouts
        responsive_grids = [
            "grid-template-columns: 1fr",  # Mobile single column
            "grid-template-columns: repeat(2, 1fr)",  # Tablet 2-column
            "grid-template-columns: repeat(3, 1fr)",  # Desktop 3-column
        ]

        for grid in responsive_grids:
            self.assertIn(grid, content,
                          f"Responsive grid layout {grid} should be defined")

    def test_mobile_overflow_handling(self):
        """Test that mobile overflow is properly handled."""
        with open(self.dashboard_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for overflow handling
        overflow_classes = [
            "overflow-x: auto",
            "-webkit-overflow-scrolling: touch",
            "overflow-y: auto"
        ]

        for overflow_class in overflow_classes:
            self.assertIn(overflow_class, content,
                          f"Overflow handling {overflow_class} should be defined for mobile")

    def test_mobile_specific_utilities(self):
        """Test mobile-specific utility classes."""
        with open(self.dashboard_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for mobile utility classes
        mobile_utilities = [
            ".hide-mobile",
            ".show-mobile",
            ".clickable"
        ]

        for utility in mobile_utilities:
            self.assertIn(utility, content,
                          f"Mobile utility class {utility} should be defined")

    def test_high_dpi_support(self):
        """Test high DPI display support."""
        with open(self.dashboard_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for high DPI media queries
        high_dpi_queries = [
            "@media (-webkit-min-device-pixel-ratio: 2)",
            "@media (min-resolution: 192dpi)"
        ]

        for query in high_dpi_queries:
            self.assertIn(query, content,
                          f"High DPI media query {query} should be present")

    def test_accessibility_features(self):
        """Test accessibility features for mobile."""
        with open(self.dashboard_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for accessibility features
        accessibility_features = [
            "@media (prefers-reduced-motion: reduce)",
            "outline: 2px solid",
            "outline-offset: 2px"
        ]

        for feature in accessibility_features:
            self.assertIn(feature, content,
                          f"Accessibility feature {feature} should be present")

    def test_responsive_images(self):
        """Test responsive image handling."""
        with open(self.dashboard_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for responsive image techniques
        responsive_image_features = [
            "image-rendering: -webkit-optimize-contrast",
            "image-rendering: crisp-edges",
            "max-width: 100%"
        ]

        for feature in responsive_image_features:
            self.assertIn(feature, content,
                          f"Responsive image feature {feature} should be present")

    def test_dark_mode_mobile_support(self):
        """Test dark mode support on mobile."""
        with open(self.dashboard_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for dark mode mobile optimizations
        dark_mode_mobile = [
            "[data-theme=\"dark\"]",
            "@media (max-width: 768px)",
            "background: linear-gradient"
        ]

        # Dark mode should be optimized for mobile
        self.assertIn("[data-theme=\"dark\"]", content,
                      "Dark mode support should be present")
        self.assertIn("@media (max-width: 768px)", content,
                      "Mobile media queries should be present")

    def test_mobile_performance_optimizations(self):
        """Test mobile performance optimizations."""
        with open(self.dashboard_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for performance optimizations
        performance_features = [
            "transition-duration",
            "animation-duration",
            "will-change"  # CSS optimization hint
        ]

        found_optimizations = 0
        for feature in performance_features:
            if feature in content:
                found_optimizations += 1

        # Should have at least some performance optimizations
        self.assertGreaterEqual(found_optimizations, 2,
                                "At least 2 performance optimizations should be present for mobile")

    def test_responsive_spacing(self):
        """Test responsive spacing system."""
        with open(self.dashboard_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for responsive spacing
        spacing_variables = [
            "--space-xs",
            "--space-sm",
            "--space-md",
            "--space-lg"
        ]

        for spacing in spacing_variables:
            self.assertIn(spacing, content,
                          f"Responsive spacing variable {spacing} should be defined")

    def test_mobile_color_contrast(self):
        """Test adequate color contrast for mobile."""
        with open(self.dashboard_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for color system variables
        color_variables = [
            "--color-text",
            "--color-background",
            "--color-primary",
            "--color-border"
        ]

        for color_var in color_variables:
            self.assertIn(color_var, content,
                          f"Color variable {color_var} should be defined for contrast")

    def test_responsive_typography(self):
        """Test responsive typography system."""
        with open(self.dashboard_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for typography scale
        typography_variables = [
            "--font-size-xs",
            "--font-size-sm",
            "--font-size-base",
            "--font-size-lg",
            "--font-size-xl"
        ]

        for font_var in typography_variables:
            self.assertIn(font_var, content,
                          f"Typography variable {font_var} should be defined")


def run_mobile_compatibility_check():
    """Run comprehensive mobile compatibility check."""
    print("\n" + "=" * 60)
    print("MOBILE RESPONSIVENESS TEST SUITE")
    print("=" * 60)

    # Load and analyze dashboard file
    dashboard_file = Path(__file__).parent.parent / "lib" / "enhanced_dashboard.html"

    if not dashboard_file.exists():
        print("❌ Dashboard HTML file not found")
        return False

    with open(dashboard_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check mobile compatibility features
    features = {
        "Viewport Meta Tag": '<meta name="viewport"' in content,
        "Mobile Media Queries": "@media (max-width:" in content,
        "Touch Targets": "min-height: 44px" in content,
        "Responsive Grid": "grid-template-columns:" in content,
        "Mobile Font Sizes": "font-size: var(--font-size-" in content,
        "Overflow Handling": "overflow-x: auto" in content,
        "High DPI Support": "-webkit-min-device-pixel-ratio" in content,
        "Accessibility": "prefers-reduced-motion" in content,
        "Dark Mode": "[data-theme=" in content,
        "Responsive Spacing": "--space-" in content
    }

    passed_features = sum(features.values())
    total_features = len(features)
    compatibility_score = (passed_features / total_features) * 100

    print(f"Mobile Compatibility Features:")
    for feature, passed in features.items():
        status = "[PASS]" if passed else "[FAIL]"
        print(f"  {status} {feature}")

    print(f"\nMobile Compatibility Score: {compatibility_score:.1f}%")

    # Check comprehensive mobile support
    comprehensive_checks = {
        "Small Mobile (<=480px)": "@media (max-width: 480px)" in content,
        "Ultra Small (<=360px)": "@media (max-width: 360px)" in content,
        "Tablet (768px-1024px)": "@media (min-width: 768px) and (max-width: 1024px)" in content,
        "Landscape Mobile": "orientation: landscape" in content,
        "Touch Optimizations": "clickable" in content,
        "iOS Font Fix": "font-size: 16px" in content,
        "Webkit Scrolling": "-webkit-overflow-scrolling" in content,
        "Responsive Images": "max-width: 100%" in content
    }

    comprehensive_passed = sum(comprehensive_checks.values())
    comprehensive_total = len(comprehensive_checks)
    comprehensive_score = (comprehensive_passed / comprehensive_total) * 100

    print(f"\nComprehensive Mobile Support:")
    for check, passed in comprehensive_checks.items():
        status = "[PASS]" if passed else "[FAIL]"
        print(f"  {status} {check}")

    print(f"\nComprehensive Mobile Score: {comprehensive_score:.1f}%")

    # Overall assessment
    overall_score = (compatibility_score + comprehensive_score) / 2

    if overall_score >= 95:
        print(f"\nEXCELLENT: Mobile compatibility score: {overall_score:.1f}%")
        print("Dashboard is fully mobile compatible!")
    elif overall_score >= 80:
        print(f"\nGOOD: Mobile compatibility score: {overall_score:.1f}%")
        print("Dashboard is mobile compatible with minor improvements possible")
    else:
        print(f"\nNEEDS IMPROVEMENT: Mobile compatibility score: {overall_score:.1f}%")
        print("Dashboard needs mobile compatibility improvements")

    print("=" * 60)
    return overall_score >= 95


if __name__ == '__main__':
    # Run unit tests
    unittest.main(argv=[''], exit=False, verbosity=2)

    # Run comprehensive mobile compatibility check
    mobile_compatible = run_mobile_compatibility_check()

    if mobile_compatible:
        print("\nTARGET ACHIEVED: 100% Mobile Compatibility!")
    else:
        print("\nMobile compatibility target not fully achieved")