// Function to fetch fee data based on inputs
function fetchFeeDataFromInputs() {
	const user = document.getElementById('user-data').getAttribute('data-username');
	const class_id = document.getElementById('class_id').getAttribute('data-class-id');
	const term = document.getElementById('term').value;
	const year = document.getElementById('year').value;

	console.log(user, class_id, term, year);
	fetchAndDisplayFeeData(user, term, year, class_id);
}

// Function to fetch fee data from the server and display it
function fetchAndDisplayFeeData(user, term, year, class_id) {
	const url = `/api/student/fee?username=${user}&term=${term}&year=${year}&class_id=${class_id}`;

	fetch(url)
		.then(response => response.json())
		.then(data => {
			console.log(data)
			// Extract fee data from the response
			const feeData = data.fee;
			const tableBody = document.getElementById('feeTableBody');
			tableBody.innerHTML = '';

			// Iterate through each fee record and create table rows
			for (const record of feeData) {
				const row = document.createElement('tr');
				
				row.innerHTML = `
					<td>${record.date}</td>
					<td>${record.amount}</td>
					<td>${record.payment_method}</td>
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




// Event listener for the 'term' "year" select element
document.getElementById('term').addEventListener('change', function() {
	fetchFeeDataFromInputs();
});

document.getElementById('year').addEventListener('change', function() {
	fetchFeeDataFromInputs();
});



window.onload = fetchFeeDataFromInputs; 


