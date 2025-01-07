const body = document.getElementById("body");

// get popup elements
const linkPopUp = document.getElementById("linkPopUp");
const link = document.getElementById("link");
const linkButton = document.getElementById("linkButton");

// array for editor buttons
const buttons = [
  "bold",
  "italic",
  "underline",
  "justifyCenter",
  "justifyLeft",
  "justifyRight",
  "insertUnorderedList",
  "insertOrderedList",
  "redo",
  "undo",
  "strikeThrough",
  "subscript",
  "superscript",
  "createLink",
  "unlink",
  "formatBlock",
  "outdent",
  "indent",
  "fontSize",
];

// variables for selection preservation
let start;
let end;
let selection;
let selected;

// gets selection offset be entering modal
function preserveSelection() {
  selection = document.getSelection();
  if (selection.anchorOffset < selection.focusOffset) {
    start = selection.anchorOffset;
    end = selection.focusOffset;
  } else {
    start = selection.focusOffset;
    end = selection.anchorOffset;
  }
  selected = selection.focusNode;
}

// restores selection when we're leaving modal
function restoreSelection() {
  let range = document.createRange();

  range.setStart(selected, start);
  range.setEnd(selected, end);

  selection.removeAllRanges();
  selection.addRange(range);
}

// function that saves link entered in modal
function saveLink(command) {
  link.addEventListener("keyup", (e) => {
    if (e.key === "Enter") {
      restoreSelection();
      document.execCommand(command, false, link.value);
      link.value = "https://";
      linkPopUp.style.display = "none";
    }
  });
  linkButton.addEventListener(
    "click",
    () => {
      restoreSelection();
      document.execCommand(command, false, link.value);
      link.value = "https://";
      linkPopUp.style.display = "none";
    },
    { once: true }
  );
}

// forEach loop that creates eventlisteners that execcommand for each editor button
buttons.forEach((element) => {
  let command = element;

  if (element === "createLink") {
    body.addEventListener("mouseup", preserveSelection);
    body.addEventListener("touchend", preserveSelection);
    element = document.getElementById(element);

    element.onclick = () => {
      if (window.getSelection().toString() == "") return;
      linkPopUp.style.display = "flex";
      link.focus();
      saveLink(command);
    };
  } else if (
    element === "insertUnorderedList" ||
    element === "insertOrderedList"
  ) {
    element = document.getElementById(element);
    element.onclick = () => {
      document.execCommand("indent");
      document.execCommand(command);
    };
  } else if (element === "formatBlock") {
    element = document.getElementById(element);
    element.onchange = (e) => {
      e.preventDefault();
      document.execCommand(command, false, element.value);
    };
    element.onmouseup = (e) => {
      e.preventDefault();
      element.selectedIndex = 0;
    };
  } else if (element === "fontSize") {
    element = document.getElementById(element);
    element.onclick = () => document.execCommand(command, false, 1);
  } else {
    element = document.getElementById(element);
    element.onclick = () => document.execCommand(command);
  }
});

// show media
const media = document.getElementById("media");
const close_modal = document.getElementById("close_modal");
const images = document.getElementById("images");

close_modal.onclick = () => {
  media.toggleAttribute("hidden");
};

function show_media() {
  fetch("/meed")
    .then((res) => res.json())
    .then((data) => {
      images.innerHTML = "";
      for (objects of data.result) {
        images.innerHTML += `
        <div style="display: flex; flex-direction: column; align-items: center;">
          <img src="https://verba-post-images.s3.${data.region}.amazonaws.com/${objects["Key"]}" style="height: 81.6px; width: 100px">
          <form action="/meed/delete/${objects["Key"]}" method="post" style="height: max-content; width: max-content;">
            <button type="submit" onclick="return confirm ('Are you sure?')" style="margin: 2px; padding: 0; background-color: transparent; color: initial; border: none;"><i class="fa fa-trash" aria-hidden="true"></i></button>
          </form>
        </div>`;
      }
      // insert inline image
      images.childNodes.forEach((el) => {
        el.addEventListener("click", () => {
          document.execCommand("insertImage", false, el.src);
          media.toggleAttribute("hidden");
        });
      });
    });
  media.toggleAttribute("hidden");
}

const upload_menu = document.getElementById("upload_menu");
const close_upload_menu = document.getElementById("close_upload_menu");

function show_upload_menu() {
  upload_menu.toggleAttribute("hidden");
}

close_upload_menu.onclick = () => {
  upload_menu.toggleAttribute("hidden");
};
