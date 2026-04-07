import os
from openai import OpenAI
from openenv.env import IncidentEnv, Action

client = OpenAI(api_key=os.getenv("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"))

env = IncidentEnv()

def choose_action(obs):
    prompt = f"""
You are a DevOps AI agent.

Logs: {obs.logs}
Metrics: {obs.metrics}
Alerts: {obs.alerts}

Choose ONE action:
restart_service, scale_up, rollback, ignore

Only return the action name.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content.strip()


total_score = 0

for _ in range(3):
    obs = env.reset()
    done = False

    while not done:
        action_str = choose_action(obs)
        obs, reward, done, _ = env.step(Action(action_type=action_str))
        total_score += reward.value

print("Final Baseline Score:", total_score)