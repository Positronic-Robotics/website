// The visitor's first and last arrival on this site, kept in their own browser and sent only with a form.
// The same rule runs on phail.ai and competition.phail.ai: a link tag or another site's referrer is an arrival;
// a direct view replaces nothing. window.positronicArrival.fields() gives the flat fields a form posts.
(function () {
  var KEY = "positronic-arrival";
  var FIRST_TOUCH_DAYS = 90;
  var TAGS = ["utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term"];
  // A sign-in redirect is not where a visitor came from.
  var SIGN_IN_HOSTS = ["workos.com", "authkit.app", "accounts.google.com"];

  function cut(value, max) {
    return (value || "").slice(0, max);
  }

  function hostOf(url) {
    try {
      return new URL(url).host;
    } catch (e) {
      return "";
    }
  }

  function isSignInHost(host) {
    return SIGN_IN_HOSTS.some(function (h) {
      return host === h || host.slice(-(h.length + 1)) === "." + h;
    });
  }

  // This view as a touch, and whether it is an arrival (a tag, or a referrer on another host).
  function thisView() {
    var params = new URLSearchParams(window.location.search);
    var touch = {};
    var tagged = false;
    TAGS.forEach(function (tag) {
      touch[tag] = cut(params.get(tag), 200);
      if (touch[tag]) tagged = true;
    });
    var refHost = hostOf(document.referrer);
    var referred = refHost !== "" && refHost !== window.location.host && !isSignInHost(refHost);
    touch.referrer = referred ? cut(document.referrer, 500) : "";
    touch.landing_page = cut(window.location.pathname, 200);
    touch.at = new Date().toISOString();
    return { touch: touch, arrival: tagged || referred };
  }

  function expired(touch) {
    var at = Date.parse(touch && touch.at);
    return !(at > Date.now() - FIRST_TOUCH_DAYS * 864e5);
  }

  function update(stored, view) {
    if (!stored || !stored.first || !stored.last || expired(stored.first)) {
      return { first: view.touch, last: view.touch };
    }
    return { first: stored.first, last: view.arrival ? view.touch : stored.last };
  }

  var stored = null;
  // Blocked storage keeps this view in memory, so a form on the landing page still sends it.
  try {
    stored = JSON.parse(localStorage.getItem(KEY) || "null");
  } catch (e) {
    console.warn("the stored arrival was not read", e);
  }
  var state = update(stored, thisView());
  try {
    localStorage.setItem(KEY, JSON.stringify(state));
  } catch (e) {
    console.warn("the arrival was not stored", e);
  }

  function source(touch) {
    return touch.utm_source || hostOf(touch.referrer) || "direct";
  }

  window.positronicArrival = {
    fields: function () {
      var out = {};
      ["first", "last"].forEach(function (which) {
        var touch = state[which];
        TAGS.concat(["referrer", "landing_page", "at"]).forEach(function (field) {
          out[which + "_" + field] = touch[field] || "";
        });
      });
      return out;
    },
    // Each arrival as one source: its utm_source, else its referrer's host, else "direct".
    sources: function () {
      return { first_source: source(state.first), last_source: source(state.last) };
    },
  };
})();
