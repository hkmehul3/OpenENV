import os
from openai import OpenAI
from openenv.env import IncidentEnv, Action

# ----------------------------
# ENV VARIABLES
# ----------------------------
API_BASE_URL = os.getenv("API_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")
HF_TOKEN = os.getenv("HF_TOKEN")

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN
)

# ----------------------------
# SIMPLE AGENT (LLM-assisted)
# ----------------------------
def choose_action(observation):
    prompt = f"""
You are an SRE agent.

Logs: {observation.logs}
Metrics: {observation.metrics}
Alerts: {observation.alerts}

Choose one action:
restart_service, scale_up, rollback, ignore

Only return action name.
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content.strip()


# ----------------------------
# RUN ENV
# ----------------------------
env = IncidentEnv()
total_score = 0

for task_id in range(3):
    obs = env.reset()

    print("[START]")
    print(f"task_id={task_id}")

    done = False
    final_reward = 0

    while not done:
        action_str = choose_action(obs)

        # safety fallback
        if action_str not in ["restart_service", "scale_up", "rollback", "ignore"]:
            action_str = "ignore"

        obs, reward, done, info = env.step(Action(action_type=action_str))

        final_reward = reward.value

        print("\n[STEP]")
        print(f"action={action_str}")
        print(f"reward={reward.value}")
        print(f"done={done}")

    print("\n[END]")
    print(f"score={final_reward}")

    total_score += final_reward

print("\nFINAL_SCORE =", total_score / 3)