Title: What Does a Robot Lose While It Thinks?
Date: 2026-11-17
Category: Blog
Slug: what-a-robot-loses-while-it-thinks
Author: Positronic Team
Image: media/thinking-time-two-clocks.jpg
Header_image: no
Summary: In most simulators the world waits while a robot model thinks. On a real robot it doesn't. We ran the same models both ways on RoboLab: the slowest models lose the most. Then we tested whether thinking costs more than the time it takes.

In most robot simulators, the world stops while the model thinks. The model receives a camera frame, takes its time to choose the next moves, and the simulator waits for the answer. On a real robot, nothing waits. The arm holds its last position, and the clock keeps running.

<figure style="margin: 2rem auto; max-width: 600px;">
  <img src="{static}/media/thinking-time-two-clocks.jpg" alt="In simulation the clock stops while the model thinks. On a real robot the arm waits and the clock keeps running, so the same motion takes more time." style="width: 100%; height: auto; border-radius: 8px;" />
</figure>

The robot models we test need between 0.2 and 1.5 seconds to plan their next moves. That is a large share of an episode, and a benchmark that pauses the world does not see it. We wanted to know what the pause hides. We ran two studies on [RoboLab](https://research.nvidia.com/labs/srl/projects/robolab), NVIDIA's simulated benchmark of household tasks.

### Study 1: the same models, with and without the pause

We ran seven models on the same 120 RoboLab tasks, 3 episodes per task, in two modes. In the first mode, the simulator waits for the model. In the second mode, the clock keeps running while the model thinks, as on a real arm. The second mode is how we score every eval: on [our real Franka](https://phail.ai/benchmark/droid), in [the sim evals we run for customers](https://positronic.ro/labs), and on the [PhAIL RoboLab board](https://phail.ai/benchmark/robolab).

Every episode of both modes is on PhAIL, with its video. The switch at the top of the board changes the mode: [clock runs](https://phail.ai/benchmark/robolab) or [sim waits](https://phail.ai/benchmark/robolab?thinking=free).

| Model | Arm waits | Success, sim waits | Success, clock runs | Change |
|---|---|---|---|---|
| [Galaxea G0.5](https://phail.ai/model/Galaxea%20G0.5?benchmark=robolab) | 45% | [20.8%](https://phail.ai/benchmark/robolab?thinking=free) | [16.7%](https://phail.ai/benchmark/robolab) | **−4.2&nbsp;±&nbsp;3.2%** |
| [NVIDIA Cosmos3 Nano](https://phail.ai/model/NVIDIA%20Cosmos3%20Nano?benchmark=robolab) | 40% | [34.2%](https://phail.ai/benchmark/robolab?thinking=free) | [26.4%](https://phail.ai/benchmark/robolab) | **−7.8&nbsp;±&nbsp;4.6%** |
| [Ai2 MolmoAct2](https://phail.ai/model/Ai2%20MolmoAct2?benchmark=robolab) | 36% | [17.5%](https://phail.ai/benchmark/robolab?thinking=free) | [13.9%](https://phail.ai/benchmark/robolab) | −3.6&nbsp;±&nbsp;4.6% |
| [FLUX 3 Action](https://phail.ai/model/Black%20Forest%20Labs%20FLUX%203%20Action?benchmark=robolab) | 19% | [42.2%](https://phail.ai/benchmark/robolab?thinking=free) | [40.3%](https://phail.ai/benchmark/robolab) | −1.9&nbsp;±&nbsp;4.4% |
| [NVIDIA GR00T N1.7](https://phail.ai/model/NVIDIA%20GR00T?benchmark=robolab) | 14% | [21.4%](https://phail.ai/benchmark/robolab?thinking=free) | [21.9%](https://phail.ai/benchmark/robolab) | +0.6&nbsp;±&nbsp;4.0% |
| [π0.5](https://phail.ai/model/Physical%20Intelligence%20%CF%80%E2%82%80.%E2%82%85?benchmark=robolab) | 12% | [28.6%](https://phail.ai/benchmark/robolab?thinking=free) | [26.4%](https://phail.ai/benchmark/robolab) | −2.2&nbsp;±&nbsp;4.0% |
| [OpenAI GPT-6 Astra](https://phail.ai/model/OpenAI%20GPT-6%20Astra?benchmark=robolab) | not measured | [48.9%](https://phail.ai/benchmark/robolab?thinking=free) | [0.6%](https://phail.ai/benchmark/robolab) | **−48.3&nbsp;±&nbsp;6.9%** |

"Arm waits" is the share of the episode in which the arm stands still while the model thinks. The ± value is the 95% range. A change in bold is larger than noise: its range does not include zero.
{: .table-note }

Unsurprisingly, the slow models lose and the fast ones barely change. [Cosmos3 Nano](https://phail.ai/model/NVIDIA%20Cosmos3%20Nano?benchmark=robolab) is one of the two slowest robot models on the board: it needs about 1.5 seconds each time it plans, so its arm stands still for 40% of every episode. It also has the largest loss of the robot models. [Galaxea G0.5](https://phail.ai/model/Galaxea%20G0.5?benchmark=robolab) waits a little longer and also loses more than noise. [MolmoAct2](https://phail.ai/model/Ai2%20MolmoAct2?benchmark=robolab) is third on both counts, and its loss is at the edge of noise. The three fast models wait 12–19% of the time, and their change is inside noise.

[GPT-6 Astra](https://phail.ai/model/OpenAI%20GPT-6%20Astra?benchmark=robolab) shows the extreme case. It is a general AI model, not a robot model, and it controls the arm by itself. With the sim paused, it has the best score on the board. With the clock running, it almost never succeeds.

<figure style="margin: 2rem auto; max-width: 600px;">
  <img src="{static}/media/thinking-time-change-vs-wait.png" alt="Change in success rate against the share of each episode the arm waits, for six robot models. Cosmos3 Nano and Galaxea G0.5 wait longest and lose more than noise." style="width: 100%; height: auto; border-radius: 8px;" />
</figure>

### Thinking time works like slow motion

A model that thinks with the clock running does not get confused. It makes the same moves, just later.

<figure style="margin: 2rem 0;">
  <video controls playsinline muted preload="metadata" poster="{static}/media/thinking-time-onion-poster.jpg" style="width: 100%; height: auto; border-radius: 8px;">
    <source src="{static}/media/thinking-time-onion.mp4" type="video/mp4">
  </video>
</figure>

Take each episode recorded with the sim paused and slow it down by the share of time that model waits. The result predicts the curve of the clock-running run along the whole episode. For Cosmos3 Nano, the prediction of the final partial-credit score lands within one point of the measured score.

The gap opens in the first seconds. At 20% of the time limit, Cosmos3 Nano with the clock running has only a third of the score it has with the sim paused. After that it stays behind, and the time limit cuts off the finishes that come late.

| Cosmos3 Nano | Sim waits | Clock runs |
|---|---|---|
| [Typical success]({filename}/blog/measuring-robot-progress.md) comes at | 34% of the time limit | 59% of the time limit |

<figure style="margin: 2rem auto; max-width: 600px;">
  <img src="{static}/media/thinking-time-cosmos-over-time.jpg" alt="Cosmos3 Nano success rate over the time limit. With the sim paused it reaches 34%. With the clock running it falls behind in the first seconds and ends at 26%." style="width: 100%; height: auto; border-radius: 8px;" />
</figure>

### Study 2: does stopping to think cost more than moving slowly?

Study 1 shows that thinking costs time. Does it cost anything more than time?

A robot that thinks with the clock running moves in bursts: it holds still, plays its next moves, then holds still again. Compare it with a robot that never stops but moves slower, at the same average pace. Both get through the same work in the same time. If the bursts cost something on their own, for example because the scene changes while the arm holds still, the first robot should do worse.

We tested this on Cosmos3 Nano, the robot model that loses the most in study 1. On average it thinks for 1.47 seconds per call and then plays 2.13 seconds of motion. We ran two setups at the same pace:

- **Fixed thinking.** The arm holds still for 1.47 seconds on each call, then moves at normal speed.
- **Slow motion.** The sim waits while the model thinks, and every move plays 1.69× slower. That is the same average pace with no stops.

We picked 7 RoboLab tasks where objects can move during a wait and where Cosmos3 Nano sometimes succeeds, and ran 51 episodes per task per setup, 714 episodes in total. Each number in the tables below opens the replays of its episodes.

| Cosmos3 Nano, 7 tasks | [Fixed thinking](https://app.positronic.ro/v/gTyZDa0vs7bJ_kc0XVo9aA/) | [Slow motion](https://app.positronic.ro/v/EPHoXzx90onrf09P8lfasw/) | Change |
|---|---|---|---|
| Success | [50.7%](https://app.positronic.ro/v/gTyZDa0vs7bJ_kc0XVo9aA/) | [52.1%](https://app.positronic.ro/v/EPHoXzx90onrf09P8lfasw/) | −1.4&nbsp;±&nbsp;9.7% |
| Median time to success | 28.1 s | 29.5 s | |

The [time-to-success]({filename}/blog/measuring-robot-progress.md) curves cross many times and end at almost the same place. Per task, the gaps go in both directions, and chance explains their spread:

| Task | Fixed thinking | Slow motion | Change |
|---|---|---|---|
| Put a white plastic bottle in the square pail | [92%](https://app.positronic.ro/v/gTyZDa0vs7bJ_kc0XVo9aA/?task=Put+any+white+plastic+bottle+in+the+square+pail) | [96%](https://app.positronic.ro/v/EPHoXzx90onrf09P8lfasw/?task=Put+any+white+plastic+bottle+in+the+square+pail) | −4&nbsp;±&nbsp;9% |
| Put the red BBQ sauce bottle in the crate | [92%](https://app.positronic.ro/v/gTyZDa0vs7bJ_kc0XVo9aA/?task=Put+the+red+bbq+sauce+bottle+in+the+crate) | [78%](https://app.positronic.ro/v/EPHoXzx90onrf09P8lfasw/?task=Put+the+red+bbq+sauce+bottle+in+the+crate) | +14&nbsp;±&nbsp;13% |
| Stack the yellow block on the red block | [55%](https://app.positronic.ro/v/gTyZDa0vs7bJ_kc0XVo9aA/?task=Stack+the+yellow+block+on+the+red+block) | [63%](https://app.positronic.ro/v/EPHoXzx90onrf09P8lfasw/?task=Stack+the+yellow+block+on+the+red+block) | −8&nbsp;±&nbsp;19% |
| Stack the white mugs | [43%](https://app.positronic.ro/v/gTyZDa0vs7bJ_kc0XVo9aA/?task=Stack+the+white+mugs+on+top+of+each+other.) | [51%](https://app.positronic.ro/v/EPHoXzx90onrf09P8lfasw/?task=Stack+the+white+mugs+on+top+of+each+other.) | −8&nbsp;±&nbsp;19% |
| Put three fruits on the plate | [41%](https://app.positronic.ro/v/gTyZDa0vs7bJ_kc0XVo9aA/?task=Put+three+%283%29+fruits+on+the+plate) | [59%](https://app.positronic.ro/v/EPHoXzx90onrf09P8lfasw/?task=Put+three+%283%29+fruits+on+the+plate) | −18&nbsp;±&nbsp;19% |
| Stand the jug upright | [24%](https://app.positronic.ro/v/gTyZDa0vs7bJ_kc0XVo9aA/?task=Stand+the+jug+upright) | [14%](https://app.positronic.ro/v/EPHoXzx90onrf09P8lfasw/?task=Stand+the+jug+upright) | +10&nbsp;±&nbsp;15% |
| Put all the green fruit on the plate | [8%](https://app.positronic.ro/v/gTyZDa0vs7bJ_kc0XVo9aA/?task=Put+all+the+green+fruit+on+the+plate) | [4%](https://app.positronic.ro/v/EPHoXzx90onrf09P8lfasw/?task=Put+all+the+green+fruit+on+the+plate) | +4&nbsp;±&nbsp;9% |

In RoboLab, a robot that stops to think does as well as a robot that moves slowly at the same pace.

<!-- Figure: time-to-success curves of the two setups -->

### Why, and what we test next

RoboLab's world is still while the robot waits. An object moves during a wait only if the arm just released it or bumped it. Nothing rolls, slides or arrives on its own. We checked [MolmoSpaces](https://github.com/allenai/molmospaces) too ([its board](https://phail.ai/benchmark/molmospaces)), and its scenes are static in the same way. So a robot that stops to think loses nothing that a slow robot keeps.

A real workplace is different. A conveyor keeps running, a person reaches in, a part settles after the robot lets go. That is where stopping to think should cost more than slow motion, and these two studies cannot show it. The next test needs a scene where the world moves without the robot.

For static scenes, the full cost of thinking time is the time itself, and the slowest models pay the most. A benchmark that runs the clock measures it. A benchmark that pauses the world does not.

- Every RoboLab run, in both modes: [phail.ai/benchmark/robolab](https://phail.ai/benchmark/robolab)
- Our eval code: [github.com/Positronic-Robotics/positronic](https://github.com/Positronic-Robotics/positronic)
