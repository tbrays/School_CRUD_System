function toggleStudentFields() {
	const studentFields = document.getElementById('student-fields');
	const isStudentSelected = document.getElementById('student').checked;

	// Show or hide student fields based on the selected role
	if (isStudentSelected) {
		studentFields.style.display = 'block';  // Show fields for students
	} else {
		studentFields.style.display = 'none';   // Hide fields for other roles
	}
}