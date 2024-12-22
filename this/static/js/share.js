const buttons = document.querySelectorAll(".shareButtons");
const shareIcon = document.getElementById("shareIcon");

shareIcon.onclick = () => {
  buttons.forEach((button) => {
    button.toggleAttribute("hidden");
  });
};
