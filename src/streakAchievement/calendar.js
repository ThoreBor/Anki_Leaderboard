const pages = document.querySelector('.pages');
const locale = window.navigator.language || 'en-us';

var data = JSON.parse(data);
var streak = data["streak"];

let today = new Date();
let newDate = new Date();
if (streak > 50) {
  newDate.setDate(newDate.getDate() - 50);
} else {
  newDate.setDate(newDate.getDate() - streak);
}
let dayNum = newDate.getDate();
let month = newDate.getMonth();
let dayName = newDate.toLocaleString(locale, { weekday: 'long' });
let monthName = newDate.toLocaleString(locale, { month: 'long' });
let year = newDate.getFullYear();
let lastPage = null;

function daysInMonth(month, year) {
  return new Date(year, month + 1, 0).getDate();
}

function getNewDate() {
  if (dayNum < daysInMonth(month, year)) {
    dayNum++;
  } else {
    dayNum = 1;
  }
  if (dayNum === 1 && month < 11) {
    month++;
  } else if (dayNum === 1 && month === 11) {
    month = 0;
  }
  if (dayNum === 1 && month === 0) {
    year++;
  }
  newDate = new Date(year, month, dayNum);
  dayName = newDate.toLocaleString('en-us', { weekday: 'long' });
  monthName = newDate.toLocaleString('en-us', { month: 'long' });
}

function updateCalendar(target) {
  if (target && target.classList.contains('page')) {
    target.classList.add('tear');
    setTimeout(() => {
      pages.removeChild(target);
    }, 800);
  } else {
    return;
  }
  renderPage();
}

function renderPage() {
  const newPage = document.createElement('div');
  newPage.classList.add('page');
  newPage.innerHTML = `
    <p class="month">${monthName}</p>
    <p class="day">${dayNum}</p>
    <p class="day-name">${dayName}</p>
    <p class="year">${year}</p>
  `;
  pages.appendChild(newPage);
  lastPage = newPage;
}

function updateText() {
  days = parseInt(streak - (today.getTime() - newDate.getTime()) / (1000 * 3600 * 24))
  document.getElementById("streak").innerHTML = `Congratulations on your ${days} day streak.<br>Keep it up!`;
}

function party() {
  setInterval(function() {
      confetti({
        particleCount: 7,
        angle: 60,
        spread: 55,
        origin: { x: 0 }
      });
      confetti({
        particleCount: 7,
        angle: 120,
        spread: 55,
        origin: { x: 1 }
      });
    }, 100)
}

renderPage();
updateText();

var timer = setInterval(function(){
  getNewDate();
  if (newDate < today) {
    updateCalendar(lastPage);
    updateText();
  } else {
    updateText();
    clearInterval(timer);
    party();
  }
}, 400)