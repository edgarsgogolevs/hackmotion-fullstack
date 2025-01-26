// Video handler
const video = document.getElementById("videoTutorial");
const progress = document.getElementById("videoProgress");
const staticCard = document.getElementById("staticCard");
const dynamicCard = document.getElementById("dynamicCard");
const fullCard = document.getElementById("fullCard");

video.addEventListener("play", function () {
  if (video.currentTime < 5) {
    hideAllCards();
  }
});

video.addEventListener("ended", registerVideoEvent);
async function registerVideoEvent() {
  if (!analyticsUrl) {
    await getAnalyticsUrl();
  }
  const uid = getCookie(UID_COOKIE);
  if (!uid) {
    console.error("user-id cookie not present!");
    return;
  }
  const eventName = "watched full video";
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

video.addEventListener("timeupdate", function () {
  // console.log(video.currentTime);
  const progressVal = (video.currentTime / video.duration) * 100;
  const prop = window.matchMedia(
    "(max-width: 800px)").matches ? "width" : "height";
  progress.style[prop] = progressVal + "%";

  if (video.currentTime >= 24.0) {
    if (!fullCard.classList.contains("active")) {
      staticCard.classList.remove("active");
      dynamicCard.classList.remove("active");
      fullCard.classList.add("active");
    }
  } else if (video.currentTime >= 14.0) {
    if (!dynamicCard.classList.contains("active")) {
      staticCard.classList.remove("active");
      fullCard.classList.remove("active");
      dynamicCard.classList.add("active");
    }
  } else if (video.currentTime >= 5.0) {
    if (!staticCard.classList.contains("active"))
      dynamicCard.classList.remove("active");
      fullCard.classList.remove("active");
      staticCard.classList.add("active");
  }
});

function hideAllCards() {
  document.querySelectorAll(".tutorial-card").forEach((el) => {
    el.classList.remove("active");
  });
}

function toggleCard(cardHeader) {
  const card = cardHeader.parentElement;
  card.classList.toggle("active");
}

function startNowHandler(target) {
  const video = document.getElementById("videoTutorial");
  video.scrollIntoView({ behavior: "smooth" });
  video.play();
}
