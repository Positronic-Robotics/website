Title: You Don't Need a Robot to Test on a Robot
Date: 2026-12-08 14:00
Category: Blog
Slug: positronic-platform-self-serve
Author: Vladimir Yakunin
Summary: Positronic Platform is open to everyone, self-serve. Test your robot policy on our Franka and YAM arms, or in MolmoSpaces and RoboLab, and get fully labelled rollout data back. Your coding agent can run the whole loop.
Image: media/self-checkout-card.png

<video controls playsinline preload="metadata" poster="{static}/media/self-checkout-video-poster.jpg" style="width: 100%; height: auto; border-radius: 8px;">
  <source src="{static}/media/self-checkout-video.mp4" type="video/mp4">
</video>

**tl;dr** Test your robot model on our robots. Positronic Platform is open to everyone and is self-serve: make an account, buy credits, submit your policy as a Docker image, and get fully labelled rollout data back from a real robot arm or a simulator. Your coding agent can run the whole loop.

- **Self-serve.** A student with a fresh fine-tune at 2 am, or an agent with ten checkpoints to try before lunch, can start a run alone.
- **No human in the loop.** Your agent submits a checkpoint, reads the results, changes the model and submits again. Nobody has to watch a robot. You focus on research, and we handle the rest.
- **Full data, not only a score.** Each run returns the video, every sensor, every command and the task progress step by step.

**Limited offer while we ramp up:** ask for free welcome credits (see "Try it for free" below).

## What you can run

- **Real arms:** a Franka FR3 in the DROID setup (an arm, a gripper and three cameras) in our lab in Cyprus, and a YAM.
- **Simulators:** Ai2 MolmoSpaces and NVIDIA RoboLab. Your policy runs on our GPU, or on your own server and we call it.
- `positronic eval catalog` lists every evaluation you can submit.

The clock keeps running while your model thinks, in the simulators too. Speed matters, just like it does on the real robot.

## How it works

```
uv tool install --managed-python --python 3.13 positronic
positronic account register --alias=<your name>
positronic account credits buy --package_id=credits-30 --transaction_key=<key>
positronic eval catalog
positronic eval run --eval=<eval> --org=<your org> \
  --policy-image=docker.io/<you>/<image>@sha256:<digest> --transaction-key=<key>
positronic eval status --id=<submission id>
```

- You sign in with Google, GitHub or email. `register` saves your API key on your machine.
- Your policy is a Docker image, pinned by its digest. If you entered the [Physical AI Competition](https://competition.phail.ai), this is the same shape.
- `buy` prints a payment link, and you pay in your browser. Run it again with the same transaction key and you get the same purchase, not a second one. `eval run` works the same way.
- The account page on [console.positronic.ro](https://console.positronic.ro/account) shows each submission, its status and its charge.

## Let your agent iterate

The [Get started](https://console.positronic.ro/start) page has a ready prompt for Claude Code, Codex or your favourite agent. The agent installs the tool, registers you, checks your balance, submits your image and checks the status until the run ends.

Then ask it to improve your model. It reads the rollout data of each run, changes the model, and submits the next checkpoint, on the real robot or in simulation. You do not need to watch a robot. You get the results when the loop ends.

The agent never sees your card: it shows you the payment link and waits while you pay. Sorry, no autonomous shopping sprees: you choose how many credits to buy, and the agent spends them.

## What it costs

A credit is $3, and you buy 4 to 1,666 at a time. Some examples:

| Run | Credits | Price |
|---|---|---|
| 10 one-minute episodes on the Franka DROID setup | 30 | $90 |
| 4 two-minute episodes on YAM | 16 | $48 |
| 120 RoboLab episodes, your policy on our GPU | about 46 | about $138 |
| 320 MolmoSpaces episodes, your policy on your own server | about 3.2 | about $10 |

The rates and the full table are on the [pricing page](https://console.positronic.ro/pricing).

When you submit, we hold the most that the run can cost. When it ends, we charge what it used and release the rest. If a run fails because of us, you pay nothing. If your policy fails, you still get the full data, and you pay for the run. Credits expire 12 months after the last time you added credits.

Scores come from automated measurement and from the review of trained people. If a score looks wrong, ask us for a review.

## Try it for free

While we ramp up, we give free welcome credits to teams that want to try the platform. This is a limited offer. Email [hi@positronic.ro](mailto:hi@positronic.ro) with your user id (your account page shows it) and what you plan to evaluate. We review each request and give welcome credits.

Questions go to our [Discord](https://discord.gg/PXvBy4NBgv).

Is your model a top model? Now you can find out today.
