#!/usr/bin/env python3
"""
Simple launcher script for Sprint Capacity Analysis

This script provides an easy way to run the capacity analysis
without command line arguments.

Usage:
    python run_capacity_analysis.py

Author: Sprint Capacity Automation System
Date: 2025-09-09
"""

import os
import sys
from sprint_capacity_app import SprintCapacityApp

def main():
    """Main function to run capacity analysis"""
    print("🚀 Sprint Capacity Analysis Tool")
    print("=" * 40)
    
    try:
        # Check if Excel file exists
        if not os.path.exists("CapacityUpdate.xlsx"):
            print("❌ Error: CapacityUpdate.xlsx file not found!")
            print("Please ensure the Excel file is in the same directory as this script.")
            input("Press Enter to exit...")
            return 1
        
        # Initialize and run the application
        print("📊 Initializing capacity analysis...")
        app = SprintCapacityApp()
        
        print("📈 Running capacity analysis...")
        success = app.run_capacity_analysis()
        
        if success:
            print("\n✅ Analysis completed successfully!")
            print("\n📋 Reports have been generated:")
            
            # List generated files
            files = [f for f in os.listdir('.') if f.startswith('sprint_capacity_report_')]
            for file in sorted(files)[-2:]:  # Show last 2 files (txt and html)
                print(f"   📄 {file}")
            
            print("\n💡 Tips:")
            print("   • Share the text report with your Scrum Master")
            print("   • Open the HTML report in a web browser for better viewing")
            print("   • Configure email settings in config.json for automatic delivery")
            
        else:
            print("❌ Analysis failed. Please check the logs for details.")
            return 1
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Analysis cancelled by user.")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return 1
    
    print("\n" + "=" * 40)
    input("Press Enter to exit...")
    return 0

if __name__ == "__main__":
    exit(main())
