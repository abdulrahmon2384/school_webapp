var tableAttendanceData = [];
let gradechart;
let histchart;
let studentchart;

function fetchDataAndGenerateTable() {
	var result_type = document.getElementById('resultSelect').value;
	var subject = document.getElementById('subjectSelect').value;
	var term = document.getElementById('termSelect').value;

	var classid = document.getElementById('class_id').getAttribute('template-class')
	var year = document.getElementById('present_year').getAttribute('template-class');
	var apiUrl = `/api/teacher/performance?class_id=${classid}&term=${term}&year=${year}&subject=${subject}&result_type=${result_type}`;
    
	fetch(apiUrl)
		.then(response => {
			if (!response.ok) {
				throw new Error('Network response was not ok');
			}
			return response.json();
		})
		.then(jsonData => {
			generateTableBody(jsonData);
			plotGradeDistribution(jsonData);
			plotHistogram(jsonData);
			displayAverageGrades(jsonData);
		})
		.catch(error => {
			console.error('There was a problem fetching data:', error);
		});
}





// Sorts the table body based on the selected option and order
function sortTableBody(option, order) {
	const tbody = document.getElementById('table-body');
	const rows = Array.from(tbody.querySelectorAll('tr'));

	// Define a custom sorting function based on the selected option and order
	let sortFunction;
	switch(option) {
		case 'fullName':
			sortFunction = (a, b) => {
				const nameA = a.querySelector('td:first-child').innerText.trim();
				const nameB = b.querySelector('td:first-child').innerText.trim();
				return order === 'asc' ? nameA.localeCompare(nameB) : nameB.localeCompare(nameA);
			};
			break;
		case 'percentage':
			sortFunction = (a, b) => {
				const genderA = a.querySelector('td:nth-child(3)').innerText.trim();
				const genderB = b.querySelector('td:nth-child(3)').innerText.trim();
				return order === 'asc' ? genderA.localeCompare(genderB) : genderB.localeCompare(genderA);
			};
			break;
		case 'age':
			sortFunction = (a, b) => {
				const ageA = parseInt(a.querySelector('td:nth-child(5)').innerText.trim(), 10);
				const ageB = parseInt(b.querySelector('td:nth-child(5)').innerText.trim(), 10);
				return order === 'asc' ? ageA - ageB : ageB - ageA;
			};
			break;
		case 'grade':
			sortFunction = (a, b) => {
				const gradeA = parseInt(a.querySelector('td:nth-child(2)').innerText.trim(), 10);
				const gradeB = parseInt(b.querySelector('td:nth-child(2)').innerText.trim(), 10);
				return order === 'asc' ? gradeA - gradeB : gradeB - gradeA;
			};
			break;
		case 'attendance':
			sortFunction = (a, b) => {
				const percentageA = parseFloat(a.querySelector('td:nth-child(4)').innerText.trim());
				const percentageB = parseFloat(b.querySelector('td:nth-child(4)').innerText.trim());
				return order === 'asc' ? percentageA - percentageB : percentageB - percentageA;
			};
			break;
		default:
			return; 
	}

	rows.sort(sortFunction);
	tbody.innerHTML = '';
	rows.forEach(row => tbody.appendChild(row));
}




// Function to generate random colors
function getRandomColor() {
  return `rgba(${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, 0.5)`;
}





function generateTableBody(jsonData) {
	
	tableAttendanceData = [];
	const students = jsonData.student;
	const tbody = document.getElementById('table-body');
	
	tbody.innerHTML = '';
	Object.entries(students).forEach(([username, data]) => {
		
		const [fullName, gender, age, grade, attendance, link, percentage, user] = data;
		tableAttendanceData.push(data)
		const baseImageUrl = document.getElementById('image-data').getAttribute('data-base-image-url');
		const imageUrl = link === 'default.png' ? `${baseImageUrl}default.png` : `${baseImageUrl}${link}`;


		const rowHTML = `
			<tr>
				<td>
				    <a href="#">
                     <img src="${imageUrl}" alt="Profile Image" class="w-8 h-8 rounded block object-cover align-middle"> ${fullName}
                   </a>
				</td>
				<td>${grade}</td>
				<td>${percentage.toFixed(1)}%</td>
				<td>${attendance.toFixed(1)}%</td>
				<td>${age}</td>
				<td>${gender}</td>
				<td>${user}</td>
			</tr>
		`;

		tbody.insertAdjacentHTML('beforeend', rowHTML);
	});
}






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

	var result_type = document.getElementById('resultSelect').value;
	var classid = document.getElementById('class_id').getAttribute('template-class')
	var year = document.getElementById('present_year').getAttribute('template-class');

	link.download = `class_${classid}_${year}_${result_type}.${selectedFormat}`;

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


// Function to plot grade distribution using Chart.js
function plotGradeDistribution(jsonData) {
	const grades = Object.values(jsonData.student).map(studentData => studentData[3]);
	const gradeCounts = {};
	
	grades.forEach(grade => {
		gradeCounts[grade] = (gradeCounts[grade] || 0) + 1;
	});

	// Prepare data for Chart.js
	const labels = Object.keys(gradeCounts);
	const data = Object.values(gradeCounts);

	// Create pie chart
	const ctx = document.getElementById('gradeChart').getContext('2d');
    const newdata = {
			type: 'pie',
			data: {
				labels: labels,
				datasets: [{
					data: data,
					backgroundColor: [
						'rgba(255, 99, 132, 0.5)',
						'rgba(54, 162, 235, 0.5)',
						'rgba(255, 206, 86, 0.5)',
						'rgba(75, 192, 192, 0.5)',
						'rgba(153, 102, 255, 0.5)',
						'rgba(255, 159, 64, 0.5)'
					]
				}]
			},
			options: {
				title: {
					display: true,
					text: 'Grade Distribution'
				}
			}
		}
	
	// If there's an existing chart, destroy it first
	if (gradechart) {
			gradechart.destroy();
	}
	gradechart = new Chart(ctx, newdata);
}



function plotHistogram(jsonData) {
  // Extracting data from JSON
  const students = Object.keys(jsonData.student);
  const attendanceRates = students.map(student => jsonData.student[student][4]);
  const scores = students.map(student => jsonData.student[student][6]);
  const grades = students.map(student => jsonData.student[student][3]);

  // Creating data sets for the histogram
  const data = [];
  const labels = [];

  // Grouping data by grades
  const uniqueGrades = [...new Set(grades)];
  uniqueGrades.forEach(grade => {
	const filteredAttendanceRates = [];
	const filteredScores = [];
	students.forEach((student, index) => {
	  if (grades[index] === grade) {
		filteredAttendanceRates.push(attendanceRates[index]);
		filteredScores.push(scores[index]);
	  }
	});
	data.push({
	  label: `Grade ${grade}`,
	  data: filteredScores,
	  backgroundColor: getRandomColor(),
	  borderColor: getRandomColor(),
	  borderWidth: 1
	});
	labels.push(...filteredAttendanceRates);
  });

 const newdata = {
		 type: 'scatter',
		 data: {
		   labels: labels,
		   datasets: data
		 },
		 options: {
		   scales: {
			 x: {
			   title: {
				 display: true,
				 text: 'Attendance Rate'
			   },
			   type: 'linear',
			   position: 'bottom'
			 },
			 y: {
			   title: {
				 display: true,
				 text: 'Total Score Percentage'
			   },
			   type: 'linear',
			   position: 'left'
			 }
		   }
		 }
	   }

  if (histchart) {
			histchart.destroy();
	}
	
  // Plotting the histogram using Chart.js
  const ctx = document.getElementById('histogramCanvas').getContext('2d');
  histchart = new Chart(ctx, newdata);
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


  const ctx = document.getElementById('studentPerformanceChart').getContext('2d');
  // If there's an existing chart, destroy it first
  if (studentchart) {
		studentchart.destroy();
	}

  studentchart = new Chart(ctx, {
	type: 'bar',
	data: chartData,
	options: options
  });



}
















function displayAverageGrades(jsonData) {
	// Parse JSON data
	const data = jsonData;
    let maleSum = 0;
	let maleCount = 0;
	let femaleSum = 0;
	let femaleCount = 0;
   
	// Iterate through the student objects
	for (const username in data.student) {
		if (data.student.hasOwnProperty(username)) {
			
			const student = data.student[username];
			
			if (student[1] === 'Male') {
				maleSum += student[6];
				maleCount++;
	
			} else if (student[1] === 'Female') {
				femaleSum += student[6];
				femaleCount++;
			}
		}
	}
    //console.log(maleSum, maleCount, femaleSum, femaleCount)
	const maleAverage = maleCount > 0 ? maleSum / maleCount : 0;
	const femaleAverage = femaleCount > 0 ? femaleSum / femaleCount : 0;

	// Update HTML template
	document.getElementById('maleAverageGrade').innerText = `Male Students: Average Grade - ${maleAverage.toFixed(1)}`;
	document.getElementById('femaleAverageGrade').innerText = `Female Students: Average Grade - ${femaleAverage.toFixed(1)}`;
}


function fetchStudentData(dataProcced) {
	const yearElement = document.getElementById("year");
	const termElement = document.getElementById("term");
	const typeElement = document.getElementById("type");
	const usernameElement = document.getElementById('studentSearch');

	// Check if any of the required elements are null
	if (!yearElement || !termElement || !typeElement || !usernameElement) {
		alert("Error: One or more required elements not found.");
		return; // Exit function
	}

	// Retrieve values from elements
	const year = yearElement.value;
	const term = termElement.value;
	const resultType = typeElement.value;
	const username = usernameElement.value;

	//console.log(year, term, resultType);
	const apiUrl = `/api/student/performance?year=${year}&term=${term}&result_type=${resultType}&username=${username}`;

	fetch(apiUrl)
		.then(response => response.json())
		.then(data => {
			dataProcced(data.results);
		})
		.catch(error => console.error('Error fetching data:', error));
}




function populateSelectOptions(jsonData) {
		const selectDiv = document.getElementById('selectOptions');
		const desiredCategories = ['Year', 'Term', 'Type']; // Array of categories to include

		// Clear existing content of selectDiv
		selectDiv.innerHTML = '';

		for (const category in jsonData.category) {
			if (desiredCategories.includes(category)) { // Check if category exists in desiredCategories array
				const select = document.createElement('select');
				const options = jsonData.category[category];
				const categoryId = category.toLowerCase(); // Creating ID based on category name

				// Set ID for the select element
				select.id = categoryId;

				options.forEach(option => {
					const optionElement = document.createElement('option');
					optionElement.textContent = option;
					select.appendChild(optionElement);
				});

				const label = document.createElement('label');
				label.textContent = category + ": ";

				selectDiv.appendChild(label);
				selectDiv.appendChild(select);
				selectDiv.appendChild(document.createElement('br'));
			}
		}

		// Add event listener to selectOptions container to trigger createHorizontalBarChart on change
		selectDiv.addEventListener('change', function () {
			fetchStudentData(createHorizontalBarChart);
		});
	}



function fetchAndPopulateSelectOptions() {
	var username = document.getElementById('studentSearch').value;
	var classId = document.getElementById('class_id').getAttribute('template-class')
	const apiUrl = `/api/teacher/category?class_id=${classId}&username=${username}`;

	return fetch(apiUrl)
		.then(response => response.json())
		.then(data => populateSelectOptions(data))
		.catch(error => console.error('Error fetching data:', error));
}










document.getElementById('resultSelect').addEventListener('change', fetchDataAndGenerateTable);
document.getElementById('subjectSelect').addEventListener('change', fetchDataAndGenerateTable);
document.getElementById('termSelect').addEventListener('change', fetchDataAndGenerateTable);

document.getElementById('sortSelect').addEventListener('change', function() {
	const selectedOption = this.value;
	const selectedOrder = document.getElementById('orderSelect').value;
	sortTableBody(selectedOption, selectedOrder);
});

document.getElementById('orderSelect').addEventListener('change', function() {
	const selectedOption = document.getElementById('sortSelect').value;
	const selectedOrder = this.value;
	sortTableBody(selectedOption, selectedOrder);
});


document.getElementById('fileTypeDropdown').addEventListener('change', function() {
	downloadData();
});




document.getElementById("searchButton").addEventListener("click", function() {
	fetchAndPopulateSelectOptions().then(() => {
		fetchStudentData(createHorizontalBarChart);
	});
});









window.onload = function(){
	fetchDataAndGenerateTable();
}