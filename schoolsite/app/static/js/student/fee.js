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
    console.log(url);
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
	console.log(url);

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
    console.log(data);	
    const divBody = document.getElementById('dataContainer');
    divBody.innerHTML = ''; // Clear previous content

    const row = document.createElement('div');

    row.innerHTML = `
	<div>
	    <div><label>Class Name: </label><span> ${data.class_name || 'N/A'}</span></div>
		<div><label>Class ID: </label><span> ${data.class_id || 'N/A'}</span></div>
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

function handleError(error) {
    console.error('Error fetching fee data:', error);
}













// Event listener for the 'term' "year" select element
document.getElementById('term').addEventListener('change', function() {
	fetchFeeDataFromInputs();
	fetchFeesDetails();
	
});

document.getElementById('year').addEventListener('change', function() {
	fetchFeeDataFromInputs();
	fetchFeesDetails();
});



window.onload = function() {
	fetchFeeDataFromInputs();
}


