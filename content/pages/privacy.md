Title: Positronic Privacy Policy
Slug: privacy
Description: How Positronic uses personal data on positronic.ro and on the Positronic platform.

Version: 1.0  
Effective date: 2 November 2026

This policy tells how Positronic uses personal data when a person visits the website
<https://positronic.ro>, signs in to the Positronic platform, buys credits and runs evaluations. The
platform is the API at <https://platform.positronic.ro>, the web console at
<https://console.positronic.ro>, and the `positronic` command-line tool. The Physical AI
Competition has its own privacy policy at <https://competition.phail.ai/privacy>.

## 1. Who is responsible

The controller is Positronic Robotics Inc., a Delaware corporation, 2261 Market Street STE 10859,
San Francisco, CA 94114, United States ("**Positronic**").

Its representative in the European Union under Article 27 of the GDPR is Positronic Robotics Cyprus
Ltd, registration number HE 495939, Agias Zonis 12, Agia Zoni Center, 4th floor, Office 404, Agia
Zoni, 3027 Limassol, Cyprus.

Contact for every privacy request: hi@positronic.ro.

## 2. What data Positronic uses, why, and on what legal basis

| Data | Purpose | Legal basis (GDPR) |
| --- | --- | --- |
| **Sign-in**: the account id from WorkOS, the email address, and, for a sign-in with Google or GitHub, the name and a link to the profile picture | To identify the person and to run the account | Performance of the contract (Art. 6(1)(b)) |
| **Account**: the creation time, the organizations of the person, and the role of the person in each one | To run the account and its permissions | Performance of the contract |
| **Access**: a hash of the API key, a hash of each web session token with its expiry, and the id of the WorkOS session. Positronic does not store the API key or the session token | To check each request | Performance of the contract |
| **Acceptance of the terms**: the version that the person accepted, and when | To prove the agreement | Performance of the contract; legitimate interest in proof (Art. 6(1)(f)) |
| **Purchases and credits**: for each purchase, the organization, the member who bought, the package, the number of credits, the amount, the currency, the Stripe customer id, the Checkout session id and the status. For the balance, each hold, charge and correction, with the person who made a correction and the reason | To sell credits, to keep the balance correct, to refund, and to keep accounting records | Performance of the contract; legal obligation for accounting and tax records (Art. 6(1)(c)) |
| **Payment messages from Stripe**: the messages that Stripe sends about each payment, refund and dispute, stored as Stripe sent them. A message can hold the name, the email address, the billing address and the tax number that the payer typed in Checkout. It never holds the full card number | To confirm a payment one time, and to handle refunds, disputes and tax | Performance of the contract; legal obligation; legitimate interest in the prevention of fraud |
| **Evaluations**: the tasks, the episode counts and time limits, the container image reference and its digest, the address of a remote endpoint, the status and the scores | To run and score the evaluation that the customer asks for | Performance of the contract |
| **Secrets of an evaluation**: a registry login for a private image, and a credential for a remote endpoint | To pull the image, or to call the endpoint | Performance of the contract |
| **Policy log**: for a container image, the last 4 MiB of the log of the policy container | To let the customer find faults in its policy | Performance of the contract |
| **Recordings**: for each episode, the robot state, the camera video of the robot and its work area, the commands, the times, the scores, and the notes and labels of operators and reviewers. Each recording is linked to the organization | To score the evaluation, to show it to the customer, to make reports, and to check each charge; and, with no customer name, to improve Positronic's labeling techniques | Performance of the contract; legitimate interest in better labeling (Art. 6(1)(f)) for the last purpose |
| **Security and operation logs**: the requests to the servers, with the user id, the time and the result | To find faults and abuse, and to keep the platform safe | Legitimate interest in a safe and working platform |
| **Messages to Positronic**: emails to the support address and their answers | To answer the person | Performance of the contract; legitimate interest |
| **Website analytics**: the pages visited on positronic.ro, and one event when a visitor clicks the link to book a call or sends the contact form (section 13) | To count and understand visits, and to count how many visits lead to a contact | Consent for Google Analytics; legitimate interest for Plausible, which sets no cookies |

To use the platform, a person must give the sign-in data. To buy credits, the payer gives payment
data to Stripe. All other data comes from the use of the platform.

## 3. Data from Google, GitHub and WorkOS

The person signs in through WorkOS AuthKit, with Google, with GitHub, or with a code that
Positronic sends by email. When the person signs in with Google or GitHub, that service gives WorkOS
the data that the person approves on its consent screen. WorkOS gives Positronic the account id, the
email address, the first and the last name, and a link to the profile picture. Positronic updates
the name and the picture link at each sign-in.

Positronic uses this data only to sign the person in and to run the account. It does not use it
for advertising and does not sell it.

## 4. Payments

Stripe processes each payment on its Checkout page. The payer types the card details on that page.
Positronic does not receive or store the full card number. Stripe states that it is certified to
PCI Service Provider Level 1.

Checkout asks the payer for an email address, a name and a billing address, which the tax
calculation needs. A business can also give its tax number. Stripe can send the payer an email
receipt. Stripe processes the payment for Positronic, and it also uses payment data as a separate
controller for its own duties, such as fraud checks and the law, under the Stripe privacy policy at
<https://stripe.com/privacy>.

When Positronic makes a Stripe customer for an organization, it gives Stripe only the organization
id. For a personal organization, that id has the form `user-<number>` and holds no name.

## 5. Cookies on the console

The console at <https://console.positronic.ro> sets only the cookies that the sign-in needs:

| Cookie | Use | Duration |
| --- | --- | --- |
| `__Host-platform-signin` | Holds the state of one sign-in | 10 minutes |
| `__Host-platform-session` | Holds the session of the person | Until the browser closes, or 7 days if the person asks to stay signed in. The session itself ends after 12 hours, or after 7 days if the person asks to stay signed in |
| `__Host-platform-key-check` | Lets the page show a new API key one time | Until the page clears it |

The console loads no analytics and no advertising script.

## 6. Who receives data

Positronic does not sell personal data. Service providers process data for Positronic under a
contract, and only to give their service.

| Provider | What it does | Where |
| --- | --- | --- |
| WorkOS | Sign-in with Google, GitHub or an email code | United States |
| Stripe | Payments, tax calculation, refunds and disputes | United States |
| Nebius | Cloud compute for the platform servers and the simulators, storage of recordings, container registry, and secret storage | EU (Finland) |
| Cloudflare | Storage and delivery of reports and view pages; hosting of the website | Storage in Western Europe; delivery through Cloudflare's worldwide network |
| Axiom | Security and operation logs | EU (Germany) |
| Resend | Delivery of sign-in code emails | EU (Ireland), with records of each email in the United States |
| Slack | Internal alerts to Positronic staff, for example about a payment dispute. A billing alert names the organization, the purchase and the amount | United States |
| Google | Website analytics (section 13); storage of the leads of the website contact form in Google Workspace | United States |
| Plausible | Website analytics with no cookies (section 13) | EU |
| Contracted reviewers | Label recordings of robot evaluations, as part of the scoring, under confidentiality and data-processing terms | Outside the EU |

Positronic's own staff, and the operators who run the robots in Positronic's lab in Cyprus, see
evaluation data and recordings when their work needs it.

Positronic can disclose data where the law requires it, or to protect its rights and the safety of
people.

**Reports and view links.** When an evaluation ends, the platform can make a report and a page that
shows the recordings. Each one has a link that is hard to guess. Any person who has the link can
open the page until the link expires, 7 days after the platform makes it. The storage deletes the
files within about two more days. The customer decides who gets the link.

## 7. Transfers outside the EU

Positronic is in the United States, so personal data goes to the United States. Each transfer to a
provider outside the EU rests on the EU-US Data Privacy Framework, where the provider is certified,
or on the standard contractual clauses of the European Commission in the provider's data processing
terms. A contracted reviewer outside the EU works under the standard contractual clauses in his or
her contract. A person can ask for a copy of these safeguards at the privacy contact.

## 8. How long Positronic keeps data

| Data | Kept until |
| --- | --- |
| Account and sign-in data | The account closes. Positronic deletes it within 30 days after that, except the records in the next lines that the law requires |
| Web sessions | Their expiry. The platform deletes expired sessions |
| Registry logins for private images | The end of the evaluation. The secret store keeps a deleted secret until its purge date |
| Purchases, credit records, acceptance of the terms and payment messages | 7 years after the end of the tax year of the purchase, as accounting and tax law require |
| Evaluations, scores, recordings and policy logs | While the account is open. Positronic deletes them within 90 days after the customer asks, or after the account closes |
| Security and operation logs | 365 days. Positronic deletes them after that |
| Backups of the databases | The continuous backup keeps about one day of history. Positronic deletes the copies of the databases that it makes before each deploy after 7 days, except the two most recent copies |

## 9. Security

- The platform stores only a hash of each API key and each session token.
- The web console keeps the session in a cookie that page scripts cannot read, and sends it only over
  HTTPS to the console's own host.
- The API and the console use HTTPS.
- The platform stores registry logins and endpoint credentials in a secret store. No response or
  log of the platform holds a registry password.
- The logs that leave the servers for Axiom have the caller's IP address, secret values and view
  link tokens masked.
- Only Positronic staff, and contracted people whose work needs it, can open the databases and the
  recordings.

## 10. The rights of the person

A person can ask to access the personal data that Positronic holds about him or her, to correct it,
to delete it, to restrict its use, or to receive a copy of it. A person can object to a use that
rests on legitimate interest, and can withdraw a consent at any time. To use a right, the person
sends an email to the privacy contact in section 1, or writes to the EU representative. Positronic
answers within one month.

The platform has no button that deletes an account. Positronic deletes an account on request. It
keeps the accounting records of section 8 for the period that the law requires.

A person can complain to the data protection authority of the EU country where he or she lives or
works, or where an infringement happened.

## 11. How Positronic scores

Positronic scores each evaluation with a combination of automated measurement and human review. In a
robot evaluation, the operator who watches the robot and trained reviewers mark each episode, and
the platform measures each recording. In a simulated evaluation, the simulator checks the result of
each episode. A score measures the robot policy, not a person. Positronic makes no decision about a
person that rests only on automated processing and that has a legal or a similar significant effect
on the person.

## 12. Age

The website and the platform are for people who are at least 18 years old. Positronic does not
knowingly collect data from younger people.

## 13. The website positronic.ro

The website <https://positronic.ro> is hosted on Cloudflare Pages.

- **Google Analytics** (measurement id `G-0LV5R7LHQ3`) loads only after the visitor selects Accept
  in the consent banner. It then sets cookies. The visitor can withdraw the consent at any time with
  the Cookie settings link in the footer.
- **Plausible Analytics** counts visits with no cookies and no personal profile.
- When a visitor clicks the link to book a call, or sends the contact form, the site reports one
  event to Plausible, and to Google Analytics if the visitor accepted it. The event names the
  action (the booking link or the contact form). It holds no email address and no note.

The contact form sends the email address and the note that the visitor types to Positronic's
server. The server keeps them in a file, adds them to a Google Sheet in Positronic's Google
Workspace, and emails them to Positronic staff. Positronic keeps a lead to answer the visitor, and
deletes it when the visitor asks.

## 14. United States state privacy laws

Positronic is below the revenue and volume thresholds of the US state privacy laws, such as the
California Consumer Privacy Act. If one of them starts to apply, Positronic adds the notice that it
requires.

## 15. Changes to this policy

When Positronic changes this policy, it publishes the new version with its date. It tells the
account holders about an important change by email.
