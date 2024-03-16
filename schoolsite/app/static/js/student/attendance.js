let tableAttendanceData = [];
let attendanceData = {};
let presentCount = 0;
let	absentCount = 0;
let lateCount = 0;
let chart


// Function to update attendance data based on selected year and month
function updateAttendanceData() {
	fetchAttendanceData(extractAttendanceStatus);
	generateCalendar();
}


// Event listener for the year dropdown menu
const yearSelect = document.getElementById("year-select");
yearSelect.addEventListener("change", () => {
	updateAttendanceData();
	updateAttendanceCounts();
	renderAttendanceTable(tableAttendanceData);
	generateDonutChart();
});

// Event listener for the month dropdown menu
const monthSelect = document.getElementById("month-select");
monthSelect.addEventListener("change", () => {
	updateAttendanceData();
	 updateAttendanceCounts();
	renderAttendanceTable(tableAttendanceData);
	generateDonutChart();
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
			updateAttendanceCounts();
			renderAttendanceTable(tableAttendanceData);
			generateDonutChart();
		})
		.catch(error => console.error('Error fetching data:', error));
}

// Function to extract morning_attendance and status
function extractAttendanceStatus(apiData) {
	tableAttendanceData = [];
	attendanceData = {};
	presentCount = 0;
	absentCount = 0;
	lateCount = 0;
	apiData.forEach(item => {
		const morning = item.morning_attendance;
		const evening = item.evening_attendance;
		const status = item.status;
		const comment = item.comment;
		const late = item.late_arrival;
		const date = item.date;
		attendanceData[date] = status;
		tableAttendanceData.push([date, morning, status, evening, late, comment]);

		if (status === 'present') {
			presentCount++;
		} else if (status === 'absent') {
			absentCount++;
		}else if (status === 'late'){
			lateCount++;
			presentCount++;
		}
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



//Function return number of present, absent and late students
function updateAttendanceCounts() {
	const presentCountElement = document.getElementById('presentCountElement');
	const absentCountElement = document.getElementById('absentCountElement');
	const lateCountElement = document.getElementById('lateCountElement');

	presentCountElement.innerText = presentCount;
	absentCountElement.innerText = absentCount;
	lateCountElement.innerText = lateCount;
}
//end of attendance count


function renderAttendanceTable(tableAttendanceData) {
	const tableBody = document.getElementById('attendanceTableBody');


	tableBody.innerHTML = '';
	tableAttendanceData.forEach(item => {
		const [date, morning, status, evening, late, comment] = item;

		const row = document.createElement('tr');
		const cellContents = [date, morning, status, evening, late, comment];

		cellContents.forEach(content => {
			const cell = document.createElement('td');
			cell.textContent = content;
			row.appendChild(cell);
		});

		tableBody.appendChild(row);
	});
}




// Function to generate donut chart
function generateDonutChart() {
	//console.log(presentCount,absentCount,lateCount)
	var ctx = document.getElementById('donutChart').getContext('2d');
	let data = {
		type: 'doughnut',
		data: {
			labels: ['Present', 'Absent', 'Late'],
			datasets: [{
				label: '# of Students',
				data: [presentCount, absentCount, lateCount],
				backgroundColor: [
					'rgba(75, 192, 192, 0.5)',
					'rgba(255, 99, 132, 0.5)',
					'rgba(255, 206, 86, 0.5)'
				],
				borderColor: [
					'rgba(75, 192, 192, 1)',
					'rgba(255, 99, 132, 1)',
					'rgba(255, 206, 86, 1)'
				],
				borderWidth: 2
			}]
		},
		options: {
			responsive: true,
			maintainAspectRatio: false,
			title: {
				display: true,
				text: 'Attendance Overview',
				fontSize: 18,
				fontColor: '#333',
				padding: 20
			},
			legend: {
				display: true,
				position: 'bottom',
				labels: {
					fontSize: 14,
					fontColor: '#333',
					padding: 10
				}
			},
			tooltips: {
				callbacks: {
					label: function(tooltipItem, data) {
						var dataset = data.datasets[tooltipItem.datasetIndex];
						var total = dataset.data.reduce(function(previousValue, currentValue, currentIndex, array) {
							return previousValue + currentValue;
						});
						var currentValue = dataset.data[tooltipItem.index];
						var percentage = Math.floor(((currentValue / total) * 100) + 0.5);
						return percentage + '%';
					}
				}
			}
		}
	};

	// If there's an existing chart, destroy it first
	if (chart) {
			chart.destroy();
	}
	chart = new Chart(ctx, data);
}












// Attach event listener to the dropdown menu
document.getElementById('fileTypeDropdown').addEventListener('change', function() {
	downloadData();
});

function downloadData() {
	const selectedFormat = document.getElementById('fileTypeDropdown').value;

	// Convert data to the selected format
	let formattedData;
	if (selectedFormat === 'csv') {
		formattedData = convertToCSV(tableAttendanceData);
	} else if (selectedFormat === 'json') {
		formattedData = JSON.stringify(tableAttendanceData, null, 2);
	} else if (selectedFormat === 'excel') {
		formattedData = convertToExcel(tableAttendanceData);
	} else if (selectedFormat === 'xml') {
		formattedData = convertToXML(tableAttendanceData);
	} else {
		console.error('Invalid file format selected');
		return;
	}

	// Create a blob with the formatted data
	const blob = new Blob([formattedData], { type: 'text/plain' });

	// Create a link element and set its attributes
	const link = document.createElement('a');
	link.href = URL.createObjectURL(blob);

	const year = yearSelect.value;
	const month = monthSelect.value;
	const user = document.getElementById('user-data').getAttribute('data-username');
	link.download = `${user}-${year}_month-${month}.${selectedFormat}`;

	// Append the link to the body and trigger the download
	document.body.appendChild(link);
	link.click();

	// Clean up by removing the link element
	document.body.removeChild(link);
}

function convertToCSV(data) {
	return data.map(row => row.join(',')).join('\n');
}

function convertToExcel(results) {
	var workbook = XLSX.utils.book_new();
	var worksheet = XLSX.utils.json_to_sheet(results);
	XLSX.utils.book_append_sheet(workbook, worksheet, "Sheet1");
	var excelBuffer = XLSX.write(workbook, { bookType: 'xlsx', type: 'array' });
	return excelBuffer;
}












function updatePerformance() {
	updateAttendanceData();
	 updateAttendanceCounts();
	renderAttendanceTable(tableAttendanceData);
	generateDonutChart();
}

window.onload = updatePerformance;