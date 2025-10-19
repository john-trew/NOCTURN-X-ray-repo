document.addEventListener('DOMContentLoaded', function() {
  // Add any interactive features here
  console.log('GitHub Pages for NOCTURN X-ray loaded');
  
  // Add click event to expandable sections if needed
  const expandButtons = document.querySelectorAll('.expand-button');
  expandButtons.forEach(button => {
    button.addEventListener('click', function() {
      const content = this.nextElementSibling;
      content.style.display = content.style.display === 'none' ? 'block' : 'none';
      this.textContent = content.style.display === 'none' ? 'Show Details' : 'Hide Details';
    });
  });
  
  // Initialize the contribution graph
  initializeHeatmap();
});

function initializeHeatmap() {
  const container = document.getElementById('contribution-graph');
  if (!container) return;
  
  // Get the data from the hidden element
  const dataElement = document.getElementById('heatmap-data');
  if (!dataElement) return;
  
  try {
    // Parse the JSON data
    const heatmapData = JSON.parse(dataElement.textContent);
    
    // Render the heatmap
    renderCalendarHeatmap(container, heatmapData);
    
    // Setup the tooltip
    setupHeatmapTooltips();
  } catch (error) {
    console.error('Error initializing heatmap:', error);
    container.innerHTML = '<p>Error loading contribution data</p>';
  }
}

function renderCalendarHeatmap(container, data) {
  // Get all unique months in the data
  const months = [];
  const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  
  // Group data by month
  const monthsData = {};
  
  // Process each day's data
  for (const date in data) {
    const dateObj = new Date(date);
    const month = dateObj.getMonth();
    const year = dateObj.getFullYear();
    const monthKey = `${year}-${month}`;
    
    if (!monthsData[monthKey]) {
      monthsData[monthKey] = {
        year,
        month,
        days: {}
      };
      months.push(monthKey);
    }
    
    monthsData[monthKey].days[dateObj.getDate()] = data[date];
  }
  
  // Sort months chronologically
  months.sort();
  
  // Create the calendar heatmap
  const heatmapHTML = document.createElement('div');
  heatmapHTML.className = 'calendar-heatmap';
  
  // Create each month's block
  months.forEach(monthKey => {
    const monthData = monthsData[monthKey];
    const monthBlock = document.createElement('div');
    monthBlock.className = 'calendar-heatmap-month';
    
    // Add month label
    const monthLabel = document.createElement('div');
    monthLabel.className = 'calendar-heatmap-month-label';
    monthLabel.textContent = monthNames[monthData.month];
    monthBlock.appendChild(monthLabel);
    
    // Calculate days in month
    const daysInMonth = new Date(monthData.year, monthData.month + 1, 0).getDate();
    
    // Add each day as a square
    for (let day = 1; day <= daysInMonth; day++) {
      const daySquare = document.createElement('div');
      daySquare.className = 'calendar-heatmap-day';
      
      const count = monthData.days[day] || 0;
      let level = 0;
      
      // Set color level based on count
      if (count > 0) {
        if (count === 1) level = 1;
        else if (count <= 3) level = 2;
        else if (count <= 6) level = 3;
        else level = 4;
      }
      
      daySquare.setAttribute('data-level', level);
      daySquare.setAttribute('data-date', `${monthData.year}-${monthData.month+1}-${day}`);
      daySquare.setAttribute('data-count', count);
      
      monthBlock.appendChild(daySquare);
    }
    
    heatmapHTML.appendChild(monthBlock);
  });
  
  // Clear container and add the heatmap
  container.innerHTML = '';
  container.appendChild(heatmapHTML);
  
  // Add legend
  const legend = document.createElement('div');
  legend.className = 'heatmap-legend';
  legend.innerHTML = `
    <div class="heatmap-legend-item">
      <div class="heatmap-legend-square" style="background-color: #ebedf0;"></div>
      <span>No updates</span>
    </div>
    <div class="heatmap-legend-item">
      <div class="heatmap-legend-square" style="background-color: #9be9a8;"></div>
      <span>1 update</span>
    </div>
    <div class="heatmap-legend-item">
      <div class="heatmap-legend-square" style="background-color: #40c463;"></div>
      <span>2-3 updates</span>
    </div>
    <div class="heatmap-legend-item">
      <div class="heatmap-legend-square" style="background-color: #30a14e;"></div>
      <span>4-6 updates</span>
    </div>
    <div class="heatmap-legend-item">
      <div class="heatmap-legend-square" style="background-color: #216e39;"></div>
      <span>7+ updates</span>
    </div>
  `;
  
  container.appendChild(legend);
}

function setupHeatmapTooltips() {
  const squares = document.querySelectorAll('.calendar-heatmap-day');
  let tooltip = null;
  
  squares.forEach(square => {
    square.addEventListener('mouseover', function(event) {
      const date = this.getAttribute('data-date');
      const count = this.getAttribute('data-count');
      
      if (!tooltip) {
        tooltip = document.createElement('div');
        tooltip.className = 'tooltip';
        document.body.appendChild(tooltip);
      }
      
      // Format date 
      const formattedDate = new Date(date).toLocaleDateString(undefined, { 
        weekday: 'long', 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
      });
      
      tooltip.innerHTML = `${formattedDate}: ${count} update${count !== '1' ? 's' : ''}`;
      
      const rect = this.getBoundingClientRect();
      tooltip.style.top = `${rect.top - 30 + window.scrollY}px`;
      tooltip.style.left = `${rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2)}px`;
      tooltip.style.display = 'block';
    });
    
    square.addEventListener('mouseout', function() {
      if (tooltip) {
        tooltip.style.display = 'none';
      }
    });
  });
}
