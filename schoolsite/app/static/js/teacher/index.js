function fetchDataAndCreateChart() {
	const term = document.getElementById('current_term').getAttribute('template-term');
	const year = document.getElementById('current_year').getAttribute('template-year');
	const class_id = document.getElementById('class_id').getAttribute('template-class');

	const url = `/api/teacher/performance?class_id=${class_id}&term=${term}&year=${year}`;
    console.log(url)
	fetch(url)
		.then(response => {
			if (!response.ok) {
				throw new Error('Network response was not ok');
			}
			return response.json();
		})
		.then(jsonData => {
			createScatterPlot(jsonData);
		})
		.catch(error => {
			console.error('There was a problem with the fetch operation:', error);
		});
}




function createScatterPlot(jsonData) {
	// Parse JSON data
	const studentData = jsonData.student;

	// Extract age and total score data
	const studentNames = Object.keys(studentData);
	const ages = studentNames.map(name => studentData[name][2]);
	const totalScores = studentNames.map(name => studentData[name][3]);

	// Create scatter plot
	var ctx = document.getElementById('scatterPlot').getContext('2d');
	var scatterChart = new Chart(ctx, {
		type: 'scatter',
		data: {
			labels: 'Scatter Plot',
			datasets: [{
				label: 'Age vs Total Score',
				data: studentNames.map((name, index) => ({x: ages[index], y: totalScores[index]})),
				backgroundColor: 'rgba(54, 162, 235, 0.5)',
				borderColor: 'rgba(54, 162, 235, 1)',
				borderWidth: 1
			}]
		},
		options: {
			scales: {
				x: {
					type: 'linear',
					position: 'bottom',
					title: {
						display: true,
						text: 'Age'
					}
				},
				y: {
					type: 'linear',
					position: 'left',
					title: {
						display: true,
						text: 'Total Score'
					}
				}
			}
		}
	});
}

document.addEventListener('DOMContentLoaded', function() {
	fetchDataAndCreateChart();
});
