import gradio as gr
from openenv.env import IncidentEnv, Action

env = IncidentEnv()
state = env.reset()

history = []

def take_action(action_type):
    global state, history

    obs, reward, done, info = env.step(Action(action_type=action_type))
    history = info["history"]

    return (
        f"📜 Logs: {obs.logs}\n\n"
        f"📊 Metrics: {obs.metrics}\n\n"
        f"🚨 Alerts: {obs.alerts}\n\n"
        f"⚡ Reward: {reward.value}\n"
        f"🏁 Done: {done}\n"
        f"✅ Correct: {info['correct_action']}\n\n"
        f"🧠 History: {history}"
    )

def reset_env():
    global state, history
    state = env.reset()
    history = []
    return "🔄 Environment Reset!"

with gr.Blocks() as demo:
    gr.Markdown("# 🚀 AI Incident Response Simulator")

    output = gr.Textbox(lines=15)

    with gr.Row():
        gr.Button("Restart Service").click(lambda: take_action("restart_service"), outputs=output)
        gr.Button("Scale Up").click(lambda: take_action("scale_up"), outputs=output)
        gr.Button("Rollback").click(lambda: take_action("rollback"), outputs=output)
        gr.Button("Ignore").click(lambda: take_action("ignore"), outputs=output)

    gr.Button("Reset").click(reset_env, outputs=output)

demo.launch()