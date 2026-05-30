Title: How Do You Know If a Robot Is Getting Better?
Date: 2026-05-31
Category: Blog
Slug: measuring-robot-progress
Author: Positronic Team
Summary: Robotics measures progress with a single number — the success rate — and it never sat right with us. Our new PhAIL paper makes the case for working with distributions instead of scalars, and shows why that's the only honest way to answer the question.
Image: theme/positronic/static/img/phail-time-to-success.png

How do you know if you're making progress?

It's a question we keep coming back to. You fine-tune a new policy, you run it, the arm picks a few things out of a bin — and then what? Is it better than last week's checkpoint? Better than the model down the hall? Robotics usually answers this with a single number, the success rate, and honestly, it never sat right with us. Our new paper, [*PhAIL: A Real-Robot VLA Benchmark and Distributional Methodology*](https://arxiv.org/abs/2605.29710), is our attempt to explain why — and to do better.

### The number is built on almost nothing

Start with sample size. A lot of well-known vision-language-action papers report success rates on **10 to 25 rollouts per task**. That isn't a measurement, it's an anecdote — the difference between 47% and 53% over 20 tries is a coin flip you happened to win. If you can't tell signal from noise, you can't tell whether last month's idea actually helped, which is the one thing you needed to know.

### It's measuring half the problem

There's a deeper issue, though, and it's about what the number leaves out. Think about where robots actually have to earn their keep: a line running the same operation a thousand times a shift. There you care about *two* things, not one. Does it work, and how fast. Reliability **and** speed.

A success rate only answers the first half. A robot that slowly but perfectly picks five items and one that fast-picks five while fumbling two can post the exact same score. One of them might be worth deploying. The number can't tell them apart.

### Adding a speed number doesn't save you

The obvious fix is to report throughput too — units per hour, cycle time. But that just surfaces the real problem. Each of these is a *projection*: it squashes a model's entire behavior down to one number and throws the rest away. And different projections disagree with each other.

On our own data, the "best" model changes depending on which metric you pick. The standard success rate crowns one model; human-relative throughput crowns a second; a beat-the-human race crowns a third. Same robots, same runs, three different champions — and nobody usually tells you which projection they chose, or why.

<figure style="margin: 2rem 0; text-align: center;">
  <img src="theme/positronic/static/img/phail-uph-mtbf.png" alt="UPH versus MTBF/A tradeoff curves for four VLA models" style="max-width: 100%; height: auto; border-radius: 8px;" />
  <figcaption style="font-size: 0.9rem; opacity: 0.75; margin-top: 0.6rem;">A model isn't a point — it's a curve. As you change how long the robot is allowed to spend per item, it trades throughput (UPH) for reliability (mean time between failures or assists), and the ranking slides along with it. Any single number is just one spot you happened to stand on this curve.</figcaption>
</figure>

### So stop projecting. Work with the distribution.

If every scalar is a lossy, arguable slice, the answer is to stop taking slices. Keep the whole thing: the distribution of how long each pick takes — the time-to-success curve.

One curve carries both axes at once. How quickly it rises is speed; how high it plateaus is reliability, because the gap to the top is the failure rate. And it tells the honest story in a single glance: the human line jumps almost straight to the top, while the best model we tested is about **seven times slower** and never quite gets there.

<figure style="margin: 2rem 0; text-align: center;">
  <img src="theme/positronic/static/img/phail-time-to-success.png" alt="Time-to-success CDFs for four VLA models versus a human reference, and detection rate versus sample size" style="max-width: 100%; height: auto; border-radius: 8px;" />
  <figcaption style="font-size: 0.9rem; opacity: 0.75; margin-top: 0.6rem;">Left: time-to-success curves. The human reference snaps to the top; every VLA crawls and stalls below it. Right: comparing whole distributions (red) separates close models far faster than any single-number test (the rest), which stay stuck near the floor.</figcaption>
</figure>

### This is what lets you measure progress at all

Here's why this isn't just a prettier chart. Go back to the question we started with. "Progress" means detecting a real difference between two models — and comparing whole distributions instead of scalars finds differences a success rate can't, roughly **30 times more cheaply**. It separates close models in tens of rollouts where a success-rate test would need many hundreds. The information was always sitting in your runs; the scalar was throwing it out before you ever looked. The bottleneck was never the size of your robot farm. It was the ruler.

### And when we can't tell, we say so

The flip side of a sharper ruler is that it's honest about its limits. Our two closest models came back statistically *indistinguishable* even at our sample size — so that's what we report, instead of crowning whoever happened to win by half a point. "We can't resolve these two yet" is a real result, and a far more useful one than a fake winner. (For the record: a single swap of which side the camera sat on moved one model's completion rate by 22 points — larger than the gap we were trying to resolve in the first place. Measurement is hard, and we treat it that way: blinded, randomized, every frame auditable.)

That's what PhAIL is. Not a scoreboard built to crown a champion — our attempt to answer, honestly, *are we making progress?* We work with distributions, not scalars, because that's the only way the answer means anything.

- Read the paper: [arXiv:2605.29710](https://arxiv.org/abs/2605.29710)
- Live results and every recorded run: [phail.ai](https://phail.ai)
- Analysis pipeline and paper source: [github.com/Positronic-Robotics/phail-paper](https://github.com/Positronic-Robotics/phail-paper)
- Think your model can do better? [Submit a checkpoint](https://phail.ai/submit)
