Title: Is Your Model a Top Model? Talk at Robo House, Menlo Park
Date: 2026-09-28
Category: Blog
Slug: robo-house-menlo-park
Author: Vladimir Yakunin
Summary: A small room at Robo House in Menlo Park, and why a success rate is not enough to tell a better robot model from a worse one.
Image: media/hero-droid-grid-poster.jpg

On Monday, 28 September, I gave a short talk at Robo House in Menlo Park. Khurram Pirov runs a lecture series there for robotics engineers, researchers and people who deploy real robots. The format is simple: a small room, a talk, an open discussion, and then a BBQ.

My question for the room was: is your model a top model, and how do you know?

A success rate hides most of the answer. It tells you how often the robot finished the task. It does not tell you where it failed in all the other episodes. On a real robot, the operator, the day and the setup also move that number, so a comparison of two models run on different days measures the days too.

So we record the whole episode. For each run we check how far the robot got: did it reach the item, touch it, move it, put it at the target. On our DROID rounds the week before the talk, one policy lost most of its episodes before it touched the item. Another lost almost half of its episodes after it already had the item moving. A success rate shows only the end of both stories, and they are two different problems.

The rest is method: run the models in the same session, blind, through one inference API, with enough episodes to tell a real difference from chance. The slides have the details and the charts.

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

Thanks to Khurram for hosting. If you want to know where your model fails, send us a checkpoint at [hi@positronic.ro](mailto:hi@positronic.ro).
