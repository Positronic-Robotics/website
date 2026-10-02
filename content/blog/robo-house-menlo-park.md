Title: Is Your Model a Top Model? Talk at Robo House, Menlo Park
Date: 2026-09-28
Category: Blog
Slug: robo-house-menlo-park
Author: Vladimir Yakunin
Summary: Vladimir Yakunin gave a talk at Robo House in Menlo Park on how to tell a better robot policy from a worse one, on real hardware. Here are the slides and the main points.
Image: media/hero-droid-grid-poster.jpg

Vladimir Yakunin gave a talk at **Robo House** in Menlo Park on 28 September 2026, titled **"Is your model a top model?"** The talk asks one question: how do you tell a better robot policy from a worse one, on real hardware?

<div style="margin: 2rem 0; text-align: center;">
    <a href="/robo-house-0926/index.html" class="button" style="
        display: inline-block;
        padding: 0.8rem 1.6rem;
        background-color: var(--accent);
        color: #111;
        font-weight: 700;
        font-size: 1.2rem;
        border-radius: 8px;
        text-decoration: none;
        transition: transform 0.2s ease, opacity 0.2s ease;">
        View the Slides
    </a>
</div>

### Four traps

Most comparisons of robot models fall into one of four traps:

- **The operator and the environment change the outcome.** Run model A on Monday and model B on Tuesday, and part of the difference you measure comes from the day.
- **Different models speak different languages.** Each model expects its own inputs, action space and control rate. Two models on one robot are not a fair comparison by default.
- **One metric is not enough.** Speed, reliability and the way a model fails are three different things.
- **Ten runs do not prove anything.** A robot policy can act differently in each run, and a handful of episodes cannot separate two models.

### Four principles

Each principle answers one trap:

- **Same-session, blinded A/B.** The models run in the same rounds, in random order, and the operator does not know which model is on the robot. So the results do not drift, and the operator cannot bias them.
- **One inference API.** Every model plugs into the same interface, so every model gets the same test.
- **Full data.** Every episode is recorded in full, so any metric can be computed after the run.
- **Enough rollouts.** Enough episodes per model to tell a real difference from chance.

### On a real robot

The second half of the talk shows these principles at work on our Franka DROID rig. Five policies ran in the same blind rounds from 21 to 25 September 2026, on single-item tasks, with 37 to 39 episodes per policy.

The main chart splits every episode into stages: moving, reaching the item, in contact with it, moving it, at the target, and a scored success. For each policy it shows how many episodes reached each stage.

That view shows where a policy fails, and the policies fail in different places:

- **π0.5** reached the item in 26 of 38 episodes, and made contact in 11. Most of its episodes end before it touches the item.
- **MolmoAct2** lost 12 of 39 episodes before it reached the item, and 9 more between moving the item and getting it to the target.
- **Cosmos3 nano** lost a few episodes at each stage, and scored a success in 26 of 39.

A success rate shows only the last of these numbers. The slides give the 95% interval for every count, and follow Cosmos3 nano and GR00T N1.7 second by second through an episode.

Is your model a top model? Send us a checkpoint at [hi@positronic.ro](mailto:hi@positronic.ro) and find out.
