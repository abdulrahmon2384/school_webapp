// start: Sidebar
const sidebarToggle = document.querySelector('.sidebar-toggle')
const sidebarOverlay = document.querySelector('.sidebar-overlay')
const sidebarMenu = document.querySelector('.sidebar-menu')
const main = document.querySelector('.main')
if(window.innerWidth < 768) {
    main.classList.toggle('active')
    sidebarOverlay.classList.toggle('hidden')
    sidebarMenu.classList.toggle('-translate-x-full')
}
sidebarToggle.addEventListener('click', function (e) {
    e.preventDefault()
    main.classList.toggle('active')
    sidebarOverlay.classList.toggle('hidden')
    sidebarMenu.classList.toggle('-translate-x-full')
})
sidebarOverlay.addEventListener('click', function (e) {
    e.preventDefault()
    main.classList.add('active')
    sidebarOverlay.classList.add('hidden')
    sidebarMenu.classList.add('-translate-x-full')
})
document.querySelectorAll('.sidebar-dropdown-toggle').forEach(function (item) {
    item.addEventListener('click', function (e) {
        e.preventDefault()
        const parent = item.closest('.group')
        if (parent.classList.contains('selected')) {
            parent.classList.remove('selected')
        } else {
            document.querySelectorAll('.sidebar-dropdown-toggle').forEach(function (i) {
                i.closest('.group').classList.remove('selected')
            })
            parent.classList.add('selected')
        }
    })
})
// end: Sidebar




// Predefined array of colors
const predefinedColors = [
	'rgba(54, 162, 235, 0.8)',    // Blue
	'rgba(255, 99, 132, 0.8)',    // Red
	'rgba(255, 159, 64, 0.8)',    // Orange
	'rgba(255, 205, 86, 0.8)',    // Yellow
	'rgba(75, 192, 192, 0.8)',    // Teal
	'rgba(153, 102, 255, 0.8)',   // Purple
	'rgba(255, 102, 204, 0.8)',   // Pink
	'rgba(102, 204, 0, 0.8)',     // Green
	'rgba(204, 102, 0, 0.8)',     // Brown
	'rgba(204, 0, 204, 0.8)',     // Magenta
	'rgba(255, 51, 153, 0.8)',    // Rose
	'rgba(102, 153, 204, 0.8)',   // Lavender
	'rgba(51, 153, 102, 0.8)',    // Jade
	'rgba(153, 153, 153, 0.8)',   // Gray
	'rgba(204, 102, 255, 0.8)'    // Orchid
];








// start: Popper
const popperInstance = {}
document.querySelectorAll('.dropdown').forEach(function (item, index) {
    const popperId = 'popper-' + index
    const toggle = item.querySelector('.dropdown-toggle')
    const menu = item.querySelector('.dropdown-menu')
    menu.dataset.popperId = popperId
    popperInstance[popperId] = Popper.createPopper(toggle, menu, {
        modifiers: [
            {
                name: 'offset',
                options: {
                    offset: [0, 8],
                },
            },
            {
                name: 'preventOverflow',
                options: {
                    padding: 24,
                },
            },
        ],
        placement: 'bottom-end'
    });
})
document.addEventListener('click', function (e) {
    const toggle = e.target.closest('.dropdown-toggle')
    const menu = e.target.closest('.dropdown-menu')
    if (toggle) {
        const menuEl = toggle.closest('.dropdown').querySelector('.dropdown-menu')
        const popperId = menuEl.dataset.popperId
        if (menuEl.classList.contains('hidden')) {
            hideDropdown()
            menuEl.classList.remove('hidden')
            showPopper(popperId)
        } else {
            menuEl.classList.add('hidden')
            hidePopper(popperId)
        }
    } else if (!menu) {
        hideDropdown()
    }
})

function hideDropdown() {
    document.querySelectorAll('.dropdown-menu').forEach(function (item) {
        item.classList.add('hidden')
    })
}
function showPopper(popperId) {
    popperInstance[popperId].setOptions(function (options) {
        return {
            ...options,
            modifiers: [
                ...options.modifiers,
                { name: 'eventListeners', enabled: true },
            ],
        }
    });
    popperInstance[popperId].update();
}
function hidePopper(popperId) {
    popperInstance[popperId].setOptions(function (options) {
        return {
            ...options,
            modifiers: [
                ...options.modifiers,
                { name: 'eventListeners', enabled: false },
            ],
        }
    });
}
// end: Popper



// start: Tab
document.querySelectorAll('[data-tab]').forEach(function (item) {
    item.addEventListener('click', function (e) {
        e.preventDefault()
        const tab = item.dataset.tab
        const page = item.dataset.tabPage
        const target = document.querySelector('[data-tab-for="' + tab + '"][data-page="' + page + '"]')
        document.querySelectorAll('[data-tab="' + tab + '"]').forEach(function (i) {
            i.classList.remove('active')
        })
        document.querySelectorAll('[data-tab-for="' + tab + '"]').forEach(function (i) {
            i.classList.add('hidden')
        })
        item.classList.add('active')
        target.classList.remove('hidden')
    })
})
// end: Tab














let chart; 


function fetchData(dataProcced) {
  const year = document.getElementById("year").value;
  const term = document.getElementById("term").value;
  const resultType = document.getElementById("result_type").value;

  const apiUrl = `/api/performance?year=${year}&term=${term}&result_type=${resultType}`;

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
				size: 10, 
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








function updatePerformance() {
	fetchData(createHorizontalBarChart);
	fetchData(displayResults); 
}
window.onload = updatePerformance;
