let attendanceData = {}


// Function to update attendance data based on selected year and month
function updateAttendanceData() {
	fetchAttendanceData(extractAttendanceStatus);
	generateCalendar();
}


// Event listener for the year dropdown menu
const yearSelect = document.getElementById("year-select");
yearSelect.addEventListener("change", () => {
	updateAttendanceData();
});

// Event listener for the month dropdown menu
const monthSelect = document.getElementById("month-select");
monthSelect.addEventListener("change", () => {
	updateAttendanceData();
});

// Function to fetch attendance data from the server
function fetchAttendanceData(dataProcessed) {
	const year = yearSelect.value;
	const month = monthSelect.value;
	const user = document.getElementById('user-data').getAttribute('data-username');
	const apiUrl = `/api/attendance?year=${year}&username=${user}&month=${month}`;

	fetch(apiUrl)
		.then(response => response.json())
		.then(data => {
			dataProcessed(data.attendance);
			generateCalendar();
		})
		.catch(error => console.error('Error fetching data:', error));
}

// Function to extract morning_attendance and status
function extractAttendanceStatus(apiData) {
	attendanceData = {};
	apiData.forEach(item => {
		const date = item.morning_attendance;
		const status = item.status;
		attendanceData[date] = status;
	});
}





// Function to generate calendar view for a specific month
function generateCalendar() {
const calendarElement = document.getElementById("calendar");
const currentmonth = monthSelect.value;
const currentYear = yearSelect.value;


calendarElement.innerHTML = ""; // Clear previous calendar
const daysInMonth = new Date(currentYear, currentmonth, 0).getDate();
const firstDay = new Date(currentYear, currentmonth - 1, 1).getDay(); // Day of the week of the first day

// Create header row for days of the week
const daysOfWeek = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
for (let day of daysOfWeek) {
  const dayElement = document.createElement("div");
  dayElement.classList.add("calendar-header");
  dayElement.textContent = day;
  calendarElement.appendChild(dayElement);
}

// Fill in empty cells before the first day of the month
for (let i = 0; i < firstDay; i++) {
  const emptyCell = document.createElement("div");
  emptyCell.classList.add("calendar-day", "empty");
  calendarElement.appendChild(emptyCell);
}

// Fill in days of the month
for (let i = 1; i <= daysInMonth; i++) {
  const date = `${currentYear}-${currentmonth.toString().padStart(2, "0")}-${i.toString().padStart(2, "0")}`;
  const dayElement = document.createElement("div");
  dayElement.classList.add("calendar-day");

  if (attendanceData[date]) {
	dayElement.classList.add(attendanceData[date]);
  }

  dayElement.textContent = i;
  calendarElement.appendChild(dayElement);
}
}




function updatePerformance() {
	updateAttendanceData();
}

window.onload = updatePerformance;