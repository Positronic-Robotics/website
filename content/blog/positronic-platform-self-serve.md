Title: You Don't Need a Robot to Test on a Robot
Date: 2026-12-01 14:00
Category: Blog
Slug: positronic-platform-self-serve
Author: Vladimir Yakunin
Summary: Positronic Platform is open to everyone, self-serve. Make an account, buy credits and test your robot policy on our robots, a Franka or a YAM arm, or in MolmoSpaces and RoboLab. Your coding agent can drive all of it.
Image: media/self-checkout-card.png

**tl;dr** Test your robot model on our robots. Positronic Platform is open to everyone and is self-serve: make an account, buy credits, submit your policy as a Docker image, and get video and scores back from a real robot arm or a simulator. Your coding agent can drive the whole thing.

- **Self-serve.** A student with a fresh fine-tune at 2 am, or an agent with ten checkpoints to try before lunch, can start a run alone.
- **Transparent.** The prices are public, and your account page shows each run and what it cost.
- **Fast.** You submit from the command line and follow the run there, from the queue to the scores.

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

## Your agent can do it

The [Get started](https://console.positronic.ro/start) page has a ready prompt for Claude Code, Codex or your favourite agent. The agent installs the tool, registers you, checks your balance, submits your image and checks the status until the run ends. It never sees your card: it shows you the payment link and waits while you pay. Sorry, no autonomous shopping sprees: you choose how many credits to buy.

## What it costs

A credit is $3, and you buy 4 to 1,666 at a time.

- **Real arm:** 2 credits per episode, plus 60 credits per hour of robot time, rounded up to 10 seconds. Ten one-minute episodes on the Franka cost 30 credits, $90.
- **RoboLab, your policy on our GPU:** 120 episodes at the standard time limits cost about 45.8 credits.
- **MolmoSpaces, your policy on your own server:** 320 episodes cost about 3.2 credits.

The full table is on the [pricing page](https://console.positronic.ro/pricing).

When you submit, we hold the most that the run can cost. When it ends, we charge what it used and release the rest. We do not charge for our own faults or for a recording that is not usable. We do charge for a usable run where the policy fails. Credits expire 12 months after the last time you added credits.

Scores come from automated measurement and from the review of trained people. If a score looks wrong, ask us for a review.

## Try it for free

While we ramp up, we give free welcome credits to teams that want to try the platform. This is a limited offer. Email [hi@positronic.ro](mailto:hi@positronic.ro) with your user id (your account page shows it) and what you plan to evaluate. We review each request and give welcome credits.

Questions go to our [Discord](https://discord.gg/PXvBy4NBgv).

Is your model a top model? Now you can find out today.
