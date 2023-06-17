// Get the mode toggle checkbox element
const modeToggleCheckbox = document.getElementById('mode-toggle-checkbox');

// Add event listener for mode toggle checkbox
modeToggleCheckbox.addEventListener('change', function() {
  if (this.checked) {
    // If checkbox is checked, enable dark mode
    document.body.classList.add('dark-mode');
  } else {
    // If checkbox is unchecked, enable light mode
    document.body.classList.remove('dark-mode');
  }
});
