const UID_COOKIE = "user-id";
let analyticsUrl;

if (!analyticsUrl) {
  getAnalyticsUrl();
}

function getCookie(cName) {
  const name = cName + "=";
  const decodedCookie = decodeURIComponent(document.cookie);
  const ca = decodedCookie.split(";");
  for (let i = 0; i < ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) === " ") {
      c = c.substring(1);
    }
    if (c.indexOf(name) === 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

async function getAnalyticsUrl() {
  try {
    const resp = await fetch("/api/analytics");
    if (!resp.ok) {
      throw new Error("Failed to fetch analytics URL. Status: " + resp.status);
    }
    const json = await resp.json();
    analyticsUrl = json.url;
    console.log("Analytics url: " + analyticsUrl);
  } catch (error) {
    console.error(error.message);
  }
}

async function registerClickEvent(target) {
  if (!analyticsUrl) {
    await getAnalyticsUrl();
  }
  const uid = getCookie(UID_COOKIE);
  if (!uid) {
    console.error("user-id cookie not present!");
    return;
  }
  const eventName = "Clicked on #" + target.id;
  const data = getUserInfo();
  data.event = eventName;
  data.uid = uid;
  console.log(data);
  try {
    const resp = await fetch(analyticsUrl, {
      method: "POST",
      body: JSON.stringify(data),
    });
    if (!resp.ok) {
      throw new Error("Failed to fetch analytics URL. Status: " + resp.status);
    }
  } catch (error) {
    console.error(error.message);
  }
}

function getUserInfo() {
  return {
    browser: {
      userAgent: navigator.userAgent,
      language: navigator.language,
      cookiesEnabled: navigator.cookieEnabled,
      doNotTrack: navigator.doNotTrack,
      onLine: navigator.onLine,
    },

    screen: {
      width: window.screen.width,
      height: window.screen.height,
      availWidth: window.screen.availWidth,
      availHeight: window.screen.availHeight,
      colorDepth: window.screen.colorDepth,
      pixelDepth: window.screen.pixelDepth,
      orientation: window.screen.orientation?.type,
    },

    window: {
      innerWidth: window.innerWidth,
      innerHeight: window.innerHeight,
      outerWidth: window.outerWidth,
      outerHeight: window.outerHeight,
    },

    hardware: {
      deviceMemory: navigator?.deviceMemory,
      hardwareConcurrency: navigator?.hardwareConcurrency,
      maxTouchPoints: navigator?.maxTouchPoints,
    },

    connection: {
      effectiveType: navigator?.connection?.effectiveType,
      downlink: navigator?.connection?.downlink,
      rtt: navigator?.connection?.rtt,
      saveData: navigator?.connection?.saveData,
    },

    timezone: {
      timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
      timezoneOffset: new Date().getTimezoneOffset(),
    },

    features: {
      localStorage: !!window.localStorage,
      sessionStorage: !!window.sessionStorage,
      webGL: !!window.WebGLRenderingContext,
      webWorkers: !!window.Worker,
      notifications: !!window.Notification,
      geolocation: !!navigator.geolocation,
    },
  };
}
