---
title: AI Incident Response Simulator
emoji: 🚀
sdk: gradio
app_file: app.py
tags:
  - openenv
---

# 🚀 AI Incident Response Simulator

## 💡 Overview
This project simulates real-world DevOps incident response tasks where an AI agent must analyze logs, metrics, and alerts to take corrective actions.

## 🎯 Motivation
Modern infrastructure requires automated incident handling. This environment enables training and evaluating AI agents for SRE/DevOps workflows.

---

## 📊 Observation Space
- `logs`: system logs (string)
- `metrics`: CPU, latency, error_rate (dict)
- `alerts`: triggered alerts (list)

---

## 🎮 Action Space
Agent must choose ONE:
- restart_service
- scale_up
- rollback
- ignore

---

## 🧠 Tasks

| Task | Description | Difficulty |
|------|------------|-----------|
| DB Timeout | Fix latency spike | Easy |
| Traffic Spike | Handle CPU overload | Medium |
| Deployment Failure | Fix crash loop | Hard |

---

## 🏆 Reward Function
- +1.0 → correct action  
- -0.2 → wrong action  
- +0.3 → latency improvement  
- +0.3 → error reduction  
- +grader bonus  

Normalized to [0,1]

---

## 🤖 Baseline Agent

Run:
```bash
export OPENAI_API_KEY=your_key
python baseline.py