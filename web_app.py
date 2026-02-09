#!/usr/bin/env python3
"""
Sprint Capacity Web Interface

A simple web interface for the Sprint Capacity Automation system.
Allows team members to view capacity reports and scrum masters to generate new reports.

Author: Sprint Capacity Automation System
Date: 2025-09-09
"""

from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for
import os
import json
from datetime import datetime
from sprint_capacity_app import SprintCapacityApp
import tempfile
import threading

app = Flask(__name__)
app.secret_key = 'sprint_capacity_secret_key_2025'

# Global variables
capacity_app = None
latest_report_data = None


def initialize_app():
    """Initialize the capacity app"""
    global capacity_app
    capacity_app = SprintCapacityApp()


@app.route('/')
def index():
    """Main dashboard page"""
    return serve_index_template()


@app.route('/api/analyze', methods=['POST'])
def analyze_capacity():
    """API endpoint to run capacity analysis"""
    try:
        global latest_report_data

        # Run analysis in background
        success = capacity_app.run_capacity_analysis()

        if success:
            # Get the latest report data
            sprints = capacity_app.sprint_manager.get_current_and_upcoming_sprints()
            sprint_capacities = []

            for sprint in sprints:
                capacity = capacity_app.sprint_manager.calculate_sprint_capacity(
                    sprint)
                sprint_capacities.append({
                    'sprint_number': capacity.sprint.number,
                    'start_date': capacity.sprint.start_date.strftime('%Y-%m-%d'),
                    'end_date': capacity.sprint.end_date.strftime('%Y-%m-%d'),
                    'total_members': capacity.total_team_members,
                    'available_members': capacity.available_members,
                    'capacity_percentage': round(capacity.capacity_percentage, 1),
                    'working_days': capacity.working_days,
                    'ideal_capacity_hours': round(capacity.ideal_capacity_hours, 1),
                    'actual_capacity_hours': round(capacity.actual_capacity_hours, 1),
                    'members_on_leave': [
                        {
                            'name': emp.name,
                            'emp_id': emp.emp_id,
                            'reason': reason
                        }
                        for emp, reason in capacity.members_on_leave
                    ]
                })

            latest_report_data = {
                'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'sprint_capacities': sprint_capacities
            }

            return jsonify({
                'success': True,
                'message': 'Analysis completed successfully',
                'data': latest_report_data
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Analysis failed. Check logs for details.'
            }), 500

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error during analysis: {str(e)}'
        }), 500


@app.route('/api/report-data')
def get_report_data():
    """Get the latest report data"""
    global latest_report_data

    if latest_report_data:
        return jsonify(latest_report_data)
    else:
        return jsonify({
            'message': 'No report data available. Run analysis first.'
        }), 404


@app.route('/api/config', methods=['GET', 'POST'])
def handle_config():
    """Handle configuration management"""
    if request.method == 'GET':
        return jsonify(capacity_app.calculator.config)

    elif request.method == 'POST':
        try:
            new_config = request.json

            # Update configuration
            capacity_app.calculator.config.update(new_config)

            # Save to file
            with open('config.json', 'w') as f:
                json.dump(capacity_app.calculator.config, f, indent=2)

            return jsonify({
                'success': True,
                'message': 'Configuration updated successfully'
            })

        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error updating configuration: {str(e)}'
            }), 500


@app.route('/download/<report_type>')
def download_report(report_type):
    """Download report files"""
    try:
        # Find the latest report file
        files = [f for f in os.listdir(
            '.') if f.startswith('sprint_capacity_report_')]

        if report_type == 'txt':
            txt_files = [f for f in files if f.endswith('.txt')]
            if txt_files:
                latest_file = max(txt_files, key=os.path.getctime)
                return send_file(latest_file, as_attachment=True)

        elif report_type == 'html':
            html_files = [f for f in files if f.endswith('.html')]
            if html_files:
                latest_file = max(html_files, key=os.path.getctime)
                return send_file(latest_file, as_attachment=True)

        return jsonify({'error': 'Report file not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# HTML Templates (embedded for simplicity)


@app.route('/templates/index.html')
def serve_index_template():
    """Serve the main template"""
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sprint Capacity Dashboard</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #e0e0e0;
        }
        .controls {
            margin-bottom: 30px;
            text-align: center;
        }
        .btn {
            background-color: #007bff;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
            margin: 0 10px;
            font-size: 16px;
        }
        .btn:hover {
            background-color: #0056b3;
        }
        .btn:disabled {
            background-color: #6c757d;
            cursor: not-allowed;
        }
        .loading {
            display: none;
            text-align: center;
            margin: 20px 0;
        }
        .report-container {
            margin-top: 30px;
        }
        .sprint-card {
            border: 1px solid #ddd;
            border-radius: 8px;
            margin-bottom: 20px;
            overflow: hidden;
        }
        .sprint-header {
            background-color: #f8f9fa;
            padding: 15px;
            font-weight: bold;
            border-bottom: 1px solid #ddd;
        }
        .sprint-content {
            padding: 15px;
        }
        .capacity-good { color: #28a745; }
        .capacity-warning { color: #ffc107; }
        .capacity-critical { color: #dc3545; }
        .leave-list {
            margin-top: 10px;
        }
        .leave-item {
            background-color: #f8f9fa;
            padding: 8px;
            margin: 5px 0;
            border-radius: 4px;
            border-left: 4px solid #007bff;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        .stat-card {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }
        .stat-value {
            font-size: 24px;
            font-weight: bold;
            color: #007bff;
        }
        .stat-label {
            font-size: 14px;
            color: #6c757d;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Sprint Capacity Dashboard</h1>
            <p>Agile Team Capacity Planning & Analysis</p>
        </div>
        
        <div class="controls">
            <button class="btn" onclick="runAnalysis()">📊 Run Capacity Analysis</button>
            <button class="btn" onclick="downloadReport('txt')">📄 Download Text Report</button>
            <button class="btn" onclick="downloadReport('html')">🌐 Download HTML Report</button>
        </div>
        
        <div class="loading" id="loading">
            <p>🔄 Running capacity analysis...</p>
        </div>
        
        <div class="report-container" id="reportContainer" style="display: none;">
            <!-- Report content will be loaded here -->
        </div>
    </div>

    <script>
        async function runAnalysis() {
            const loadingDiv = document.getElementById('loading');
            const reportContainer = document.getElementById('reportContainer');
            
            loadingDiv.style.display = 'block';
            reportContainer.style.display = 'none';
            
            try {
                const response = await fetch('/api/analyze', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
                
                const result = await response.json();
                
                if (result.success) {
                    displayReport(result.data);
                } else {
                    alert('Analysis failed: ' + result.message);
                }
            } catch (error) {
                alert('Error: ' + error.message);
            } finally {
                loadingDiv.style.display = 'none';
            }
        }
        
        function displayReport(data) {
            const container = document.getElementById('reportContainer');
            
            let html = `
                <h2>📈 Sprint Capacity Report</h2>
                <p><strong>Generated:</strong> ${data.generated_at}</p>
                
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-value">${data.sprint_capacities.length}</div>
                        <div class="stat-label">Sprints Analyzed</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">${data.sprint_capacities[0]?.total_members || 0}</div>
                        <div class="stat-label">Team Members</div>
                    </div>
                </div>
            `;
            
            data.sprint_capacities.forEach(sprint => {
                const capacityClass = sprint.capacity_percentage >= 80 ? 'capacity-good' : 
                                    sprint.capacity_percentage >= 60 ? 'capacity-warning' : 'capacity-critical';
                
                html += `
                    <div class="sprint-card">
                        <div class="sprint-header">
                            Sprint ${sprint.sprint_number} - ${sprint.start_date} to ${sprint.end_date}
                        </div>
                        <div class="sprint-content">
                            <div class="stats-grid">
                                <div class="stat-card">
                                    <div class="stat-value">${sprint.working_days}</div>
                                    <div class="stat-label">Working Days</div>
                                </div>
                                <div class="stat-card">
                                    <div class="stat-value">${sprint.available_members}/${sprint.total_members}</div>
                                    <div class="stat-label">Available Members</div>
                                </div>
                                <div class="stat-card">
                                    <div class="stat-value ${capacityClass}">${sprint.capacity_percentage}%</div>
                                    <div class="stat-label">Team Capacity</div>
                                </div>
                                <div class="stat-card">
                                    <div class="stat-value">${sprint.ideal_capacity_hours} hrs</div>
                                    <div class="stat-label">Ideal Capacity</div>
                                </div>
                                <div class="stat-card">
                                    <div class="stat-value">${sprint.actual_capacity_hours} hrs</div>
                                    <div class="stat-label">Actual Capacity</div>
                                </div>
                            </div>
                            
                            ${sprint.members_on_leave.length > 0 ? `
                                <h4>Members on Leave:</h4>
                                <div class="leave-list">
                                    ${sprint.members_on_leave.map(member => `
                                        <div class="leave-item">
                                            <strong>${member.name}</strong> (${member.emp_id}): ${member.reason}
                                        </div>
                                    `).join('')}
                                </div>
                            ` : '<p><em>No team members on leave during this sprint.</em></p>'}
                        </div>
                    </div>
                `;
            });
            
            container.innerHTML = html;
            container.style.display = 'block';
        }
        
        function downloadReport(type) {
            window.open(`/download/${type}`, '_blank');
        }
        
        // Load existing report data on page load
        window.onload = async function() {
            try {
                const response = await fetch('/api/report-data');
                if (response.ok) {
                    const data = await response.json();
                    displayReport(data);
                }
            } catch (error) {
                console.log('No existing report data found');
            }
        };
    </script>
</body>
</html>
    """
    return html_content


if __name__ == '__main__':
    initialize_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
