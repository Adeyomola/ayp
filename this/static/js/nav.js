const profile = document.getElementById("profile");
const list = document.getElementById("profile-list");

profile.addEventListener("click", (e) => {
  e.stopPropagation();
  list.classList.add("show");
});

window.addEventListener("click", () => {
  list.classList.remove("show");
});
