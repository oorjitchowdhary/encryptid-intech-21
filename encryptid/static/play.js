const notyf = new Notyf({ position: { x: "right", y: "top" } });
document.getElementById("answer").addEventListener(
  "keydown",
  (e) => {
    if (!e) {
      let e = window.event;
    }
    if (e.keyCode === 13) {
      handleSubmit();
    }
  },
  false
);

const handleSubmit = async () => {
  const answer = document.getElementById("answer").value;

  if (!answer) {
    notyf.error("Please enter an answer.");
  } else {
    await fetch("/submit", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        answer: answer,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          notyf.success(data.message);
          setTimeout(() => window.location.reload(), 500);
        } else {
          notyf.error(data.message);
          document.getElementById("answer").value = "";
        }
      })
      .catch((err) => console.log(err));
  }
};
