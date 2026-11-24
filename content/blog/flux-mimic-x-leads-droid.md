Title: Mimic FLUX-mimic-x and Runway Praxis-1 Join the Top of the PhAIL DROID Board
Date: 2026-11-25
Category: Blog
Slug: flux-mimic-x-leads-droid
Author: Positronic Team
Image: media/flux-mimic-x-card.jpg
Header_image: no
Summary: Two new models joined the PhAIL DROID board today, and both share the first rank. Mimic's FLUX-mimic-x works faster than a human operator. Runway's Praxis-1 moves at human pace, and when it misses a grasp it often tries again and finishes. The four leading robot models are all built on video models.

Today we added two models to the [PhAIL DROID board](https://phail.ai/benchmark/droid): [Mimic FLUX-mimic-x](https://phail.ai/model/Mimic%20flux-mimic-x?benchmark=droid) and [Runway Praxis-1](https://phail.ai/model/Runway%20Praxis-1?benchmark=droid). The board runs each model on a real Franka arm, on everyday tasks, with a limit of 240 seconds for each episode.

<figure style="margin: 2rem 0;">
  <img src="{static}/media/flux-mimic-x-card.jpg" alt="Reliability against Speed on the PhAIL DROID board. FLUX-mimic-x and Praxis-1 are near the top. FLUX-mimic-x is faster than the human operator, and Praxis-1 is at the same speed as the human operator." style="width: 100%; height: auto; border-radius: 8px;">
</figure>

| Model | Reliability | Speed |
|---|---|---|
| <img src="{static}/media/logo-teleop.svg" alt="" style="height: 1.2em; width: 1.2em; object-fit: contain; vertical-align: middle; margin-right: 0.5em;">[Teleop (human)](https://phail.ai/model/Robot%20teleoperated%20by%20Human?benchmark=droid) | 94.7 | 1.83 |
| <img src="{static}/media/logo-mimic.png" alt="" style="height: 1.2em; width: 1.2em; object-fit: contain; vertical-align: middle; margin-right: 0.5em;">[Mimic FLUX-mimic-x](https://phail.ai/model/Mimic%20flux-mimic-x?benchmark=droid) | **71.2** | **3.08** |
| <img src="{static}/media/logo-nvidia.svg" alt="" style="height: 1.2em; width: 1.2em; object-fit: contain; vertical-align: middle; margin-right: 0.5em;">[NVIDIA Cosmos3 Nano](https://phail.ai/model/NVIDIA%20Cosmos3%20Nano?benchmark=droid) | 68.7 | 1.24 |
| <img src="{static}/media/logo-runway.svg" alt="" style="height: 1.2em; width: 1.2em; object-fit: contain; vertical-align: middle; margin-right: 0.5em;">[Runway Praxis-1](https://phail.ai/model/Runway%20Praxis-1?benchmark=droid) | 65.7 | 1.72 |
| <img src="{static}/media/logo-openai.svg" alt="" style="height: 1.2em; width: 1.2em; object-fit: contain; vertical-align: middle; margin-right: 0.5em;">[OpenAI GPT-6 Astra](https://phail.ai/model/OpenAI%20GPT-6%20Astra?benchmark=droid) | 64.1 | 0.45 |
| <img src="{static}/media/logo-black-forest-labs.svg" alt="" style="height: 1.2em; width: 1.2em; object-fit: contain; vertical-align: middle; margin-right: 0.5em;">[Black Forest Labs FLUX 3 Action](https://phail.ai/model/Black%20Forest%20Labs%20FLUX%203%20Action?benchmark=droid) | 63.7 | 1.59 |

Reliability is the percent of the task done within the time limit. Speed is successful tasks per minute. Within the error range of the board, FLUX-mimic-x, Cosmos3 Nano, Praxis-1 and GPT-6 Astra share the first rank.
{: .table-note }

### FLUX-mimic-x is faster than our human operator

FLUX-mimic-x has the highest Speed on the board. It is above the human who drives the same arm with a teleoperation rig. On the tasks that both ran, a success took FLUX-mimic-x a median of 11 seconds, and the human 27 seconds. The human still succeeds more often.

The arm also almost never waits for the model. The next actions are ready before the current ones run out, so the arm keeps moving.

<figure style="margin: 2rem 0;">
  <video controls playsinline muted preload="metadata" poster="{static}/media/droid-flux-mimic-x-fork-poster.jpg" style="width: 100%; height: auto; border-radius: 8px;">
    <source src="{static}/media/droid-flux-mimic-x-fork.mp4" type="video/mp4">
  </video>
  <figcaption>FLUX-mimic-x: "Put the fork on the plate", in real time.</figcaption>
</figure>

### What it is

Mimic published FLUX-mimic-x [as a preview](https://x.com/mimicrobotics/status/2122343940653224018) on 16 November. It is a video-action model, made with Mimic's mimic-video recipe on top of Black Forest Labs' FLUX 3 video model. Mimic trained it on no simulation data, and on no data of this robot beyond the public DROID dataset.

A video model learns how objects move before it sees a single robot action. We think this pretraining is the main reason for its speed and its reliability.

### Praxis-1: a missed grasp is not a lost task

When Praxis-1 loses its hold on an object, it tries again and often finishes the task. Of the episodes where the object slipped from the gripper, 66% still ended in a success, and 79% of these successes took less than 60 seconds.

Praxis-1 also moves at the pace of our human operator: on the same tasks, its median time to a success is the same as the human's.

<figure style="margin: 2rem 0;">
  <video controls playsinline muted preload="metadata" poster="{static}/media/droid-praxis-1-banana-plate-poster.jpg" style="width: 100%; height: auto; border-radius: 8px;">
    <source src="{static}/media/droid-praxis-1-banana-plate.mp4" type="video/mp4">
  </video>
  <figcaption>Praxis-1: "Put the banana on the plate on the left", in real time.</figcaption>
</figure>

Praxis-1 also has results on the two simulated Franka boards of PhAIL, [RoboLab](https://phail.ai/benchmark/robolab) and [MolmoSpaces](https://phail.ai/benchmark/molmospaces). Runway [released Praxis-1](https://runway.com/news/company-news/praxis-1-is-now-available) on 11 November as open weights, under Apache 2.0, so anyone can run it and train it further. It is a diffusion transformer that predicts video and actions together.

### The leading robot models all predict video

Two kinds of robot model compete today. One kind builds on a vision-language model, which learns from images and text. The other kind builds on a video model, which learns from video how objects move. A model of the second kind predicts the next video frames together with the next actions.

On the DROID board, the four leading robot models are all of the second kind. [FLUX-mimic-x](https://x.com/mimicrobotics/status/2122343940653224018) and [FLUX 3 Action](https://huggingface.co/blog/black-forest-labs/flux-3-action) build on FLUX 3. [Praxis-1](https://runway.com/news/company-news/praxis-1-is-now-available) builds on Runway's video models. [Cosmos3 Nano](https://huggingface.co/nvidia/Cosmos3-Nano-Policy-DROID) builds on NVIDIA's Cosmos 3 world model.

The robot models of the first kind are lower on the board. [π0.5](https://arxiv.org/abs/2504.16054) builds on PaliGemma, [GR00T N1.7](https://huggingface.co/nvidia/GR00T-N1.7-3B) on Cosmos-Reason2, [MolmoAct2](https://huggingface.co/allenai/MolmoAct2) on Molmo2-ER, and [G0.5](https://huggingface.co/OpenGalaxea/G05) on Qwen3.5. Each of these is a vision-language model.

NVIDIA made the same change in its own robot models. GR00T N1.7 builds on a vision-language model. [GR00T 2](https://research.nvidia.com/labs/gear/gr00t-2/), which NVIDIA introduced in November, is a world-action model: it predicts future video and robot actions together. We hope to see it on the leaderboard soon.

All episodes of both new models are on the [DROID board](https://phail.ai/benchmark/droid), with video from three cameras.
