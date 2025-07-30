#!/usr/bin/env python3
"""
🦖 HTML Test Report Generator for Restaceratops
Generates beautiful, interactive HTML reports with charts and analysis
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Any
import base64

class HTMLReporter:
    """Generate beautiful HTML test reports."""
    
    def __init__(self, output_path: str = "reports/test_report.html"):
        self.output_path = Path(output_path)
        self.results = []
        self.start_time = time.time()
        self.metadata = {
            "project_name": "Restaceratops API Tests",
            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "version": "1.0.0"
        }
    
    def record(self, step_name: str, success: bool, latency_ms: float, error: str = None):
        """Record a test result."""
        self.results.append({
            "name": step_name,
            "success": success,
            "latency_ms": latency_ms,
            "error": error,
            "timestamp": time.time()
        })
    
    def _generate_chart_data(self) -> Dict:
        """Generate data for charts."""
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r["success"])
        failed_tests = total_tests - passed_tests
        
        # Performance data
        latencies = [r["latency_ms"] for r in self.results]
        avg_latency = sum(latencies) / len(latencies) if latencies else 0
        max_latency = max(latencies) if latencies else 0
        min_latency = min(latencies) if latencies else 0
        
        # Status distribution
        status_data = [
            {"status": "Passed", "count": passed_tests, "color": "#28a745"},
            {"status": "Failed", "count": failed_tests, "color": "#dc3545"}
        ]
        
        # Performance distribution
        performance_ranges = [
            {"range": "0-100ms", "count": sum(1 for l in latencies if l <= 100)},
            {"range": "100-500ms", "count": sum(1 for l in latencies if 100 < l <= 500)},
            {"range": "500-1000ms", "count": sum(1 for l in latencies if 500 < l <= 1000)},
            {"range": "1000ms+", "count": sum(1 for l in latencies if l > 1000)}
        ]
        
        return {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "success_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0,
            "avg_latency": avg_latency,
            "max_latency": max_latency,
            "min_latency": min_latency,
            "status_data": status_data,
            "performance_ranges": performance_ranges
        }
    
    def _generate_html_template(self, chart_data: Dict) -> str:
        """Generate the HTML template with embedded CSS and JavaScript."""
        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🦖 Restaceratops Test Report</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .header .metadata {{
            display: flex;
            justify-content: space-around;
            margin-top: 20px;
            flex-wrap: wrap;
        }}
        
        .metadata-item {{
            text-align: center;
            margin: 10px;
        }}
        
        .metadata-value {{
            font-size: 1.5em;
            font-weight: bold;
        }}
        
        .metadata-label {{
            font-size: 0.9em;
            opacity: 0.9;
        }}
        
        .summary {{
            padding: 30px;
            background: #f8f9fa;
        }}
        
        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .summary-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
        }}
        
        .summary-card.success {{
            border-left: 5px solid #28a745;
        }}
        
        .summary-card.danger {{
            border-left: 5px solid #dc3545;
        }}
        
        .summary-card.info {{
            border-left: 5px solid #17a2b8;
        }}
        
        .summary-value {{
            font-size: 2em;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        
        .summary-label {{
            color: #666;
            font-size: 0.9em;
        }}
        
        .charts {{
            padding: 30px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 30px;
        }}
        
        .chart-container {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .chart-title {{
            text-align: center;
            margin-bottom: 20px;
            color: #333;
            font-size: 1.2em;
        }}
        
        .test-results {{
            padding: 30px;
        }}
        
        .test-results h2 {{
            margin-bottom: 20px;
            color: #333;
        }}
        
        .test-table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .test-table th {{
            background: #f8f9fa;
            padding: 15px;
            text-align: left;
            font-weight: 600;
            color: #333;
        }}
        
        .test-table td {{
            padding: 15px;
            border-top: 1px solid #eee;
        }}
        
        .test-table tr:hover {{
            background: #f8f9fa;
        }}
        
        .status-badge {{
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: bold;
        }}
        
        .status-passed {{
            background: #d4edda;
            color: #155724;
        }}
        
        .status-failed {{
            background: #f8d7da;
            color: #721c24;
        }}
        
        .error-details {{
            background: #f8f9fa;
            padding: 10px;
            border-radius: 5px;
            margin-top: 5px;
            font-family: monospace;
            font-size: 0.9em;
            color: #721c24;
        }}
        
        .footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            border-top: 1px solid #eee;
        }}
        
        @media (max-width: 768px) {{
            .charts {{
                grid-template-columns: 1fr;
            }}
            
            .summary-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
            
            .metadata {{
                flex-direction: column;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🦖 Restaceratops Test Report</h1>
            <p>AI-Powered API Testing Results</p>
            <div class="metadata">
                <div class="metadata-item">
                    <div class="metadata-value">{chart_data['total_tests']}</div>
                    <div class="metadata-label">Total Tests</div>
                </div>
                <div class="metadata-item">
                    <div class="metadata-value">{chart_data['passed_tests']}</div>
                    <div class="metadata-label">Passed</div>
                </div>
                <div class="metadata-item">
                    <div class="metadata-value">{chart_data['failed_tests']}</div>
                    <div class="metadata-label">Failed</div>
                </div>
                <div class="metadata-item">
                    <div class="metadata-value">{chart_data['success_rate']:.1f}%</div>
                    <div class="metadata-label">Success Rate</div>
                </div>
            </div>
        </div>
        
        <div class="summary">
            <div class="summary-grid">
                <div class="summary-card success">
                    <div class="summary-value">{chart_data['passed_tests']}</div>
                    <div class="summary-label">Tests Passed</div>
                </div>
                <div class="summary-card danger">
                    <div class="summary-value">{chart_data['failed_tests']}</div>
                    <div class="summary-label">Tests Failed</div>
                </div>
                <div class="summary-card info">
                    <div class="summary-value">{chart_data['avg_latency']:.1f}ms</div>
                    <div class="summary-label">Average Latency</div>
                </div>
                <div class="summary-card info">
                    <div class="summary-value">{chart_data['max_latency']:.1f}ms</div>
                    <div class="summary-label">Max Latency</div>
                </div>
            </div>
        </div>
        
        <div class="charts">
            <div class="chart-container">
                <div class="chart-title">Test Results Distribution</div>
                <canvas id="statusChart"></canvas>
            </div>
            <div class="chart-container">
                <div class="chart-title">Performance Distribution</div>
                <canvas id="performanceChart"></canvas>
            </div>
        </div>
        
        <div class="test-results">
            <h2>Detailed Test Results</h2>
            <table class="test-table">
                <thead>
                    <tr>
                        <th>Test Name</th>
                        <th>Status</th>
                        <th>Latency</th>
                        <th>Error Details</th>
                    </tr>
                </thead>
                <tbody>
                    {self._generate_test_rows()}
                </tbody>
            </table>
        </div>
        
        <div class="footer">
            <p>Generated by Restaceratops on {self.metadata['generated_at']}</p>
            <p>🦖 Part of Team Agentosaurus - The Future of AI-Augmented Testing</p>
        </div>
    </div>
    
    <script>
        // Status Chart
        const statusCtx = document.getElementById('statusChart').getContext('2d');
        new Chart(statusCtx, {{
            type: 'doughnut',
            data: {{
                labels: {json.dumps([item['status'] for item in chart_data['status_data']])},
                datasets: [{{
                    data: {json.dumps([item['count'] for item in chart_data['status_data']])},
                    backgroundColor: {json.dumps([item['color'] for item in chart_data['status_data']])},
                    borderWidth: 2,
                    borderColor: '#fff'
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{
                        position: 'bottom'
                    }}
                }}
            }}
        }});
        
        // Performance Chart
        const performanceCtx = document.getElementById('performanceChart').getContext('2d');
        new Chart(performanceCtx, {{
            type: 'bar',
            data: {{
                labels: {json.dumps([item['range'] for item in chart_data['performance_ranges']])},
                datasets: [{{
                    label: 'Number of Tests',
                    data: {json.dumps([item['count'] for item in chart_data['performance_ranges']])},
                    backgroundColor: 'rgba(40, 167, 69, 0.8)',
                    borderColor: 'rgba(40, 167, 69, 1)',
                    borderWidth: 1
                }}]
            }},
            options: {{
                responsive: true,
                scales: {{
                    y: {{
                        beginAtZero: true
                    }}
                }},
                plugins: {{
                    legend: {{
                        display: false
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""
    
    def _generate_test_rows(self) -> str:
        """Generate HTML table rows for test results."""
        rows = []
        for result in self.results:
            status_class = "status-passed" if result["success"] else "status-failed"
            status_text = "PASSED" if result["success"] else "FAILED"
            
            error_details = ""
            if not result["success"] and result["error"]:
                error_details = f'<div class="error-details">{result["error"]}</div>'
            
            row = f"""
                <tr>
                    <td>{result["name"]}</td>
                    <td><span class="status-badge {status_class}">{status_text}</span></td>
                    <td>{result["latency_ms"]:.1f}ms</td>
                    <td>{error_details}</td>
                </tr>
            """
            rows.append(row)
        
        return "\n".join(rows)
    
    def generate_report(self) -> Path:
        """Generate and save the HTML report."""
        chart_data = self._generate_chart_data()
        html_content = self._generate_html_template(chart_data)
        
        # Ensure output directory exists
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write HTML file
        with open(self.output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return self.output_path
    
    def summary(self) -> bool:
        """Generate report and return success status."""
        report_path = self.generate_report()
        print(f"📊 HTML report generated: {report_path}")
        
        # Return True if all tests passed
        return all(result["success"] for result in self.results) 