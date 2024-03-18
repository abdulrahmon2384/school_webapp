let globalCopy ;

// Function to fetch fee data based on inputs
function fetchFeeDataFromInputs() {
	const user = document.getElementById('user-data').getAttribute('data-username');
	const class_id = document.getElementById('class_id').getAttribute('data-class-id');
	const term = document.getElementById('term').value;
	const year = document.getElementById('year').value;

    fetchFeesDetails(user, term, year, class_id);
	fetchAndDisplayFeeData(user, term, year, class_id);
}



// Function to fetch fee data from the server and display it
function fetchAndDisplayFeeData(user, term, year, class_id) {
	const url = `/api/student/fee?username=${user}&term=${term}&year=${year}&class_id=${class_id}`;
    //console.log(url);
	fetch(url)
		.then(response => response.json())
		.then(data => {
			
			// Extract fee data from the response
			const feeData = data.fee;
			const tableBody = document.getElementById('feeTableBody');
			tableBody.innerHTML = '';

			// Iterate through each fee record and create table rows
			for (const record of feeData) {
				const row = document.createElement('tr');
				
				row.innerHTML = `
					<td>${record.date}</td>
					<td>₦${record.amount}</td>
					<td>₦${record.payment_method}</td>
					<td>${record.status}</td>
					<td>${record.comment}</td>
				`;

				tableBody.appendChild(row);
			}
		})
		.catch(error => {
			console.error('Error fetching fee data:', error);
		});
}






function fetchFeesDetails(user, term, year, class_id) {
    const url = `/api/student/fee_details?username=${user}&term=${term}&year=${year}&class_id=${class_id}`;

    fetch(url)
        .then(handleResponse)
        .then(displayFeeData)
        .catch(handleError);
}

function handleResponse(response) {
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    return response.json();
}

function displayFeeData(data) {
    if (!data) {
        throw new Error('Empty response received');
    }
    	
	fetchClassLessonBookAmount(data.class_id);
    const divBody = document.getElementById('dataContainer');
    divBody.innerHTML = ''; 

    const row = document.createElement('div');

    row.innerHTML = `
	<div id="class-id" data-class="${data.class_id}">
	    <div><label>Class Name: </label><span> ${data.class_name || 'N/A'}</span></div>
		<div><label>Class ID: </label ><div id="class_idd"> ${data.class_id || 'N/A'}</div></div>
        <div><label>Class Fee: </label><span> ₦${data.class_fee || 'N/A'}</span></div>
	</div>
	<div>
	    <div><label>Student Name <span> ${data.name || 'N/A'} </span></label></div>
	    <div><label>Amount Paid: </label><span> ₦${data.amount_paid || 'N/A'} </span></div>
        <div><label>Dept: </label><span>₦${data.dept || 'N/A'}</span></div>
	</div>
    `;

    divBody.appendChild(row);
}





function fetchClassLessonBookAmount(class_id) {
	const url = `/api/student/supplies_Books_amount?class_id=${class_id}`;

	fetch(url)
		.then(handleClassResponse)
		.then(displayFeeClassData)
		.catch(handleError);
}

function handleClassResponse(response) {
	if (!response.ok) {
		throw new Error('Network response was not ok');
	}
	return response.json();
}

function displayFeeClassData(data) {
	if (!data || !data.class_fee || !data.lesson_fee || !data.Books_total || !data.Total) {
		throw new Error('Incomplete or invalid response data received');
	}
	//console.log(data);	
	const divBody = document.getElementById('dueSection');
	divBody.innerHTML = ''; 

	const table = document.createElement('table');
	table.innerHTML = `
			 <tr><th>Category</th><th>Amount</th></tr>
			 <tr><td>Tuition Fees</td><td> ₦${data.class_fee}</td></tr>
			 <tr><td>Lesson Fee</td><td> ₦${data.lesson_fee}</td></tr>
			 <tr><td>Books and Supplies</td><td> ₦${data.Books_total}</td></tr>
			 <tr class="total"><td>Total</td><td> ₦${data.Total}</td></tr>
	`;

	divBody.appendChild(table);
}


function handleError(error) {
	console.error('Error fetching fee data:', error);
}








// Event listener for the 'term' "year" select element
document.getElementById('term').addEventListener('change', function() {
	fetchFeeDataFromInputs();
});

document.getElementById('year').addEventListener('change', function() {
	fetchFeeDataFromInputs();
});



window.onload = function() {
	fetchFeeDataFromInputs();
}


