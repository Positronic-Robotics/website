Title: Why every competition run now uses two simulators
Date: 2026-11-16
Category: Blog
Slug: why-two-simulators
Author: Positronic Team
Summary: A simulator can score a run as a success when the robot did not do the task. That is why every entry in the Nebius × Positronic Physical AI Competition now runs in two simulators.
Image: media/sim-success-poster.jpg
Header_image: no

Stage 1 of the Nebius × Positronic Physical AI Competition ended on 15 November. 40 teams sent an entry, and 20 of them beat every baseline model, NVIDIA's GR00T N1.7 and the Allen Institute for AI's (Ai2) MolmoAct2 included. A baseline is a public model that we run as a reference. From today, in stage 2, every entry runs in two simulators: MolmoSpaces and RoboLab. The reason: one simulator can score a run as a success when the robot did not do the task.

### What a simulator is

A simulator is a physics program that stands in for the robot and the room. Teams use simulators to test their robot models (the programs that control a robot), because a simulator is fast and cheap. Each run in a simulator ends with a score.

### What the video shows

<video controls muted playsinline preload="metadata" poster="{static}/media/sim-success-poster.jpg" style="display: block; width: 100%; max-width: 560px; height: auto; margin: 1.5rem auto; border-radius: 8px;">
  <source src="{static}/media/sim-success.mp4" type="video/mp4">
</video>

The task is "hang the mug on the rack". The simulator scored both runs as a success. In both runs, the mug is still in the robot's hand.

### How a simulator decides "success"

A simulator does not understand the task. It only checks the measurements that a person wrote into its code. For this task, the check asks two questions: is the mug at the right height, and is it near the hook? It does not ask whether the mug hangs on its own. A mug that the robot holds in the right place passes both questions.

A June 2026 [paper from the University of California, Berkeley](https://arxiv.org/abs/2606.03134) calls this a "false success": the run is recorded as a success, but the task is not done. The paper studies how to detect false successes in simulated robot runs.

### Why it matters for a leaderboard

One wrong score is a small problem. A leaderboard that ranks models by these scores has a larger problem: a model can learn to pass the check and not do the task. The more a team tunes a model to one simulator, the more the model can learn the mistakes of that simulator.

We saw this on a real robot. [On 10 November](https://competition.phail.ai/updates?utm_source=positronic.ro&utm_medium=blog&utm_campaign=competition-launch-2026-10&utm_content=company), we ran the entries of the 10 leading teams on our real robot arm, on 9 tasks that public models also ran. The teams succeeded in 3% of the runs (7 of 270). The public models succeeded in 42% (21 of 50).

Simulators are still useful. We ran six models on our real robot and in the first simulator of the competition. The real robot put 14 pairs of these models in a clear order, and the simulator put [13 of the 14 pairs](https://competition.phail.ai/rules?utm_source=positronic.ro&utm_medium=blog&utm_campaign=competition-launch-2026-10&utm_content=company) in the same order.

### What changes in stage 2

The two simulators score in different ways:

- **MolmoSpaces**, from Ai2: simulated homes, where the arm picks up objects and places them. A run counts only when the task is complete.
- **RoboLab**, from NVIDIA: other scenes and other pick-and-place tasks. It gives part credit: the share of each task that the robot completes.

The board ranks the mean of the two scores. A model that does well in both is less likely to depend on the mistakes of one.

Final entries close on 13 December. From 15 to 17 December, up to 10 teams run the same model on a real Franka arm in our lab, and the real-robot results decide the winners. Teams can follow the scores on the [competition board](https://competition.phail.ai/?utm_source=positronic.ro&utm_medium=blog&utm_campaign=competition-launch-2026-10&utm_content=company#leaderboard).

To get our next articles by email, [subscribe to our updates](#updates-form).
