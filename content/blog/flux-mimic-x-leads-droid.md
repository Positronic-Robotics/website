Title: Mimic's flux-mimic-x Leads the PhAIL DROID Board, in Half the Teleoperator's Time
Date: 2026-11-25
Category: Blog
Slug: flux-mimic-x-leads-droid
Author: Positronic Team
Image: media/flux-mimic-x-card.jpg
Header_image: no
Summary: Two new models joined the PhAIL DROID board this month. Mimic's flux-mimic-x is first, and it finishes its tasks in half the time a human operator takes. Runway's Praxis-1 succeeds as often on the same tasks, at human pace. All four leading robot models are built on video models.

This month we added two models to the [PhAIL DROID board](https://phail.ai/benchmark/droid): [Mimic flux-mimic-x](https://phail.ai/model/Mimic%20flux-mimic-x?benchmark=droid) and [Runway Praxis-1](https://phail.ai/model/Runway%20Praxis-1?benchmark=droid). The DROID board runs each model on a real Franka arm, on everyday tasks, with a limit of 240 seconds for each episode. flux-mimic-x ran one episode on each of 100 random tasks, and Praxis-1 one episode on each of 187, beside reference models from the earlier board.

| Model | Reliability | Speed |
|---|---|---|
| [Teleop (human)](https://phail.ai/benchmark/droid) | 91.5&nbsp;±&nbsp;3.1 | 1.82 |
| [Mimic flux-mimic-x](https://phail.ai/model/Mimic%20flux-mimic-x?benchmark=droid) | **71.7&nbsp;±&nbsp;7.4** | **2.80** |
| [NVIDIA Cosmos3 Nano](https://phail.ai/model/NVIDIA%20Cosmos3%20Nano?benchmark=droid) | 68.6&nbsp;±&nbsp;3.9 | 1.24 |
| [Runway Praxis-1](https://phail.ai/model/Runway%20Praxis-1?benchmark=droid) | 65.9&nbsp;±&nbsp;6.1 | 1.72 |
| [OpenAI GPT-6 Astra](https://phail.ai/model/OpenAI%20GPT-6%20Astra?benchmark=droid) | 64.1&nbsp;±&nbsp;5.2 | 0.45 |
| [Black Forest Labs FLUX 3 Action](https://phail.ai/model/Black%20Forest%20Labs%20FLUX%203%20Action?benchmark=droid) | 63.6&nbsp;±&nbsp;4.0 | 1.59 |

Reliability is the percent of the task done within the time limit. Speed is successful tasks per minute. The ± value is the 95% range. flux-mimic-x shares the first rank with Cosmos3 Nano and Praxis-1, because chance can explain the gaps between them.
{: .table-note }

### flux-mimic-x is faster than our human operator

flux-mimic-x completes 2.80 tasks per minute. That is the highest Speed on the board, above the 1.82 of a human who drives the same arm with a teleoperation rig.

On the 96 tasks that both ran, flux-mimic-x needed a median of 13 seconds for a success. The human needed 29 seconds. 51 of its 71 successes took less than 20 seconds. The human still succeeds more often: 83 of those 96 tasks, against 68 for flux-mimic-x.

The model also keeps the arm moving. In its 100 episodes, the arm stopped to wait for the next actions only 2 times, for 2.3 seconds out of 3,885 seconds of motion. A request for the next actions took a median of 252 milliseconds.

### What it is

Mimic published flux-mimic-x [as a preview](https://x.com/mimicrobotics/status/2122343940653224018) on 16 November. It is a 7B video-action model, made with Mimic's updated mimic-video recipe on top of Black Forest Labs' FLUX 3 video model. Mimic trained it on no simulation data, and on no data of this robot beyond the public DROID dataset. Mimic says its earlier model, [FLUX-mimic](https://www.mimicrobotics.com/), learns a factory task from about 30 minutes of demonstrations.

A video model learns how objects move before it sees a single robot action. We think this pretraining is the main reason for its speed and its reliability.

### Where it fails

flux-mimic-x did not succeed on 29 of its 100 tasks. The failures group in four kinds of task: drawers (4 tasks), cloth and towels (4), two-step tasks such as "spoon in the cup, then on the table" (3), and unstacking (2). Every episode is on PhAIL, with its video.

### Praxis-1: the same successes, at human pace

On the 73 tasks that both new models ran, flux-mimic-x and Praxis-1 succeeded the same number of times: 52 each. The difference is time. flux-mimic-x needed a median of 13 seconds for a success, and Praxis-1 needed 26 seconds.

Praxis-1 moves at the pace of our human operator. On the same 187 tasks, its median time to a success is 24.9 seconds, and the human's is 24.8 seconds. It also almost never stalls. Only 5 of its 187 episodes ran out of time, against 12 of 100 for flux-mimic-x.

Praxis-1 also has results on the two simulated Franka boards of PhAIL, where flux-mimic-x has none yet. It scores 51.8 on [RoboLab](https://phail.ai/benchmark/robolab) and 41.9 on [MolmoSpaces](https://phail.ai/benchmark/molmospaces), close behind FLUX 3 Action in both. Runway [released Praxis-1](https://runway.com/news/company-news/praxis-1-is-now-available) on 12 November as open weights, under Apache 2.0. It is a 27B diffusion transformer that predicts video and actions together.

### The leading robot models all predict video

The four robot models at the top of the DROID board share one design. [flux-mimic-x](https://x.com/mimicrobotics/status/2122343940653224018) and [FLUX 3 Action](https://huggingface.co/blog/black-forest-labs/flux-3-action) build on FLUX 3. [Praxis-1](https://runway.com/news/company-news/praxis-1-is-now-available) builds on Runway's video models. [Cosmos3 Nano](https://huggingface.co/nvidia/Cosmos3-Nano-Policy-DROID) builds on NVIDIA's Cosmos 3 world model. Each one predicts the next video frames together with the next actions.

They hold the first four places among the robot models, and the fastest of them is faster than a human with a teleop rig.

All episodes of both new models are on the [DROID board](https://phail.ai/benchmark/droid), with video from three cameras.
