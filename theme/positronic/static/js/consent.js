// Google Analytics loads only after the visitor accepts it.
// A deck page has no banner and no footer: it loads analytics only on a choice made on the main site.
(function () {
  var GA_ID = 'G-0LV5R7LHQ3';
  var CHOICE_KEY = 'analytics-consent';
  var GRANTED = 'granted';
  var DENIED = 'denied';
  var host = window.location.hostname;
  var isProduction = host === 'positronic.ro' || host === 'www.positronic.ro';
  var banner = document.getElementById('consent');
  var choice = null;
  // Blocked storage reads as no choice: GA stays off and the banner asks again on each page.
  try { choice = localStorage.getItem(CHOICE_KEY); } catch (e) {}

  function loadAnalytics() {
    window['ga-disable-' + GA_ID] = false;
    if (!isProduction || window.gtag) return;
    var script = document.createElement('script');
    script.async = true;
    script.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
    document.head.appendChild(script);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', GA_ID);
  }

  // A withdrawal stops a gtag already on the page and removes the cookies it set.
  function stopAnalytics() {
    window['ga-disable-' + GA_ID] = true;
    var domains = ['', '; domain=' + host, '; domain=.' + host.replace(/^www\./, '')];
    document.cookie.split(';').forEach(function (pair) {
      var name = pair.split('=')[0].trim();
      if (name !== '_ga' && name.indexOf('_ga_') !== 0 && name !== '_gid' && name !== '_gat') return;
      domains.forEach(function (domain) {
        document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/' + domain;
      });
    });
  }

  function decide(value) {
    // Blocked storage keeps the choice for this page only; see the read above.
    try { localStorage.setItem(CHOICE_KEY, value); } catch (e) {}
    banner.hidden = true;
    if (value === GRANTED) loadAnalytics(); else stopAnalytics();
  }

  if (choice === GRANTED) loadAnalytics();

  // A choice made in another tab applies to this one too.
  window.addEventListener('storage', function (event) {
    if (event.key !== CHOICE_KEY) return;
    if (event.newValue === GRANTED) loadAnalytics(); else stopAnalytics();
    if (banner) banner.hidden = event.newValue === GRANTED || event.newValue === DENIED;
  });

  if (!banner) return;
  if (choice !== GRANTED && choice !== DENIED) banner.hidden = false;

  banner.querySelectorAll('[data-consent]').forEach(function (button) {
    button.addEventListener('click', function () { decide(button.getAttribute('data-consent')); });
  });
  document.querySelectorAll('[data-consent-open]').forEach(function (link) {
    link.addEventListener('click', function () {
      banner.hidden = false;
      banner.querySelector('[data-consent]').focus();
    });
  });
})();
