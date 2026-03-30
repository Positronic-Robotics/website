Title: Positronic – The Infrastructure Layer for Physical AI
Slug: index
Save_as: index.html
URL: index.html

### We measure how physical AI actually performs.

Every lab claims their model works. Conference demos look great. But can these models handle real commercial tasks – reliably, repeatedly, at production speed?

We built PhAIL (Physical AI Leaderboard) to answer that question. PhAIL is the first real-hardware benchmark for foundation models in robotics. We test leading VLA models on physical robots doing commercial tasks, and measure what businesses actually care about: throughput, reliability, and failure modes.

Not success rates in simulation. Real results on real hardware.

Models on the leaderboard include OpenPI 0.5 (Physical Intelligence), GR00T and DreamZero (NVIDIA), and SmolVLA (HuggingFace) – tested alongside human and teleoperated baselines.

<div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 1.2rem; margin: 3em 0;">
  <a href="https://phail.ai" class="btn-primary"
     style="display: inline-flex; flex-direction: column; align-items: center; gap: 0.3rem;
            padding: 1em 2.5em; background: rgb(177, 231, 79); color: #020617;
            text-decoration: none; border-radius: 999px; font-weight: 600; font-size: 1.1em;
            box-shadow: 0 0 0 1px rgba(17, 24, 39, 0.9), 0 10px 24px rgba(177, 231, 79, 0.35);
            transition: all 0.2s ease;">
    <span style="font-size: 1em;">View the Leaderboard</span>
    <span style="font-size: 0.82em; opacity: 0.85;">Real models. Real robots. Real metrics.</span>
  </a>
  <a href="https://github.com/Positronic-Robotics/positronic" class="btn-github"
     style="display: inline-flex; flex-direction: column; align-items: center; gap: 0.3rem;
            padding: 1em 2.5em; background: #ffffff; color: #24292f;
            text-decoration: none; border-radius: 999px; font-weight: 600; font-size: 1.1em;
            border: 1px solid rgba(27, 31, 36, 0.15);
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12), 0 8px 20px rgba(0, 0, 0, 0.08);
            transition: all 0.2s ease;">
    <span style="display: inline-flex; align-items: center; gap: 0.5rem; font-size: 1em;">
      <svg height="20" width="20" viewBox="0 0 16 16" fill="#24292f"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path></svg>
      Open Source on GitHub
    </span>
    <span style="font-size: 0.82em; opacity: 0.65;">The engine behind PhAIL.</span>
  </a>
</div>

<style>
.btn-primary:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 0 0 1px rgba(17, 24, 39, 0.9), 0 14px 32px rgba(177, 231, 79, 0.45) !important;
}
.btn-github:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15), 0 12px 28px rgba(0, 0, 0, 0.12) !important;
  background: #f6f8fa !important;
}
</style>

### The infrastructure problem

New foundation models ship every month. Each requires its own inference setup, its own data format, its own training recipe. Teams spend weeks on integration work that becomes obsolete when the next model drops.

Running OpenPI 0.5 needs 78 GB of VRAM. GR00T needs CUDA on Linux. SmolVLA runs on a consumer GPU. Getting all of them to talk to the same robot arm is its own engineering project – every single time.

**This is the problem we solve.**

### What Positronic does

Positronic is an open-source Python toolkit that handles the full lifecycle of deploying AI on real robots – from data collection through fine-tuning to production inference. One codebase, any model vendor, any hardware.

1. **Collect** – teleoperate in simulation or on hardware (phone, VR, leader arm)
2. **Train** – fine-tune on your data. Switch models without re-recording.
3. **Run** – unified inference across vendors. Same protocol, any model, any robot.
4. **Iterate** – measure what works, collect edge cases, retrain.

We built this to run PhAIL. Every model on the leaderboard goes through the same infrastructure: same data pipeline, same hardware drivers, same evaluation protocol. The codec layer translates between one canonical task representation and each model's expected format – so every model gets a fair test under identical conditions.

The same infrastructure is available for your deployment.

### The long view

Despite the hype, this field is much earlier than most think. We are where self-driving was in 2015 – real potential, but years of groundwork ahead.

The teams that deploy physical AI at scale will need more than a trained model. They will need infrastructure that doesn't break every time a better model ships: reliable evaluation, unified inference, production data pipelines. That is what we are building. PhAIL is where we prove it works.

### Get involved

- **[PhAIL is live](https://phail.ai)** – the full leaderboard, methodology, and evaluation data.
- **[Star on GitHub](https://github.com/Positronic-Robotics/positronic)** – the open-source infrastructure behind PhAIL.
- **[Join Discord](https://discord.gg/PXvBy4NBgv)** – questions, discussion, feature requests.
- Email: **[hi@positronic.ro](mailto:hi@positronic.ro)**
