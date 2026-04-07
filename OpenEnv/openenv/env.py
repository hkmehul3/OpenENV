from typing import Dict, List, Tuple
from pydantic import BaseModel
from openenv.grader import grade_easy, grade_medium, grade_hard


# -------------------------------
# OpenEnv Models
# -------------------------------
class Observation(BaseModel):
    logs: str
    metrics: Dict[str, float]
    alerts: List[str]


class Action(BaseModel):
    action_type: str


class Reward(BaseModel):
    value: float


# -------------------------------
# Environment
# -------------------------------
class IncidentEnv:
    def __init__(self):
        self.max_steps = 5
        self.current_step = 0
        self.task_id = -1
        self.history = []

        self.tasks = [
            {
                "logs": "Error: DB connection timeout",
                "metrics": {"cpu": 40.0, "latency": 900.0, "error_rate": 0.3},
                "alerts": ["High latency", "DB timeout"],
                "correct_action": "restart_service"
            },
            {
                "logs": "Traffic spike detected",
                "metrics": {"cpu": 90.0, "latency": 700.0, "error_rate": 0.2},
                "alerts": ["High CPU"],
                "correct_action": "scale_up"
            },
            {
                "logs": "Deployment crash loop",
                "metrics": {"cpu": 60.0, "latency": 1200.0, "error_rate": 0.6},
                "alerts": ["Crash loop"],
                "correct_action": "rollback"
            }
        ]

    # -------------------------------
    # Reset
    # -------------------------------
    def reset(self) -> Observation:
        self.current_step = 0
        self.history = []
        self.task_id = (self.task_id + 1) % len(self.tasks)
        self.state_data = self.tasks[self.task_id].copy()

        return Observation(
            logs=self.state_data["logs"],
            metrics=self.state_data["metrics"],
            alerts=self.state_data["alerts"]
        )

    # -------------------------------
    # Step
    # -------------------------------
    def step(self, action: Action) -> Tuple[Observation, Reward, bool, dict]:
        self.current_step += 1
        self.history.append(action.action_type)

        correct = self.state_data["correct_action"]
        reward = 0.0

        # -------------------------------
        # Base reward (strong signal)
        # -------------------------------
        if action.action_type == correct:
            reward += 1.0
        else:
            reward -= 0.5

        # -------------------------------
        # Simulate real system changes
        # -------------------------------
        if action.action_type == "restart_service":
            self.state_data["metrics"]["latency"] -= 500
            self.state_data["metrics"]["error_rate"] -= 0.15

        elif action.action_type == "scale_up":
            self.state_data["metrics"]["cpu"] -= 40
            self.state_data["metrics"]["latency"] -= 250

        elif action.action_type == "rollback":
            self.state_data["metrics"]["error_rate"] -= 0.5

        elif action.action_type == "ignore":
            reward -= 0.3  # strong penalty

        # -------------------------------
        # Clamp metrics (REALISM FIX)
        # -------------------------------
        m = self.state_data["metrics"]

        m["latency"] = max(0.0, m["latency"])
        m["cpu"] = max(0.0, m["cpu"])
        m["error_rate"] = max(0.0, min(1.0, m["error_rate"]))

        # -------------------------------
        # Partial rewards (progress-based)
        # -------------------------------
        if m["latency"] < 500:
            reward += 0.2

        if m["error_rate"] < 0.2:
            reward += 0.2

        if m["cpu"] < 50:
            reward += 0.1

        # -------------------------------
        # Grader bonus (task success)
        # -------------------------------
        if self.task_id == 0:
            reward += grade_easy(self.history)
        elif self.task_id == 1:
            reward += grade_medium(self.history)
        else:
            reward += grade_hard(self.history)

        # -------------------------------
        # DONE condition (REALISTIC)
        # -------------------------------
        done = (
            m["latency"] < 400 and m["error_rate"] < 0.1
        ) or self.current_step >= self.max_steps

        # -------------------------------
        # Normalize reward (OpenEnv requirement)
        # -------------------------------
        reward = max(0.0, min(reward, 1.0))

        # -------------------------------
        # Return
        # -------------------------------
        observation = Observation(
            logs=self.state_data["logs"],
            metrics=m,
            alerts=self.state_data["alerts"]
        )

        return observation, Reward(value=reward), done, {
            "history": self.history,
            "correct_action": correct,
            "step": self.current_step
        }

    # -------------------------------
    # State
    # -------------------------------
    def state(self) -> dict:
        return {
            "task_id": self.task_id,
            "step": self.current_step,
            "metrics": self.state_data["metrics"],
            "history": self.history
        }