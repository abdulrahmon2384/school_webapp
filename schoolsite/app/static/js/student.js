let chart;


function fetchData(dataProcced) {
  const year = document.getElementById("year").value;
  const term = document.getElementById("term").value;
  const resultType = document.getElementById("result_type").value;

  const apiUrl = `/api/student/performance?year=${year}&term=${term}&result_type=${resultType}`;

  fetch(apiUrl)
	.then(response => response.json())
	.then(data => {

		dataProcced(data.results);
	})
	.catch(error => console.error('Error fetching data:', error));
}

function displayResults(results) {
  const tableBody = document.getElementById("performanceTableBody");
  tableBody.innerHTML = ""; // Clear previous results

  results.forEach(result => {
	const row = document.createElement("tr");
	row.innerHTML = `
	  <td class="py-2 px-4 border-b border-b-gray-50"><span class="text-[13px] font-medium text-gray-400">${result.subject}</div></td>
	  <td class="py-2 px-4 border-b border-b-gray-50"><span class="text-[13px] font-medium text-gray-400">${result.grade}</span></td>
	  <td class="py-2 px-4 border-b border-b-gray-50"><span class="text-[13px] font-medium text-gray-400">${result.percentage}</span></td>
	  <td class="py-2 px-4 border-b border-b-gray-50"><span class="text-[13px] font-medium text-gray-400">${result.comments}</span></td>

	`;
	tableBody.appendChild(row);
  });
}






function createHorizontalBarChart(data) {
  const subjects = data.map(item => item.subject);
  const testMarks = data.map(item => item.test_scores);
  const term = data.map(item => item.term);
  const result_type = data.map(item => item.result_type);


  const colors = predefinedColors.slice(0, subjects.length);

  const chartData = {
	labels: subjects,
	datasets: [{
	  label: term[0]+" : "+result_type[0] ,
	  data: testMarks,
	  backgroundColor: colors,
	  borderColor: 'rgba(0, 0, 0, 0)',
	  borderWidth: 1
	}]
  };

	// Chart options
	  const options = {
		responsive: true,
		indexAxis: 'y',
		scales: {
		  x: {
			beginAtZero: true,
			ticks: {
			  font: {
				family: 'monospace', 
				size: 8, 
			  }
			}
		  },
		  y: {
			ticks: {
			  font: {
				family: 'Verdana', 
				size: 8, 
			  }
			},
			grid: {
				display: false
			}
		  }
		}
	  };


  const ctx = document.getElementById('Chart').getContext('2d');
  // If there's an existing chart, destroy it first
  if (chart) {
		chart.destroy();
	}

  chart = new Chart(ctx, {
	type: 'bar',
	data: chartData,
	options: options
  });



}


//create donut chart

function createDonutChart(data) {
  var grades = data.map(item => item.grade);
  var uniqueGrades = [...new Set(grades)];
  var gradeCounts = {};
  grades.forEach(grade => {
	gradeCounts[grade] = (gradeCounts[grade] || 0) + 1;
  });

  var chartData = {
	labels: uniqueGrades,
	datasets: [{
	  data: uniqueGrades.map(grade => gradeCounts[grade]),
	  backgroundColor: [
		'rgba(255, 99, 132, 0.5)',
		'rgba(54, 162, 235, 0.5)',
		'rgba(255, 206, 86, 0.5)',
		'rgba(75, 192, 192, 0.5)',
		'rgba(153, 102, 255, 0.5)',
		'rgba(255, 159, 64, 0.5)'
	  ],
	  hoverOffset: 4
	}]
  };

  var ctx = document.getElementById('Chart').getContext('2d');
  if (chart) {
		chart.destroy();
  }
  chart = new Chart(ctx, {
	type: 'doughnut',
	data: chartData
  });
}
// end donut chart



document.getElementById('barChartButton').addEventListener('click', function() {
	fetchData(createHorizontalBarChart);
});
document.getElementById('donutChartButton').addEventListener('click', function() {
	fetchData(createDonutChart);
});


function generateFilename(results, fileExtension) {
  const filename = `student_${results[0].year}_${results[0].term}_${results[0].result_type}.${fileExtension}`;
  return filename;
}


function convertToExcel(results) {
	var workbook = XLSX.utils.book_new();
	var worksheet = XLSX.utils.json_to_sheet(results);
	XLSX.utils.book_append_sheet(workbook, worksheet, "Sheet1");
	var excelBuffer = XLSX.write(workbook, { bookType: 'xlsx', type: 'array' });
	return excelBuffer;
}



function downloadData(fileType) {
  fetchData(results => {
	let data;
	let filename;
	switch (fileType) {
	  case 'excel':
		data = convertToExcel(results);
		filename = generateFilename(results, 'xlsx');
		break;
	  case 'csv':
		data = convertToCSV(results);
		filename = generateFilename(results, 'csv');
		break;
	  case 'json':
		data = JSON.stringify(results);
		filename = generateFilename(results, 'json');
		break;
	  case 'xml':
		data = convertToXML(results);
		filename = generateFilename(results, 'xml');
		break;
	  default:
		console.error('Invalid file type');
		return;
	}

	// Create a blob with the data
	const blob = new Blob([data], { type: 'application/octet-stream' });
	const link = document.createElement('a');
	link.href = window.URL.createObjectURL(blob);
	link.download = filename;
	link.click();
	window.URL.revokeObjectURL(link.href);
  });
}


const downloadDropdown = document.getElementById("Download");
downloadDropdown.addEventListener("change", function() {
  const selectedFileType = this.value;
  downloadData(selectedFileType);
});











// Sample attendance data (replace with actual data)
const attendanceData = {
"2024-03-01": "present",
"2024-03-02": "absent",
"2024-03-03": "weekend",
"2024-04-07": 'present'
// Add more dates and attendance status here...
};



// Function to extract morning_attendance and status
function extractAttendanceStatus(apiData) {
attendanceData = {};

apiData.forEach(item => {
  const date = item.morning_attendance;
  const status = item.status;
  attendanceData[date] = status;
  console.log(attendanceData);
});
}



function fetchAttendanceData(dataProcced) {
const term = document.getElementById("term-select").value;
//const username = document.getElementById("username").value;

const apiUrl = `/api/attendance?term=${term}&username=ahenderson`;

fetch(apiUrl)
.then(response => response.json())
.then(data => {

  dataProcced(data.attendance);
})
.catch(error => console.error('Error fetching data:', error));
}





// Function to generate calendar view for a specific month
function generateCalendar(month) {
const calendarElement = document.getElementById("calendar");
calendarElement.innerHTML = ""; // Clear previous calendar

const currentDate = new Date();
const currentYear = currentDate.getFullYear();

const daysInMonth = new Date(currentYear, month, 0).getDate();
const firstDay = new Date(currentYear, month - 1, 1).getDay(); // Day of the week of the first day

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
  const date = `${currentYear}-${month.toString().padStart(2, "0")}-${i.toString().padStart(2, "0")}`;
  const dayElement = document.createElement("div");
  dayElement.classList.add("calendar-day");

  if (attendanceData[date]) {
	dayElement.classList.add(attendanceData[date]);
  }

  dayElement.textContent = i;
  calendarElement.appendChild(dayElement);
}
}


function handleMonthChange() {
const monthSelect = document.getElementById("month-select");
const selectedMonth = parseInt(monthSelect.value);
generateCalendar(selectedMonth);
}

function handleTermChange() {
fetchAttendanceData(extractAttendanceStatus);
}


const monthSelect = document.getElementById("month-select");
monthSelect.addEventListener("change", handleMonthChange);

//const termSelect = document.getElementById("term-select");
//termSelect.addEventListener("change", handleTermChange);


// Initialize calendar for the current month
const currentMonth = new Date().getMonth() + 1; // Months are zero-indexed
console.log(currentMonth)
generateCalendar(currentMonth);




















function updatePerformance() {
	fetchData(createHorizontalBarChart);
	fetchData(displayResults);
}
window.onload = updatePerformance;
