Title: Docs — Positronic Robotics
Slug: docs
Template: platform
Description: Run physical AI evaluations with Claude Code, Codex or another coding agent. Copy the prompt; the agent signs you in and submits your model.

<section class="page-head"><h1>Docs</h1><p class="hero-lede">A coding agent can run your evaluations for you. Copy the prompt below into your agent, then follow along.</p></section>

<section class="band" id="quick-start"><div class="rail"><span class="label">Quick start<a class="anchor" href="#quick-start" aria-label="Link to Quick start">#</a></span></div><div class="col"><p>Paste this prompt into Claude Code, Codex or another coding agent. The agent asks you to sign in, and you approve each purchase.</p><div class="prompt"><pre><code id="agent-prompt">{AGENT_PROMPT}</code></pre><button class="act act-ghost prompt-copy" type="button" data-copy="agent-prompt">Copy</button></div></div></section>

<section class="band" id="what-the-agent-does"><div class="rail"><span class="label">What the agent does<a class="anchor" href="#what-the-agent-does" aria-label="Link to What the agent does">#</a></span></div><div class="col"><ol class="howto"><li><span class="step-verb">1. Sign in</span><p>The agent installs the <code>positronic</code> command line tool and starts the sign-in. You sign in in your browser. The tool saves your API key on your computer.</p></li><li><span class="step-verb">2. Add credits</span><p>The agent checks your balance. You choose each purchase and pay for it yourself.</p></li><li><span class="step-verb">3. Submit</span><p>The agent pushes your policy image to a registry, submits the evaluation with <code>positronic eval run</code>, and checks its status until it ends.</p></li></ol><div class="actions docs-cta"><a class="act act-primary" href="{APP_URL}/start">Get started</a></div></div></section>

<section class="band close" id="full-guide"><div class="rail"><span class="label">Full guide<a class="anchor" href="#full-guide" aria-label="Link to Full guide">#</a></span></div><div class="col"><p>The guide to the <code>positronic</code> command line tool and its Python client is on GitHub: <a href="https://github.com/Positronic-Robotics/positronic/blob/main/client/README.md">client/README.md</a>. It covers the sign-in, credits, eval plans, the commands, their configuration and the Python client.</p></div></section>
