Title: Docs: run your first evaluation — Positronic Robotics
Slug: docs
Template: platform
Description: How to run a robot policy evaluation on Positronic: install the command line tool, create an account, get credits, submit in a simulator or on a real robot, and read the results.

<section class="hero pf-hero"><span class="pf-kicker">Docs</span><h1>Run your first <em>evaluation</em></h1><p class="hero-lede">Run an evaluation with the positronic command line tool, or let a coding agent run it for you.</p><div class="actions pf-actions"><a class="act act-primary" href="{APP_URL}/signin">Sign up</a><a class="act act-ghost" href="/pricing">See prices</a></div></section>

<section class="band" id="agent"><div class="rail"><span class="label">Use a coding agent</span></div><div class="col"><h2>Let your agent run it</h2><p>Copy this into Claude Code, Codex or another coding agent. It asks you to sign in and to approve each purchase.</p><pre class="pf-prompt"><code>Help me evaluate my robot policy on Positronic Platform.
1. Run: uv tool install --managed-python --python 3.13 positronic. Then read the guide of the version that uv tool list shows: https://github.com/Positronic-Robotics/positronic/blob/v&lt;version&gt;/client/README.md
2. Run positronic account register in the background. Show me its sign-in line at once and wait while I sign in. Never print my API key. If it says that I have a key already, use the key saved on this computer, or ask me to set POSITRONIC_PLATFORM_API_KEY and restart you. Rotate the key only on my go.
3. Check my balance. Buy only the credits that I choose: show me checkout_url and wait while I pay. Never ask me for card details. If a purchase shows review_reason, stop and tell me. I can also ask hi@positronic.ro for welcome credits.
4. Push my policy image to a registry. Submit it with positronic eval run --org=&lt;your org&gt;, and check the status until the evaluation ends.</code></pre></div></section>

<section class="band" id="steps"><div class="rail"><span class="label">Step by step</span></div><div class="col"><h2>From install to your first run</h2><ol class="pf-steps">
<li><b>Install the command line tool.</b> You need uv 0.8.5 or later.<pre><code>uv tool install --managed-python --python 3.13 positronic</code></pre></li>
<li><b>Create your account.</b> The command prints a sign-in link. Sign in with Google, GitHub or your email. It saves your API key on this computer, and the other commands read it from there. The alias is the name that a leaderboard shows.<pre><code>positronic account register --alias=&lt;your name&gt;</code></pre>Signed in on the website before? The command keeps your key. Set <code>POSITRONIC_PLATFORM_API_KEY</code> to that key, or make a new key on your <a href="{APP_URL}/account">account page</a>.</li>
<li><b>Get credits.</b> Buy credits on your <a href="{APP_URL}/account">account page</a>. It also shows your user id and your org. To try first, email <a href="mailto:hi@positronic.ro">hi@positronic.ro</a> with your user id and what you plan to evaluate, and ask for welcome credits. You can also buy from the command line. The package <code>credits-37</code> buys 37 credits. Use a new transaction key for each purchase, for example the output of <code>uuidgen</code>, then open the link in <code>checkout_url</code> and pay in your browser.<pre><code>positronic account credits account
positronic account credits buy --package_id=credits-&lt;number&gt; \
  --transaction_key=&lt;a new key&gt;
positronic account credits get-purchase --id=&lt;purchase id&gt;</code></pre></li>
<li><b>Submit an evaluation in a simulator.</b> The catalog command lists the evaluations. Your policy runs from a Docker image in a registry. The guide <a href="https://github.com/Positronic-Robotics/positronic/blob/main/docs/submit-a-policy-image.md">Submit a policy image</a> tells what the image serves.<pre><code>positronic eval catalog
positronic eval run --eval=molmo.franka_pick_mini_smoke \
  --org=&lt;your org&gt; \
  --policy-image=docker.io/&lt;you&gt;/&lt;image&gt;@sha256:&lt;digest&gt; \
  --transaction-key=&lt;a new key&gt;</code></pre></li>
<li><b>Run on a real robot.</b> Your policy runs on your own server, and our Franka DROID setup or two-arm YAM connects to it over a secure websocket. Your server accepts only the bearer token in the file that <code>auth_token_file</code> names. The plan waits in the queue for an operator at the robot. The guide <a href="https://github.com/Positronic-Robotics/positronic/blob/main/client/README.md#eval-plans">Eval plans</a> tells every field of a plan.<pre><code># plan.yaml
rig_shape: franka
tasks:
  - &lt;a task id from positronic eval catalog&gt;
endpoints:
  - name: my-policy
    wire: websocket_tls
    address: {host: &lt;your server&gt;, port: 443, path: /api/v1/session}
    auth_token_file: ~/.config/positronic/policy-token
episodes_per_endpoint: 10
cap_per_episode_sec: 120
policy_preset: production</code></pre><pre><code>positronic eval run --from-file=plan.yaml --org=&lt;your org&gt; \
  --transaction-key=&lt;a new key&gt;</code></pre></li>
<li><b>See the results.</b> Your account page and the command line tool show each submission, its status and its charge.<pre><code>positronic eval list
positronic eval status --id=&lt;submission id&gt;</code></pre></li>
</ol><p class="pf-more"><a href="https://github.com/Positronic-Robotics/positronic/blob/main/client/README.md">Read the full command line guide</a></p></div></section>

<section class="band close"><div class="rail"><span class="label">Get started</span></div><div class="col"><h2>Test your model on our robots</h2><div class="actions pf-actions"><a class="act act-primary" href="{APP_URL}/signin">Sign up</a><a class="act act-ghost" href="/pricing">See prices</a></div><p>Questions go to our <a href="https://discord.gg/PXvBy4NBgv">Discord</a>.</p></div></section>
