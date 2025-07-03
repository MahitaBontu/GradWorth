console.log("roi.js loaded");

// URL to your JSON file
const jsonUrl = "https://raw.githubusercontent.com/mahitabontu/GradWorth/main/roi_institution_data.json";

// Fetch JSON data and populate dropdown
fetch(jsonUrl)
  .then(response => response.json())
  .then(data => {
    const dropdown = document.getElementById('schoolDropdown');
    
    // Sort schools alphabetically
    data.sort((a, b) => a.school.localeCompare(b.school));
    
    // Add all schools to dropdown
    data.forEach((school, index) => {
      const option = document.createElement('option');
      option.value = index;
      option.textContent = school.school;
      dropdown.appendChild(option);
    });

    // Save data globally
    window.schoolData = data;
  })
  .catch(error => {
    console.error("Error loading JSON:", error);
    document.getElementById('roiResult').textContent = "Error loading school data. Please try again later.";
  });

// Major-specific salary adjustments (multipliers based on national averages)
const majorMultipliers = {
  'Computer Science': 1.2,
  'Engineering': 1.25,
  'Business': 1.1,
  'Mathematics': 1.15,
  'Biology': 0.9,
  'Chemistry': 0.95,
  'Physics': 1.1,
  'Psychology': 0.85,
  'Economics': 1.15,
  'English': 0.8,
  'History': 0.8,
  'Political Science': 0.9,
  'Sociology': 0.85,
  'Art': 0.75,
  'Music': 0.75,
  'Education': 0.8,
  'Nursing': 1.1,
  'Medicine': 1.5,
  'Law': 1.3
};

// Calculate ROI function with major consideration
function calculateROI(earnings, debt, cost, major) {
  if (!earnings || !debt) return null;
  const multiplier = majorMultipliers[major] || 1;
  const adjustedEarnings = earnings * multiplier;
  return (adjustedEarnings - debt) / (cost || debt);
}

// Format currency
function formatCurrency(amount) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    maximumFractionDigits: 0
  }).format(amount);
}

// When user selects a major
function onMajorChange() {
  updateROIDisplay();
}

// When user selects a school from dropdown
function onSchoolChange() {
  updateROIDisplay();
}

// Update ROI display based on selected school and major
function updateROIDisplay() {
  const resultDiv = document.getElementById('roiResult');
  const schoolDropdown = document.getElementById('schoolDropdown');
  const majorDropdown = document.getElementById('majorDropdown');
  
  const selectedIndex = schoolDropdown.value;
  const selectedMajor = majorDropdown.value;

  if (!window.schoolData || !selectedIndex || !selectedMajor) {
    resultDiv.innerHTML = "Please select both a school and major to view ROI information.";
    return;
  }

  const school = window.schoolData[selectedIndex];
  const earnings = school.earnings;
  const debt = school.debt;
  const cost = school.tuition_in_state;
  const roi = calculateROI(school.earnings, school.debt, school.cost, selectedMajor);

  const majorMultiplier = majorMultipliers[selectedMajor];
  const adjustedEarnings = formatCurrency(school.earnings * majorMultiplier);

  let roiHtml = '';
  if (roi !== null) {
    roiHtml = `<p><strong>ROI:</strong> ${(roi * 100).toFixed(1)}%</p>`;
  } else {
    roiHtml = `<p><em>Insufficient data to calculate ROI</em></p>`;
    resultsHtml += `<p><em>Insufficient data to calculate ROI</em></p>`;
  }

  resultDiv.innerHTML = resultsHtml;
}
