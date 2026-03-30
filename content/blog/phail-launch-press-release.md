Title: Is Physical AI Ready? A New Leaderboard Measures Whether Robots Can Actually Do Real Work
Date: 2026-03-31
Category: Blog
Slug: phail-launch
URL: press/phail-launch.html
Save_as: press/phail-launch.html
Author: Positronic Team
Summary: Positronic Robotics launches PhAIL (Physical AI Leaderboard) – an ongoing, real-world benchmark evaluating robotics foundation models on commercial tasks using throughput and reliability metrics.
Image: theme/positronic/static/img/logo.png

*San Francisco, CA - March 31, 2026* - Positronic Robotics, a company helping developers make robots work with AI, launches PhAIL (Physical AI Leaderboard) - an ongoing, real-world benchmark evaluating robotics foundation models on commercial tasks using throughput and reliability metrics.

PhAIL evaluates models on physical robotic setups performing commercially relevant operations, starting with bin-to-bin order picking - one of the most common tasks in logistics and industrial automation. In this task, items are transferred one at a time from an inbound container to an outbound container. The current evaluation rig uses a Franka Research 3 robotic arm paired with a Robotiq 2F-85 gripper (DROID-style configuration), a reproducible and widely used research platform.

The leaderboard itself is hardware-agnostic, and additional robotic embodiments will be added beginning in Q2 2026 to reflect the diversity of hardware used in real-world deployments. Bin-to-bin picking is only the starting point: the goal of the benchmark is to measure how well AI models perform on repetitive, economically important operations that occur thousands of times per day in real facilities.

Instead of reporting academic "success rate," PhAIL measures Units Per Hour (UPH), and Mean Time Between Failures or Assists (MTBF/A).

Each run is executed on real hardware, not in simulation. Model checkpoints are selected randomly and evaluated in blinded conditions. Every run is logged and published with synchronized video, robot telemetry, station metadata, and scoring artifacts.

Physical AI has advanced rapidly in recent years, with foundation models capable of handling increasingly diverse manipulation tasks. But most benchmarks still rely on simulation or controlled laboratory conditions, and many public evaluations emphasize curated demo videos rather than sustained operation. For industrial deployment, two variables dominate: throughput and reliability.

PhAIL measures both directly. Models perform multiple timed runs on real hardware, each recorded with synchronized video, telemetry, and scoring artifacts. From these runs, PhAIL computes Units Per Hour and Mean Time Between Failures – the same metrics an operations manager would use to evaluate a deployment. The protocol is fully documented in the PhAIL white paper.

"We all dream about a robot that folds our laundry – but that's a task that happens once a day. In factories and logistics, the same operation runs hundreds of times per shift and most of those still aren't solved," said Sergey Arkhangelskiy, founder of Positronic Robotics. "Physical AI needs to prove itself there first, and PhAIL is how we measure whether it can."

In the inaugural evaluations, four models were fine-tuned and tested: OpenPI 0.5 (Physical Intelligence), GR00T (NVIDIA), SmolVLA (HuggingFace/LeRobot), and ACT (LeRobot) – as well as teleoperated and human baselines. The results show a measurable gap between current foundation models and human-level performance in both throughput and reliability on commercial picking tasks. Positronic frames it as calibration: a transparent baseline that allows progress to be measured consistently over time. As new models are released, they can be evaluated under the same protocol, creating a continuous, comparable record of performance.

PhAIL targets three structural issues in the Physical AI ecosystem:

1. **Lack of objective measurement of commercial readiness.** Most public metrics do not reflect factory-floor constraints.

2. **Unclear ROI signals for operators.** Success rates do not translate directly into deployment decisions.

3. **A broken feedback loop for model builders.** Without standardized, auditable benchmarks, it is difficult to iterate toward real-world reliability.

By publishing synchronized video, logs, firmware versions, hardware configuration, and scoring artifacts for every run, PhAIL emphasizes auditability and reproducibility.

PhAIL launches as a governed consortium rather than as a proprietary product. Nebius, the AI cloud company that provides the cloud foundation for the full robotics lifecycle, joins as a founding consortium partner, and Toloka participates as a data partner supporting evaluation processes. The benchmark is intended as a shared industry yardstick, not as a competitive marketing vehicle.

"Scaling physical AI requires a clear, shared standard for production readiness," said Evan Helda, Head of Physical AI at Nebius. "With no established blueprint for deploying these systems at scale, the PhAIL Leaderboard delivers an important benchmark grounded in real-world performance data—bringing greater transparency to what's ready for deployment. Nebius is committed to accelerating physical AI development across the ecosystem. Through our participation in the PhAIL consortium, we're proud to help advance the next phase of commercial robotics alongside industry partners."

The PhAIL dataset and fine-tuning scripts are publicly available. Model builders can fine-tune their systems and submit checkpoints for evaluation. Hardware vendors can validate model performance across embodiments. Operators can review published artifacts directly.

The leaderboard is live at [phail.ai](https://phail.ai), alongside the full evaluation protocol.

## About Positronic Robotics

Positronic Robotics builds tools that help developers turn AI models into working robot behaviors. The company's platform lets engineers pick a model, connect it to a robot, and run real-world tasks — without having to build the robotics infrastructure from scratch.

Alongside its developer toolkit, Positronic operates PhAIL (Physical AI Leaderboard), an independent benchmark that evaluates how robotics foundation models perform on commercially relevant tasks. While many tools help train robotics models, Positronic focuses on the next step: making robots actually work in the real world.

The company is led by Sergey Arkhangelskiy, former Staff Software Engineer in Search Ranking at Google and CEO and co-founder of WANNA, the AR company acquired by Farfetch.

## About Nebius

Nebius, the AI cloud company, is building the full-stack platform for developers and companies to take charge of their AI future — from data and model training to production deployment. Founded on deep in-house technological expertise and operating at scale with a rapidly expanding global footprint, Nebius serves startups and enterprises building AI products, agents and services worldwide.

Nebius is listed on Nasdaq (NASDAQ: NBIS) and headquartered in Amsterdam.

For more information please visit [www.nebius.com](https://www.nebius.com)

**Media Contacts**
Nebius: [media@nebius.com](mailto:media@nebius.com)
