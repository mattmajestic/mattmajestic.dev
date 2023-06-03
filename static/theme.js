// Function to set the theme
function setTheme(theme) {
  const body = document.body;
  body.className = theme;
  localStorage.setItem('theme', theme);
}

// Function to toggle between light and dark themes
function toggleTheme() {
  const body = document.body;
  const currentTheme = body.className;

  if (currentTheme === 'light') {
    setTheme('dark');
  } else if (currentTheme === 'dark') {
    setTheme('light');
  }
}

// Event listener for the theme switch toggle
document.addEventListener('DOMContentLoaded', function() {
  const themeSwitch = document.getElementById('themeSwitch');

  // Check the stored theme preference
  const storedTheme = localStorage.getItem('theme');
  if (storedTheme) {
    setTheme(storedTheme);
    if (storedTheme === 'dark') {
      themeSwitch.checked = true;
    }
  } else {
    setTheme('light'); // Set default theme to light
    themeSwitch.checked = false; // Set toggle switch to unchecked
  }

  themeSwitch.addEventListener('change', toggleTheme);
});
