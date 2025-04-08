# LLM Agent Analytics Dashboard

A sleek, dark-mode dashboard for monitoring and analyzing LLM agent performance metrics.

## Features

- **Overview Dashboard:** Track key metrics across all agents including total queries, success rates, response times, and costs
- **Agent Details:** Dive deep into individual agent performance with detailed charts and metrics
- **Team Management:** View team member assignments and workload distribution
- **Agent Comparison:** Compare performance metrics across multiple agents
- **Interactive Visualizations:** Explore data through various chart types with download and expand capabilities

## Metrics Tracked

- **Usage Metrics:** Total queries, tokens, conversations
- **Performance Metrics:** Success rate, response time, time to resolution
- **Quality Metrics:** User ratings, hallucination rate
- **Cost Metrics:** Total cost, cost per query, cost per token
- **Error Analysis:** Error types, error distribution
- **Tool Usage:** Frequency and patterns of tool usage by agents

## Tech Stack

- **Backend:** FastAPI, Python
- **Frontend:** HTML, CSS, JavaScript
- **Data Visualization:** Chart.js
- **Templating:** Jinja2

## Setup and Installation

1. Clone the repository
2. Run the setup script:
   ```
   chmod +x run.sh
   ./run.sh
   ```
3. Access the dashboard at http://localhost:8000

## Dashboard Sections

- **Overview:** High-level metrics and trends across all agents
- **Agent Detail:** In-depth analysis of individual agent performance
- **Team:** Team member assignments and workload distribution
- **Compare:** Side-by-side comparison of multiple agents

## Development Roadmap

- Add user authentication and role-based access
- Implement real-time monitoring capabilities
- Add export functionality for reports
- Create custom alert and notification systems
- Integrate with external monitoring tools