Title: Positronic Platform Terms of Service
Slug: terms
Description: Read the terms of service of the Positronic platform: credits, evaluations, charges, refunds and liability.

Version: 1.4  
Effective date: 10 November 2026  
Last changed: 10 November 2026

## Summary

This summary is not part of the terms. It helps the customer read them.

- The customer buys credits in advance. The platform takes credits from the balance for each
  evaluation of a robot policy, in simulation or on a real robot.
- When Positronic accepts an evaluation, it holds the maximum that the evaluation can cost. When
  the evaluation ends, the platform charges what the evaluation used and releases the rest.
- The platform does not charge for a platform fault or for an invalid recording. It charges for a
  usable recording, also when the policy fails.
- Positronic scores each evaluation with automated measurement and with the review of trained
  people. The customer can ask for a review of a score.
- Credits have no cash value. All credits in the account expire 12 months after the last time credits
  were added to it. The refund
  policy says when Positronic returns money for credits that the customer did not spend. A consumer in the EU or the UK can withdraw from a purchase within
  14 days.
- The customer keeps the rights in its policy, and owns the results of its private evaluations. The
  customer can publish the results of its own evaluations.
- Positronic keeps the customer's information confidential.

## 1. The parties and these terms

1.1 **Positronic.** These terms are an agreement between the customer and Positronic Robotics Inc.,
a Delaware corporation, 2261 Market Street STE 10859, San Francisco, CA 94114, United States
("**Positronic**").

1.2 **The customer.** The "**customer**" is the person who accepts these terms, and the
organization for which that person acts. A person who acts for an organization states that he or
she has the authority to bind it. A "**consumer**" is a customer who is a natural person and who
uses the platform for purposes outside his or her trade, business or profession.

1.3 **Who may use the platform.** The customer must:

- be at least 18 years old and able to make a binding contract;
- be outside Cuba, Iran, North Korea, Syria, the Crimea region, and the so-called Donetsk and
  Luhansk People's Republics; and
- be absent from the sanctions lists of the United Nations, the United States, the European Union
  and the United Kingdom. A party on such a list must not own or control the customer.

1.4 **How the customer accepts.** The customer accepts these terms when it ticks the box that
accepts them at registration. The customer accepts them again, in the version that applies then,
when it ticks the box at each purchase of credits. Positronic records which version the customer
accepted and when.

1.5 **A signed agreement wins.** If the customer and Positronic signed a separate agreement for the
platform, that agreement wins where it differs from these terms. These terms apply to each matter
that the signed agreement does not cover.

1.6 **Other documents.** The refund policy at <https://positronic.ro/refund-policy> is part of these
terms. The privacy policy at <https://positronic.ro/privacy> tells how Positronic uses personal
data. The privacy policy is information. It is not part of these terms.

## 2. Definitions

- **Platform**: Positronic's evaluation service, with all the tools and features that Positronic
  gives through it. It includes the API at
  <https://platform.positronic.ro>, the web console at <https://console.positronic.ro>, and the
  `positronic` command-line tool and client library.
- **Organization**: the account that holds credits, purchases, evaluations and recordings.
  Registration makes one personal organization for each user.
- **Policy**: the customer's software that controls a robot. The customer gives it to the platform
  as a container image, or as an address of a server that the customer runs (a "remote endpoint").
- **Evaluation**: a run of a policy on tasks that the platform offers, in a simulator (a "simulated
  evaluation") or on a real robot in Positronic's lab (a "robot evaluation").
- **Episode**: one attempt of the policy at one task.
- **Recording**: the data of an episode: robot state, camera video, commands, times and scores.
- **Score**: the measure of an episode or an evaluation, as section 6 states.
- **Results**: all data and materials that the platform generates from the customer's evaluations,
  in any form, including recordings, scores, labels, reports, analyses, comparisons, view pages and
  exports.
- **Credit**: a prepaid unit that pays for evaluations on the platform.
- **Bought credit**: a credit that the customer paid for. A **granted credit** is a credit that
  Positronic gave at no charge.
- **Quote**: the maximum number of credits that an evaluation can use. The platform shows it
  before the customer files the evaluation.
- **Hold**: credits that the platform reserves for an accepted evaluation.
- **Settlement**: the step that charges the credits that an evaluation used and releases the rest
  of its hold.
- **Payment provider**: the third-party service that processes payments for Positronic. The
  privacy policy names it.
- **Pricing page**: the page at <https://console.positronic.ro/pricing> that shows the credit
  packages, their prices and the rates in credits.

## 3. The account

3.1 **Sign-in.** The customer signs in with a method that the platform offers, for example Google,
GitHub or a code sent by email.
The customer must give a correct email address.

3.2 **API key.** Each user gets one API key. The key gives full access to the user's organizations
on the platform. The customer keeps the key secret. The customer is responsible for every action
that its account or its key does.

3.3 **A lost or stolen key.** The customer replaces the key at once in the console. The customer
tells Positronic at the support address in section 18 if another person used it.

3.4 **Members and the spend permission.** In an organization, a member can read the balance and
quotes. Only a member with the spend permission can buy credits and file paid evaluations. The user
of a personal organization has the spend permission.

## 4. Credits

### 4.1 What a credit is

4.1.1 A credit pays for evaluations on the platform. It has no other use.

4.1.2 A credit is not money, a deposit, electronic money or a security. It has no cash value and earns
no interest. Positronic returns money for credits only as the refund policy states.

4.1.3 Credits belong to the organization that bought them. The customer cannot transfer credits to
another organization, sell them or exchange them.

### 4.2 Buy credits

4.2.1 The pricing page shows each credit package, its number of credits, its price and its currency.

4.2.2 Each price includes the VAT, GST or sales tax that applies. The tax is calculated at checkout
from the billing address, and the receipt shows it. A business customer can give its tax number at
checkout.

4.2.3 The customer pays on the checkout page of the payment provider. Positronic does not receive or
store the full card number.

4.2.4 Positronic adds the credits to the balance when the payment provider confirms the payment. The
page that the browser shows after the payment does not add credits. A cancelled, declined or
expired payment adds no credits.

4.2.5 If the payment provider confirms a payment late, Positronic adds the credits of that purchase one time.

### 4.3 What an evaluation costs

4.3.1 The pricing page states the rates in credits.

4.3.2 **Robot evaluation.** The platform charges a fee for each episode, which depends on the task,
and a rate for each minute of the recording. The platform measures the recording time from the
recorded robot and camera data, and rounds it up to the step that the pricing page states. The fee
for each episode covers setup and scene reset. The rate for each minute applies only to the
recording time, and not to setup, scene reset or wait time.

4.3.3 **Simulated evaluation.** The platform charges a fee for each start of the simulator and a rate
for each minute of simulated robot time of each episode, rounded up to the step that the pricing
page states. The fee and the rate depend on the simulator, and on whether Positronic hosts the
policy.

4.3.4 **Grants.** Positronic can grant credits at no charge, for example as a prize, a promotion, a
pilot or a welcome grant. The grant states its conditions. Granted credits expire with the other credits
in the account, as section 4.7 states. Granted credits follow these terms, have no cash value and cannot be
refunded. For a refund, Positronic counts granted credits as spent before bought credits.

### 4.4 The quote and the hold

4.4.1 The platform shows the quote before the customer files an evaluation. The quote is the maximum
cost: each episode at its time limit.

4.4.2 When Positronic accepts an evaluation, the platform holds the quote from the available balance.
The acceptance and the hold happen together. If the available balance is less than the quote, the
platform does not accept the evaluation and holds nothing.

4.4.3 The customer cannot spend held credits on other work.

4.4.4 An accepted evaluation keeps the rates that applied when Positronic accepted it. A later change
of rates does not change it.

### 4.5 Settlement

4.5.1 When an evaluation ends and the platform has all its records, the platform charges what the
evaluation used and releases the rest of the hold. The charge is never more than the hold.

4.5.2 **Robot evaluation.** The platform applies these rules to each recording:

| Recording | Charge |
| --- | --- |
| A usable recording, also when the policy failed or the operator stopped the robot for safety | The episode fee and the recording time |
| A recording that the platform discarded, or an attempt that a platform error stopped | No charge. The platform runs the episode again, within its retry limits |
| A recording with robot data that is missing, cut short or not valid | No charge |
| A recording up to 10 seconds longer than the time limit | Charged as if it stopped at the time limit |
| A recording that the platform cannot verify, or more than 10 seconds over the limit | The hold stays until Positronic reviews it |

4.5.3 **Simulated evaluation.** The platform charges the start fee and the simulated minutes of the
episodes that ran, up to the hold. It charges nothing when a platform fault ended the evaluation,
or when the evaluation never started.

4.5.4 **Cancel.** If the customer cancels an evaluation before the platform starts it, the platform
charges nothing.

4.5.5 **Records not complete.** While the platform waits for a record that it needs, the hold stays.
Positronic resolves a hold that stays too long.

4.5.6 **Repeat after a rejection.** If an operator rejects an episode, the platform can run it again.
The platform does not charge again for that repeat. If the charge of the first run was wrong,
Positronic corrects the balance.

### 4.6 Corrections

Positronic can correct an error in a balance or a charge. Each correction names the person who made
it and the reason. The customer sees the correction in the credit history of the console. A
correction cannot use held credits or make the available balance negative.

### 4.7 Expiry

4.7.1 All credits in the account expire 12 months after the last time credits were added to it: a
purchase, a grant or a correction that adds credits. All credits in the account have the same
expiry date. An expired credit leaves the balance, and Positronic does not refund it.

4.7.2 The expiry is at the same date and time, one year after the last addition. If that date does not
exist (29 February), the expiry is on 1 March.

4.7.3 Credits that a hold reserves when they expire stay in the hold. The evaluation can use them.
Settlement does not return them to the balance.

4.7.4 Up to the expiry, the customer can ask for a refund of available bought credits under the
refund policy.

### 4.8 Changes to prices and rates

4.8.1 Positronic can change the price of credit packages. A change does not change credits that the
customer already bought.

4.8.2 Positronic can change the rates in credits. A change applies to evaluations that Positronic
accepts after the change. Positronic tells the customer about an increase by email at least 30 days
before it applies. In those 30 days, the customer can ask for a refund of its available bought
credits under the refund policy.

### 4.9 Payment disputes

The customer agrees to ask Positronic first, at the support address. If the customer disputes a
payment with its bank, Positronic can stop the spend of the credits of that purchase until the
dispute closes. If the bank returns the money to the customer, Positronic removes the credits of
that purchase. If the customer spent them already, Positronic can suspend the account until the
customer pays for the credits that it used.

## 5. The customer's policy and data

5.1 **The policy stays the customer's.** The customer keeps all rights in its policy, its model and
its weights.

5.2 **Licence to run the policy.** The customer gives Positronic a non-exclusive, royalty-free
licence to copy, store and run the policy, only to do the evaluations that the customer asks for
and to keep the platform safe. Positronic gives the policy to no one else.

5.3 **Container image.** The platform pulls the image from the reference that the customer gives,
when the evaluation starts. It records the digest of the image that it pulled. It keeps no copy of
the image after the evaluation. The customer keeps the image available until the evaluation ends.
If the platform cannot pull the image, the evaluation fails.

5.4 **Private registry.** If the customer gives a registry login, the platform stores it as a secret
and uses it only to pull the image. It deletes the secret when the evaluation ends.

5.5 **Remote endpoint.** The platform sends observations to the customer's endpoint and receives
actions from it. The customer runs the endpoint and is responsible for it. If the endpoint needs a
credential, Positronic stores it as a secret and sends it only to that endpoint.

5.6 **Results.** The results of the customer's private evaluations belong to the customer. The
customer gives Positronic a licence to store, process, score and label them, to show them to the
customer, to generate further results from them for the customer, to diagnose faults, to improve
the evaluation, and, with no customer name, to improve Positronic's labeling techniques. Positronic
keeps them while the account is open, and deletes them within 90 days after the customer asks or
the account closes.

5.7 **No training.** Positronic does not use the customer's policy or its recordings to train a
robot policy, or any model that controls a robot or copies the customer's policy.

5.8 **Links to results.** The platform can make a web page that shows results. The page has a unique
address that contains a randomly generated code, and it does not require sign-in. Any person who has
the link can open the page until the link expires. A link stays valid for a limited period of at
least 7 days after the platform makes it. The customer controls who gets the link. The
expiry of a link does not limit the right of the customer to publish its results under section 8.2.

5.9 **The customer's data.** The customer puts personal data, secrets and data of other people in
its policy, its task text or its endpoint answers only where the evaluation needs it.

5.10 **Confidentiality.** The customer's "**confidential information**" is the information that the
customer gives to the platform, and the information that the platform makes from the customer's
evaluations. It includes the policy, the results, the task text, the endpoint details and the
credentials. Positronic keeps the customer's confidential information
confidential. It uses the information only to provide the platform and for the uses that section
5.6 allows. It discloses the information only to its staff, subcontractors and service providers
who need it to provide the platform and who are bound by duties of confidentiality. This section
does not apply to information that:

- is public, or becomes public, through no fault of Positronic;
- Positronic had before the customer gave it, or develops independently;
- Positronic gets lawfully from a third party that has no duty of confidentiality; or
- the law or a court requires Positronic to disclose. Positronic then tells the customer before the
  disclosure, where the law allows it, and discloses only the information that the law requires.

This section continues after the account closes.

## 6. Scores

6.1 **How Positronic scores.** Positronic scores each evaluation with a combination of automated
measurement and human review. In a robot evaluation, the operator who watches the robot and trained
reviewers mark each episode, and the platform measures each recording. In a simulated evaluation,
the simulator checks the result of each episode.

6.2 **What a score is.** A score measures the policy in the evaluation that ran. It does not
predict how the policy works in other conditions.

6.3 **Review of a score.** The customer can ask Positronic to review a score within 60 days after
the evaluation ends, at the support address. Positronic checks the recording and answers within
10 business days. If the score was wrong, Positronic corrects it, and corrects the charge where the
score changed it.

## 7. Acceptable use

7.1 The customer must not:

- use the platform for an unlawful purpose;
- submit a policy or an endpoint that contains malware, or that tries to read or change the
  simulator, the scoring, the robot software, the platform, or the data of another customer;
- try to make a robot move in a way that can hurt a person or damage the robot, the lab or its
  objects;
- try to get access that Positronic did not give, test the security of the platform without
  Positronic's written permission, or put an unusual load on it;
- avoid a hold, a quota or a limit of the platform, or use more than one account to get more of
  them;
- give the API key to a person outside the organization, or resell access to the platform without
  a written agreement with Positronic; or
- use the platform in breach of the sanctions and export rules in section 1.3.

7.2 **Safety on the real robot.** A trained operator watches each robot evaluation and can stop an
episode at any time. A stop for safety counts as an unsuccessful episode, and the platform charges
it as section 4.5 states. Positronic can refuse or stop a policy that it thinks is not safe.

## 8. Positronic's rights

8.1 Positronic and its licensors own the platform, the simulators, the task catalogue, the scoring
methods, and the tools and formats that present results. These terms give the customer a limited, non-exclusive,
non-transferable right to use the platform for its own evaluations while these terms apply.

8.2 **Publication of results.** The customer can publish, quote and share the results of its own
evaluations, for example in a paper, a blog post or a presentation. The customer must not alter
the scores or present the results in a misleading manner. The customer can state that the evaluation ran
on the Positronic platform.

8.3 The `positronic` client library and command-line tool have their own open-source licence. That
licence applies to them.

8.4 If the customer sends ideas or feedback, Positronic can use them with no duty to the customer.

## 9. Availability and changes

9.1 Positronic runs the platform with care. It does not promise that the platform is available at
all times or free of errors. Robot evaluations wait in a queue and run when an operator and a robot
are available.

9.2 Positronic can change, add or remove features, tasks and simulators. It can stop new credit
sales and new paid evaluations. If it does, accepted evaluations continue under their terms, and
the customer keeps its balance.

9.3 Positronic can stop the platform for maintenance or for safety.

## 10. Suspension and termination

10.1 **By the customer.** The customer can stop the use of the platform at any time. To close its
account, the customer sends an email from the account's email address to the support address.

10.2 **By Positronic.** Positronic can suspend or close an account, after notice where the law or
the situation allows it, if:

- the customer breaks these terms;
- the customer's use puts the platform, a robot, a person or another customer at risk;
- the law requires it; or
- Positronic stops the platform. Positronic then gives 30 days notice by email.

10.3 **Credits after termination.** If Positronic closes the account because the law requires it or
because Positronic stops the platform, it refunds the available bought credits under the refund
policy. If Positronic closes the account because the customer broke these terms or put the platform,
a robot, a person or another customer at risk, the customer loses its credits, except where mandatory
consumer law gives a refund. Positronic can deduct from any refund the amount that the customer
owes it.

10.4 Sections 4.6, 5, 6, 8, 11, 12, 13, 16 and 17 continue after termination.

## 11. Disclaimer

The platform, the simulators, the robots and the scores are provided "as is" and "as available". To
the extent that the law allows, Positronic gives no warranty of merchantability, fitness for a
purpose or non-infringement. If the customer is a consumer, this section does not limit the rights
that consumer law gives, such as the right to a service that conforms to the contract.

## 12. Limitation of liability

12.1 To the extent that the law allows, Positronic is not liable for indirect, special, incidental
or consequential damages, or for lost profits, lost data or lost work.

12.2 To the extent that the law allows, the total liability of Positronic for all claims under
these terms is limited to the greater of USD 100 and the amount that the customer paid Positronic
in the 12 months before the claim.

12.3 These terms do not limit a liability that the law does not let a party limit, such as liability
for fraud, or for death or personal injury that negligence causes. If the customer is a consumer,
12.1 and 12.2 apply only as far as consumer law allows.

## 13. Indemnity

This section does not apply to a consumer. The customer indemnifies Positronic against claims of
third parties, and the losses and reasonable costs that result from them, that come from the
customer's policy, its endpoint, or its breach of these terms.

## 14. Privacy

The privacy policy tells how Positronic collects and uses personal data on the platform.

## 15. Changes to these terms

15.1 Positronic can change these terms. It publishes each new version with its date. It tells the
customer about an important change by email at least 30 days before the change applies.

15.2 A change does not apply to an evaluation that Positronic accepted before the change.

15.3 If the customer does not accept a change, it can stop the use of the platform. In the 30 days
before the change applies, it can ask for a refund of its available bought credits under the refund
policy.

## 16. Governing law and disputes

16.1 The law of the State of Delaware governs these terms, with no regard to its conflict-of-law
rules.

16.2 A claim between a business customer and Positronic goes to individual, binding arbitration
under the Commercial Arbitration Rules of the American Arbitration Association, in English. The
place of arbitration is Wilmington, Delaware. The hearings are held by video conference, unless both
parties agree to meet in person. No claim goes ahead as a class or a representative action. Each party can still
bring a claim in a small-claims court, or ask a court for an urgent order to protect its
intellectual property or confidential data.

16.3 A consumer who lives in the United States can choose a small-claims court, or individual
arbitration under the Consumer Arbitration Rules of the American Arbitration Association, with the
hearings held by video conference.

16.4 A consumer who lives in the EU, the UK or another country whose law gives consumers that right
can bring a claim in the courts of the country where he or she lives. These terms keep each right
that the consumer has under the mandatory consumer protection law of that country.

## 17. General

17.1 These terms, the refund policy and any order form are the whole agreement about the platform.

17.2 If a court holds a section invalid, the other sections stay in force.

17.3 The customer cannot transfer these terms without Positronic's written consent. Positronic can
transfer them to an affiliate or to a buyer of its business, and tells the customer.

17.4 Neither party is liable for a delay or a failure that a cause outside its reasonable control
makes, such as a failure of a cloud provider, a power cut or a government act.

17.5 Positronic sends notices to the email address of the account. The customer sends notices to
the support address.

17.6 These terms are in English. A translation is for information only.

## 18. Contact

Positronic Robotics Inc., 2261 Market Street STE 10859, San Francisco, CA 94114, United States
Email: hi@positronic.ro
