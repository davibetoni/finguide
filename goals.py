import json
import os
from datetime import datetime

GOAL_FILE = f"files/goals_{datetime.now().year}.json"

def load_goals():
    if os.path.exists(GOAL_FILE):
        with open(GOAL_FILE, "r") as f:
            return json.load(f)
    return {}

def save_goal(month, category, amount):
    goals = load_goals()
    if month not in goals:
        goals[month] = {}
    goals[month][category] = amount
    with open(GOAL_FILE, "w") as f:
        json.dump(goals, f, indent=2)

def get_goal(month, category):
    goals = load_goals()
    return goals.get(month, {}).get(category)
