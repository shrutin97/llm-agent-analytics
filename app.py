import os
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
import pandas as pd
import numpy as np

# Create the FastAPI app
app = FastAPI(
    title="LLM Agent Analytics Dashboard",
    description="Track and analyze performance metrics for LLM agents",
    version="1.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Mock data generator for LLM agent analytics
def generate_mock_data():
    """Generate mock data for LLM agent analytics if not exists"""
    os.makedirs("data", exist_ok=True)
    
    # Generate agents data
    agents = []
    agent_names = ["Research Assistant", "Customer Support Bot", "Code Generator", 
                  "Data Analyst", "Content Moderator", "Meeting Assistant"]
    agent_models = ["GPT-4", "Claude 3 Opus", "Claude 3 Sonnet", "GPT-4o", "Mistral Large", "LLaMA 3"]
    
    for i in range(6):
        agent = {
            "id": f"agent_{i+1}",
            "name": agent_names[i],
            "model": agent_models[i % len(agent_models)],
            "description": f"An LLM agent that helps with {agent_names[i].lower()} tasks",
            "created_at": (datetime.now() - timedelta(days=90 + i*10)).isoformat(),
            "team_members": [f"member_{((i*2) % 10) + 1}", f"member_{((i*2+1) % 10) + 1}"],
            "status": "active" if i < 5 else "inactive",
            "version": f"1.{i+1}"
        }
        agents.append(agent)
    
    with open("data/agents.json", "w") as f:
        json.dump(agents, f, indent=2)
    
    # Generate team members data
    team_members = []
    first_names = ["Alex", "Casey", "Jordan", "Taylor", "Morgan", "Riley", "Sam", "Jamie", "Quinn", "Avery"]
    last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor"]
    
    for i in range(10):
        member = {
            "id": f"member_{i+1}",
            "name": f"{first_names[i]} {last_names[i]}",
            "role": "AI Engineer" if i < 5 else "Product Manager",
            "email": f"{first_names[i].lower()}.{last_names[i].lower()}@example.com",
            "avatar": f"/static/img/avatar_{(i % 5) + 1}.png"
        }
        team_members.append(member)
    
    with open("data/team_members.json", "w") as f:
        json.dump(team_members, f, indent=2)
    
    # Generate daily metrics for each agent
    all_metrics = {}
    
    for agent in agents:
        agent_id = agent["id"]
        agent_metrics = []
        
        # Base values that will be adjusted for each agent
        base_usage = 1000 if agent["status"] == "active" else 500
        base_success_rate = 0.92
        base_response_time = 2.5
        base_tokens_per_query = 1200
        base_cost_per_1k = 0.03
        
        # Generate 30 days of data
        for day in range(30):
            date = (datetime.now() - timedelta(days=30-day)).strftime("%Y-%m-%d")
            
            # Add some randomness and trends
            day_factor = 1.0 + (day / 60)  # Slight upward trend
            weekend_factor = 0.7 if (datetime.now() - timedelta(days=30-day)).weekday() >= 5 else 1.0
            random_factor = np.random.normal(1.0, 0.1)  # Random noise
            
            # Calculate metrics with factors
            total_queries = int(base_usage * day_factor * weekend_factor * random_factor)
            success_rate = min(0.99, base_success_rate + (day / 300))
            avg_response_time = base_response_time * (1.0 - (day / 200)) * random_factor
            
            # More metrics with some correlation
            tokens_per_query = int(base_tokens_per_query * random_factor)
            total_tokens = tokens_per_query * total_queries
            cost_per_1k = base_cost_per_1k * (0.95 + (day / 600))  # Slight cost increase over time
            total_cost = (total_tokens / 1000) * cost_per_1k
            
            # Add some specific patterns for different agents
            if agent_id == "agent_1":  # Research Assistant gets more usage
                total_queries = int(total_queries * 1.4)
                total_tokens = int(total_tokens * 1.5)
                total_cost = (total_tokens / 1000) * cost_per_1k
            elif agent_id == "agent_3":  # Code Generator has longer responses
                tokens_per_query = int(tokens_per_query * 1.8)
                total_tokens = tokens_per_query * total_queries
                total_cost = (total_tokens / 1000) * cost_per_1k
            
            # Success and error metrics
            successful_queries = int(total_queries * success_rate)
            failed_queries = total_queries - successful_queries
            error_types = {
                "timeout": int(failed_queries * 0.3),
                "context_length": int(failed_queries * 0.2),
                "rate_limit": int(failed_queries * 0.15),
                "api_error": int(failed_queries * 0.2),
                "other": int(failed_queries * 0.15)
            }
            
            # Generate user ratings with a distribution favoring 4-5 stars
            ratings_count = int(total_queries * 0.4)  # 40% of users leave ratings
            ratings_dist = [0.02, 0.08, 0.15, 0.35, 0.4]  # Distribution across 1-5 stars
            ratings = {
                str(star): int(ratings_count * dist) for star, dist in enumerate(ratings_dist, 1)
            }
            avg_rating = sum(int(star) * count for star, count in ratings.items()) / ratings_count if ratings_count > 0 else 0
            
            # Add some correlation between ratings and success rate
            avg_rating = avg_rating * (0.9 + (success_rate / 10))
            
            # User engagement metrics
            avg_turns_per_session = 4.2 + (random_factor - 1.0) * 3
            avg_time_to_resolution = avg_response_time * avg_turns_per_session * (1.0 + (1.0 - success_rate) * 2)
            
            # Tool usage metrics
            tools_available = ["search", "calculator", "database", "code_execution", "summarization"]
            tool_usage = {
                tool: int(total_queries * np.random.uniform(0.1, 0.5)) for tool in tools_available
            }
            
            # Add agent-specific tool usage patterns
            if agent_id == "agent_1":  # Research Assistant uses search more
                tool_usage["search"] = int(total_queries * 0.8)
            elif agent_id == "agent_3":  # Code Generator uses code execution more
                tool_usage["code_execution"] = int(total_queries * 0.9)
            elif agent_id == "agent_4":  # Data Analyst uses database and calculator more
                tool_usage["database"] = int(total_queries * 0.7)
                tool_usage["calculator"] = int(total_queries * 0.6)
            
            # Hallucination metrics (simulated)
            hallucination_rate = max(0.01, 0.1 - (success_rate - 0.85) * 2)
            hallucination_count = int(total_queries * hallucination_rate)
            
            # Create the day's metrics
            day_metrics = {
                "date": date,
                "total_queries": total_queries,
                "success_rate": success_rate,
                "avg_response_time": avg_response_time,
                "tokens_per_query": tokens_per_query,
                "total_tokens": total_tokens,
                "cost_per_1k_tokens": cost_per_1k,
                "total_cost": total_cost,
                "successful_queries": successful_queries,
                "failed_queries": failed_queries,
                "error_types": error_types,
                "ratings": ratings,
                "avg_rating": avg_rating,
                "avg_turns_per_session": avg_turns_per_session,
                "avg_time_to_resolution": avg_time_to_resolution,
                "tool_usage": tool_usage,
                "hallucination_rate": hallucination_rate,
                "hallucination_count": hallucination_count
            }
            
            agent_metrics.append(day_metrics)
        
        all_metrics[agent_id] = agent_metrics
    
    with open("data/agent_metrics.json", "w") as f:
        json.dump(all_metrics, f, indent=2)

# Helper function to load data
def load_data(filename):
    path = os.path.join("data", filename)
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return None

# Helper function to get agent by ID
def get_agent_by_id(agent_id):
    agents = load_data("agents.json")
    if agents:
        for agent in agents:
            if agent["id"] == agent_id:
                return agent
    return None

# Helper function to get team member by ID
def get_team_member_by_id(member_id):
    members = load_data("team_members.json")
    if members:
        for member in members:
            if member["id"] == member_id:
                return member
    return None

# Helper function to get agent metrics
def get_agent_metrics(agent_id, days=30):
    metrics = load_data("agent_metrics.json")
    if metrics and agent_id in metrics:
        return metrics[agent_id][-days:]
    return []

# Helper to calculate summary metrics across all agents
def get_summary_metrics(days=30):
    agents = load_data("agents.json")
    metrics = load_data("agent_metrics.json")
    
    if not agents or not metrics:
        return {}
    
    summary = {
        "total_queries": 0,
        "total_tokens": 0,
        "total_cost": 0,
        "avg_success_rate": 0,
        "avg_response_time": 0,
        "total_successful_queries": 0,
        "total_failed_queries": 0,
        "error_types": {
            "timeout": 0,
            "context_length": 0,
            "rate_limit": 0,
            "api_error": 0,
            "other": 0
        },
        "avg_rating": 0,
        "daily_queries": {},
        "daily_costs": {},
        "model_usage": {},
        "agent_comparison": []
    }
    
    active_agents = [a for a in agents if a["status"] == "active"]
    
    for agent in active_agents:
        agent_id = agent["id"]
        if agent_id in metrics:
            agent_data = metrics[agent_id][-days:]
            
            # Aggregations
            agent_total_queries = sum(day["total_queries"] for day in agent_data)
            agent_total_tokens = sum(day["total_tokens"] for day in agent_data)
            agent_total_cost = sum(day["total_cost"] for day in agent_data)
            agent_success_rates = [day["success_rate"] for day in agent_data]
            agent_response_times = [day["avg_response_time"] for day in agent_data]
            agent_ratings = [day.get("avg_rating", 0) for day in agent_data if day.get("avg_rating", 0) > 0]
            
            # Update summary
            summary["total_queries"] += agent_total_queries
            summary["total_tokens"] += agent_total_tokens
            summary["total_cost"] += agent_total_cost
            summary["total_successful_queries"] += sum(day["successful_queries"] for day in agent_data)
            summary["total_failed_queries"] += sum(day["failed_queries"] for day in agent_data)
            
            # Error types
            for day in agent_data:
                for error_type, count in day["error_types"].items():
                    summary["error_types"][error_type] += count
            
            # Track by model
            model = agent["model"]
            if model not in summary["model_usage"]:
                summary["model_usage"][model] = {
                    "queries": 0,
                    "tokens": 0,
                    "cost": 0
                }
            summary["model_usage"][model]["queries"] += agent_total_queries
            summary["model_usage"][model]["tokens"] += agent_total_tokens
            summary["model_usage"][model]["cost"] += agent_total_cost
            
            # Daily tracking for time series
            for day in agent_data:
                date = day["date"]
                if date not in summary["daily_queries"]:
                    summary["daily_queries"][date] = 0
                    summary["daily_costs"][date] = 0
                
                summary["daily_queries"][date] += day["total_queries"]
                summary["daily_costs"][date] += day["total_cost"]
            
            # Add to agent comparison
            summary["agent_comparison"].append({
                "id": agent_id,
                "name": agent["name"],
                "model": agent["model"],
                "total_queries": agent_total_queries,
                "avg_success_rate": sum(agent_success_rates) / len(agent_success_rates) if agent_success_rates else 0,
                "avg_response_time": sum(agent_response_times) / len(agent_response_times) if agent_response_times else 0,
                "total_cost": agent_total_cost,
                "avg_rating": sum(agent_ratings) / len(agent_ratings) if agent_ratings else 0
            })
    
    # Calculate averages
    num_active_agents = len(active_agents)
    if num_active_agents > 0:
        # Averaging success rate across all agents
        success_rates = []
        response_times = []
        ratings = []
        
        for agent in summary["agent_comparison"]:
            success_rates.append(agent["avg_success_rate"])
            response_times.append(agent["avg_response_time"])
            if agent["avg_rating"] > 0:
                ratings.append(agent["avg_rating"])
        
        summary["avg_success_rate"] = sum(success_rates) / len(success_rates) if success_rates else 0
        summary["avg_response_time"] = sum(response_times) / len(response_times) if response_times else 0
        summary["avg_rating"] = sum(ratings) / len(ratings) if ratings else 0
    
    # Sort daily data for charts
    summary["daily_queries"] = dict(sorted(summary["daily_queries"].items()))
    summary["daily_costs"] = dict(sorted(summary["daily_costs"].items()))
    
    # Sort agent comparison by total queries
    summary["agent_comparison"] = sorted(
        summary["agent_comparison"], 
        key=lambda x: x["total_queries"], 
        reverse=True
    )
    
    return summary

# Routes
@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    # Generate mock data if it doesn't exist
    if not os.path.exists("data/agents.json"):
        generate_mock_data()
    
    agents = load_data("agents.json") or []
    summary = get_summary_metrics()
    
    return templates.TemplateResponse(
        "dashboard.html", 
        {
            "request": request,
            "summary": summary,
            "agents": agents
        }
    )

@app.get("/agent/{agent_id}", response_class=HTMLResponse)
async def agent_detail(request: Request, agent_id: str):
    agents = load_data("agents.json") or []
    agent = get_agent_by_id(agent_id)
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Get agent metrics and team member details
    metrics = get_agent_metrics(agent_id)
    team_members = []
    for member_id in agent["team_members"]:
        member = get_team_member_by_id(member_id)
        if member:
            team_members.append(member)
    
    return templates.TemplateResponse(
        "agent_detail.html", 
        {
            "request": request,
            "agent": agent,
            "metrics": metrics,
            "team_members": team_members,
            "agents": agents
        }
    )

@app.get("/team", response_class=HTMLResponse)
async def team_overview(request: Request):
    agents = load_data("agents.json") or []
    team_members = load_data("team_members.json") or []
    
    # Enrich team members with their assigned agents
    for member in team_members:
        member["assigned_agents"] = []
        for agent in agents:
            if member["id"] in agent["team_members"]:
                member["assigned_agents"].append({
                    "id": agent["id"],
                    "name": agent["name"],
                    "status": agent["status"]
                })
    
    return templates.TemplateResponse(
        "team.html", 
        {
            "request": request,
            "team_members": team_members,
            "agents": agents
        }
    )

@app.get("/compare", response_class=HTMLResponse)
async def compare_agents(request: Request):
    agents = load_data("agents.json") or []
    
    return templates.TemplateResponse(
        "compare.html", 
        {
            "request": request,
            "agents": agents
        }
    )

@app.get("/api/agent/{agent_id}/metrics")
async def api_agent_metrics(agent_id: str, days: int = 30):
    metrics = get_agent_metrics(agent_id, days)
    return metrics

@app.get("/api/summary")
async def api_summary(days: int = 30):
    summary = get_summary_metrics(days)
    return summary

@app.get("/api/compare")
async def api_compare_agents(agent_ids: str, metric: str = "total_queries", days: int = 30):
    agent_id_list = agent_ids.split(",")
    metrics = {}
    
    for agent_id in agent_id_list:
        agent_metrics = get_agent_metrics(agent_id, days)
        if agent_metrics:
            # Get daily values of the specified metric
            daily_values = []
            for day in agent_metrics:
                date = day["date"]
                value = day.get(metric, 0)
                daily_values.append({"date": date, "value": value})
            
            metrics[agent_id] = daily_values
    
    return metrics

if __name__ == "__main__":
    import uvicorn
    
    # Create sample data if it doesn't exist
    if not os.path.exists("data/agents.json"):
        generate_mock_data()
    
    # Start the app
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)