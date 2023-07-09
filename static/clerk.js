const publishableKey = "pk_test_Zmxvd2luZy1oYWdmaXNoLTUuY2xlcmsuYWNjb3VudHMuZGV2JA"; // Add your Publishable Key here

const handleSignUp = async () => {
  try {
    await Clerk.openSignUp();
  } catch (error) {
    console.error("Error opening sign up:", error);
  }
};

const handleSignIn = async () => {
  try {
    await Clerk.openSignIn();
  } catch (error) {
    console.error("Error opening sign in:", error);
  }
};

const startClerk = async () => {
  const Clerk = window.Clerk;

  try {
    // Load Clerk environment and session if available
    await Clerk.load();

    const userButton = document.getElementById("user-button");
    const authLinks = document.getElementById("auth-links");

    Clerk.addListener(({ user }) => {
      authLinks.style.display = user ? "none" : "block";
    });

    if (Clerk.user) {
      // Mount user button component
      Clerk.mountUserButton(userButton);
      userButton.style.margin = "auto";
    }
  } catch (error) {
    console.error("Error starting Clerk:", error);
  }
};

(() => {
  const script = document.createElement("script");
  script.setAttribute("data-clerk-publishable-key", publishableKey);
  script.async = true;
  script.src = `https://flowing-hagfish-5.clerk.accounts.dev/npm/@clerk/clerk-js@4/dist/clerk.browser.js`;
  script.crossOrigin = "anonymous";
  script.addEventListener("load", startClerk);
  script.addEventListener("error", () => {
    document.getElementById("no-frontend-api-warning").hidden = false;
  });
  document.body.appendChild(script);
})();
