Title: What Does a Robot Lose While It Thinks?
Date: 2026-11-17
Category: Blog
Slug: what-a-robot-loses-while-it-thinks
Author: Positronic Team
Summary: In most simulators the world waits while a robot model thinks. On a real robot it doesn't. We ran the same models both ways on RoboLab: the slowest models lose the most. Then we tested whether thinking costs more than the time it takes.

In most robot simulators, the world stops while the model thinks. The model receives a camera frame, takes its time to choose the next moves, and the simulator waits for the answer. On a real robot, nothing waits. The arm holds its last position, and the clock keeps running.

The robot models we test need between 0.2 and 1.5 seconds to plan their next moves. That is a large share of an episode, and a benchmark that pauses the world does not see it. We wanted to know what the pause hides. We ran two studies on RoboLab, NVIDIA's simulated benchmark of household tasks.

### Study 1: the same models, with and without the pause

We ran seven models on the same 120 RoboLab tasks, 3 episodes per task, in two modes. In the first mode, the simulator waits for the model. In the second mode, the clock keeps running while the model thinks, as on a real arm. The second mode is how we score every eval: on our real Franka, in the sim evals we run for customers, and on the [PhAIL RoboLab board](https://phail.ai/benchmark/robolab).

Every episode of both modes is on PhAIL, with its video. The switch at the top of the board changes the mode: [clock runs](https://phail.ai/benchmark/robolab) or [sim waits](https://phail.ai/benchmark/robolab?thinking=free).

| Model | Share of the episode the arm waits | Success, sim waits | Success, clock runs | Partial-credit change |
|---|---|---|---|---|
| Galaxea G0.5 | 45% | 20.8% (75/360) | 16.7% (60/360) | **−5.9 pts** |
| NVIDIA Cosmos3 Nano | 40% | 34.2% (123/360) | 26.4% (95/360) | **−6.7 pts** |
| Ai2 MolmoAct2 | 36% | 17.5% (63/360) | 13.9% (50/360) | **−5.8 pts** |
| FLUX 3 Action | 19% | 42.2% (152/360) | 40.3% (145/360) | −2.7 pts |
| NVIDIA GR00T N1.7 | 14% | 21.4% (77/360) | 21.9% (79/360) | +0.4 pts |
| π0.5 | 12% | 28.6% (103/360) | 26.4% (95/360) | −2.6 pts |
| OpenAI GPT-6 Astra | not measured | 48.9% (176/360) | 0.6% (2/360) | **−55.5 pts** |

Partial credit is RoboLab's own subtask score. A change in bold is larger than noise: its 95% range does not include zero.

The slow models lose, and the fast models do not. Cosmos3 Nano is one of the two slowest robot models on the board: it needs about 1.5 seconds each time it plans, so its arm stands still for 40% of every episode. It also has the largest loss of the robot models. Galaxea G0.5 waits a little longer and loses almost as much. MolmoAct2 is third on both counts. The three fast models wait 12–19% of the time, and their change is inside noise.

GPT-6 Astra shows the extreme case. It is a general AI model, not a robot model, and it controls the arm by itself. With the sim paused, it has the best score on the board. With the clock running, it succeeds in 2 episodes of 360.

<!-- Figure: success per model in both modes, against the share of time the arm waits -->

### Thinking time works like slow motion

A model that thinks with the clock running does not get confused. It makes the same moves, just later.

Take each episode recorded with the sim paused and slow it down by the share of time that model waits. The result predicts the curve of the clock-running run along the whole episode. For Cosmos3 Nano, the prediction of the final partial-credit score lands within one point of the measured score.

The gap opens in the first seconds. At 20% of the time limit, Cosmos3 Nano with the clock running has only a third of the score it has with the sim paused. After that it stays behind, and the time limit cuts off the finishes that come late.

| Cosmos3 Nano | Sim waits | Clock runs |
|---|---|---|
| Typical success comes at | 34% of the time limit | 59% of the time limit |

<!-- Figure: Cosmos3 Nano progress over the time limit, both modes, with the slow-motion prediction -->

This also tells you which tasks lose most: the ones where a late finish runs out of time. Across Cosmos3 Nano, π0.5, FLUX 3 Action and GR00T N1.7 together:

| Task group | Tasks | Successes, sim waits | Successes, clock runs | Partial-credit change |
|---|---|---|---|---|
| Long tasks (150–300 s limit) | 26 | 57 | 40 | −5.6 pts |
| Tasks with 3 or more steps | 26 | 79 | 58 | −5.4 pts |
| Short tasks (20–40 s limit) | 26 | — | — | −1.3 pts |

The ranges of these groups overlap, so this split is weaker evidence than the per-model result.

### Study 2: does stopping to think cost more than moving slowly?

Study 1 shows that thinking costs time. Does it cost anything more than time?

A robot that thinks with the clock running moves in bursts: it holds still, plays its next moves, then holds still again. Compare it with a robot that never stops but moves slower, at the same average pace. Both get through the same work in the same time. If the bursts cost something on their own, for example because the scene changes while the arm holds still, the first robot should do worse.

We tested this on Cosmos3 Nano, the robot model that loses the most in study 1. On average it thinks for 1.47 seconds per call and then plays 2.13 seconds of motion. We ran two setups at the same pace:

- **Fixed thinking.** The arm holds still for 1.47 seconds on each call, then moves at normal speed.
- **Slow motion.** The sim waits while the model thinks, and every move plays 1.69× slower. That is the same average pace with no stops.

We picked 7 RoboLab tasks where objects can move during a wait and where Cosmos3 Nano sometimes succeeds, and ran 51 episodes per task per setup, 714 episodes in total. You can watch every episode: [fixed thinking](https://app.positronic.ro/v/gTyZDa0vs7bJ_kc0XVo9aA/), [slow motion](https://app.positronic.ro/v/EPHoXzx90onrf09P8lfasw/).


| Cosmos3 Nano, 7 tasks | Fixed thinking | Slow motion |
|---|---|---|
| Successes | 181/357 (50.7%) | 186/357 (52.1%) |
| Median time to success | 28.1 s | 29.5 s |

The difference is −1.4 points, with a 95% range across tasks from −11.2 to +8.1 points. The time-to-success curves cross many times and end at almost the same place. Per task, the gaps go in both directions, and chance explains their spread:

| Task | Fixed thinking | Slow motion |
|---|---|---|
| Put a white plastic bottle in the square pail | 47/51 | 49/51 |
| Put the red BBQ sauce bottle in the crate | 47/51 | 40/51 |
| Stack the yellow block on the red block | 28/51 | 32/51 |
| Stack the white mugs | 22/51 | 26/51 |
| Put three fruits on the plate | 21/51 | 30/51 |
| Stand the jug upright | 12/51 | 7/51 |
| Put all the green fruit on the plate | 4/51 | 2/51 |

In RoboLab, a robot that stops to think does as well as a robot that moves slowly at the same pace.

<!-- Figure: time-to-success curves of the two setups -->

### Why, and what we test next

RoboLab's world is still while the robot waits. An object moves during a wait only if the arm just released it or bumped it. Nothing rolls, slides or arrives on its own. We checked MolmoSpaces too, and its scenes are static in the same way. So a robot that stops to think loses nothing that a slow robot keeps.

A real workplace is different. A conveyor keeps running, a person reaches in, a part settles after the robot lets go. That is where stopping to think should cost more than slow motion, and these two studies cannot show it. The next test needs a scene where the world moves without the robot.

For static scenes, the full cost of thinking time is the time itself, and the slowest models pay the most. A benchmark that runs the clock measures it. A benchmark that pauses the world does not.

- Every RoboLab run, in both modes: [phail.ai/benchmark/robolab](https://phail.ai/benchmark/robolab)
- Our eval code: [github.com/Positronic-Robotics/positronic](https://github.com/Positronic-Robotics/positronic)
