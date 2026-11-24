Title: Mimic's flux-mimic-x Leads the PhAIL DROID Board, in Half the Teleoperator's Time
Date: 2026-11-25
Category: Blog
Slug: flux-mimic-x-leads-droid
Author: Positronic Team
Image: media/flux-mimic-x-card.jpg
Header_image: no
Summary: Two new models joined the PhAIL DROID board this month. Mimic's flux-mimic-x is first, and it works faster than a human operator. Runway's Praxis-1 succeeds as often on the same tasks, at human pace. The four leading robot models are all built on video models.

This month we added two models to the [PhAIL DROID board](https://phail.ai/benchmark/droid): [Mimic flux-mimic-x](https://phail.ai/model/Mimic%20flux-mimic-x?benchmark=droid) and [Runway Praxis-1](https://phail.ai/model/Runway%20Praxis-1?benchmark=droid). The board runs each model on a real Franka arm, on everyday tasks, with a limit of 240 seconds for each episode.

<figure style="margin: 2rem 0;">
  <img src="{static}/media/flux-mimic-x-card.jpg" alt="Reliability against Speed on the PhAIL DROID board. flux-mimic-x is at the top right, faster than the human operator. Praxis-1 is close behind." style="width: 100%; height: auto; border-radius: 8px;">
</figure>

| Model | Reliability | Speed |
|---|---|---|
| <img src="{static}/media/logo-teleop.svg" alt="" style="height: 1.2em; width: 1.2em; object-fit: contain; vertical-align: middle; margin-right: 0.5em;">[Teleop (human)](https://phail.ai/model/Robot%20teleoperated%20by%20Human?benchmark=droid) | 91.5 | 1.82 |
| <img src="{static}/media/logo-mimic.png" alt="" style="height: 1.2em; width: 1.2em; object-fit: contain; vertical-align: middle; margin-right: 0.5em;">[Mimic flux-mimic-x](https://phail.ai/model/Mimic%20flux-mimic-x?benchmark=droid) | **71.7** | **2.80** |
| <img src="{static}/media/logo-nvidia.svg" alt="" style="height: 1.2em; width: 1.2em; object-fit: contain; vertical-align: middle; margin-right: 0.5em;">[NVIDIA Cosmos3 Nano](https://phail.ai/model/NVIDIA%20Cosmos3%20Nano?benchmark=droid) | 68.6 | 1.24 |
| <img src="{static}/media/logo-runway.svg" alt="" style="height: 1.2em; width: 1.2em; object-fit: contain; vertical-align: middle; margin-right: 0.5em;">[Runway Praxis-1](https://phail.ai/model/Runway%20Praxis-1?benchmark=droid) | 65.9 | 1.72 |
| <img src="{static}/media/logo-openai.svg" alt="" style="height: 1.2em; width: 1.2em; object-fit: contain; vertical-align: middle; margin-right: 0.5em;">[OpenAI GPT-6 Astra](https://phail.ai/model/OpenAI%20GPT-6%20Astra?benchmark=droid) | 64.1 | 0.45 |
| <img src="{static}/media/logo-black-forest-labs.svg" alt="" style="height: 1.2em; width: 1.2em; object-fit: contain; vertical-align: middle; margin-right: 0.5em;">[Black Forest Labs FLUX 3 Action](https://phail.ai/model/Black%20Forest%20Labs%20FLUX%203%20Action?benchmark=droid) | 63.6 | 1.59 |

Reliability is the percent of the task done within the time limit. Speed is successful tasks per minute. Within the error range of the board, flux-mimic-x shares the first rank with Cosmos3 Nano and Praxis-1.
{: .table-note }

### flux-mimic-x is faster than our human operator

flux-mimic-x has the highest Speed on the board. It is above the human who drives the same arm with a teleoperation rig. On the tasks that both ran, a success took flux-mimic-x a median of 13 seconds, and the human 29 seconds. The human still succeeds more often.

The arm also almost never waits for the model. The next actions are ready before the current ones run out, so the arm keeps moving.

<figure style="margin: 2rem 0;">
  <video controls playsinline muted preload="metadata" poster="{static}/media/droid-fork-on-plate-poster.jpg" style="width: 100%; height: auto; border-radius: 8px;">
    <source src="{static}/media/droid-fork-on-plate.mp4" type="video/mp4">
  </video>
  <figcaption>"Put the fork on the plate": flux-mimic-x and Praxis-1 on the same task, in real time.</figcaption>
</figure>

### What it is

Mimic published flux-mimic-x [as a preview](https://x.com/mimicrobotics/status/2122343940653224018) on 16 November. It is a video-action model, made with Mimic's mimic-video recipe on top of Black Forest Labs' FLUX 3 video model. Mimic trained it on no simulation data, and on no data of this robot beyond the public DROID dataset.

A video model learns how objects move before it sees a single robot action. We think this pretraining is the main reason for its speed and its reliability.

### Where it fails

The failures of flux-mimic-x cluster in four kinds of task: drawers, cloth and towels, two-step tasks, and unstacking. The rest are spread over single pick-and-place moves.

### Praxis-1: the same successes, at human pace

On the tasks that both new models ran, flux-mimic-x and Praxis-1 succeeded the same number of times. The difference is time. Praxis-1 needs about twice as long for a success, which is the pace of our human operator. It also almost never runs out of time.

<figure style="margin: 2rem 0;">
  <video controls playsinline muted preload="metadata" poster="{static}/media/droid-keys-in-bowl-poster.jpg" style="width: 100%; height: auto; border-radius: 8px;">
    <source src="{static}/media/droid-keys-in-bowl.mp4" type="video/mp4">
  </video>
  <figcaption>"Pick up the keys and put them in the bowl": both models succeed, Praxis-1 at a slower pace.</figcaption>
</figure>

Praxis-1 also has results on the two simulated Franka boards of PhAIL, [RoboLab](https://phail.ai/benchmark/robolab) and [MolmoSpaces](https://phail.ai/benchmark/molmospaces). There it is close behind FLUX 3 Action. Runway [released Praxis-1](https://runway.com/news/company-news/praxis-1-is-now-available) on 11 November as open weights, under Apache 2.0. It is a diffusion transformer that predicts video and actions together.

### The leading robot models all predict video

The four robot models at the top of the DROID board share one design. GPT-6 Astra, between them in the table, is a general AI model that controls the arm, not a robot model. [flux-mimic-x](https://x.com/mimicrobotics/status/2122343940653224018) and [FLUX 3 Action](https://huggingface.co/blog/black-forest-labs/flux-3-action) build on FLUX 3. [Praxis-1](https://runway.com/news/company-news/praxis-1-is-now-available) builds on Runway's video models. [Cosmos3 Nano](https://huggingface.co/nvidia/Cosmos3-Nano-Policy-DROID) builds on NVIDIA's Cosmos 3 world model. Each one predicts the next video frames together with the next actions.

All episodes of both new models are on the [DROID board](https://phail.ai/benchmark/droid), with video from three cameras.
