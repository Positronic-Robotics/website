Title: Announcing Positronic Robotics
Date: 2025-09-25
Category: Blog
Slug: announcing-positronic
Author: Positronic Team
Summary: We are publicly announcing Positronic Robotics to fix the broken infrastructure of ML robotics. We're building a Python-native runtime and a data OS to make professional-grade AI robotics approachable.
Image: theme/positronic/static/img/logo.png

After several months in stealth, I’m publicly announcing **Positronic Robotics**.

I believe that **AI Robotics** – specifically end-to-end ML policies controlling robots – is going to be a huge deal. AI paves the path to truly universal machines: the same commodity hardware solving multiple tasks.

### The Reality Check

Despite all the hype, this field is much earlier than most think. We are now where self-driving was in 2015 – real potential, but years of groundwork ahead. This is the truth that very few in the industry are willing to admit publicly.

### Our Goal

Our goal at Positronic is to **make professional-grade ML robotics approachable**.

Over the last year, we trained ML policies, spoke with dozens of teams, and learned the painful truths. Teams still lack the basics:
*   Clean data pipelines
*   Scaling dataset management
*   Objective and reliable evaluation
*   Recipes for model finetuning
*   Handling inevitable distribution drift in production
*   Managing various hardware

This is what we are fixing.

### What We Are Shipping

We are shipping a few pieces I’m proud of:

1.  **Positronic Runtime (`pimm/`)**: A Python-native, immediate-mode runtime to wire sensors, controllers, inference, and GUIs without the pain of managing ROS launch files or other DSLs.
2.  **Positronic Dataset (`positronic.dataset`)**: A pragmatic dataset layer for multi-rate episodes, lazy transforms, and a web viewer for triage.
3.  **A Clean End-to-End Loop**: Collect → Inspect/Curate → Train → Validate.

### Get Involved

Check the [<svg height="16" width="16" viewBox="0 0 16 16" fill="currentColor" style="vertical-align: text-bottom; margin-right: 4px;"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path></svg>repository](https://github.com/Positronic-Robotics/positronic) and docs, kick the tires, and [<svg height="16" width="16" viewBox="0 -28.5 256 256" fill="#5865F2" style="vertical-align: text-bottom; margin-right: 4px;"><path d="M216.856339,16.5966031 C200.285002,8.84328665 182.566144,3.2084988 164.041564,0 C161.766523,4.11318106 159.108624,9.64549908 157.276099,14.0464379 C137.583995,11.0849896 118.072967,11.0849896 98.7430163,14.0464379 C96.9108417,9.64549908 94.1925838,4.11318106 91.8971895,0 C73.3526068,3.2084988 55.6133949,8.86399117 39.0420583,16.6376612 C5.61752293,67.146514 -3.4433191,116.400813 1.08711069,164.955721 C23.2560196,181.510915 44.7403634,191.567697 65.8621325,198.148576 C71.0772151,190.971126 75.7283628,183.341335 79.7352139,175.300261 C72.104019,172.400575 64.7949724,168.822202 57.8887866,164.667963 C59.7209612,163.310589 61.5131304,161.891452 63.2445898,160.431257 C105.36741,180.133187 151.134928,180.133187 192.754523,160.431257 C194.506336,161.891452 196.298154,163.310589 198.110326,164.667963 C191.183787,168.842556 183.854737,172.420929 176.223542,175.320965 C180.230393,183.341335 184.861538,190.991831 190.096624,198.16893 C211.238746,191.588051 232.743023,181.531619 254.911949,164.955721 C260.227747,108.668201 245.831087,59.8662432 216.856339,16.5966031 Z M85.4738752,135.09489 C72.8290281,135.09489 62.4592217,123.290155 62.4592217,108.914901 C62.4592217,94.5396472 72.607595,82.7145587 85.4738752,82.7145587 C98.3405064,82.7145587 108.709962,94.5189427 108.488529,108.914901 C108.508531,123.290155 98.3405064,135.09489 85.4738752,135.09489 Z M170.525237,135.09489 C157.88039,135.09489 147.510584,123.290155 147.510584,108.914901 C147.510584,94.5396472 157.658606,82.7145587 170.525237,82.7145587 C183.391518,82.7145587 193.761324,94.5189427 193.539891,108.914901 C193.539891,123.290155 183.391518,135.09489 170.525237,135.09489 Z"></path></svg>tell us what breaks](https://discord.gg/PXvBy4NBgv).

*We’re also working on something big and exciting for release in January 2026.*
