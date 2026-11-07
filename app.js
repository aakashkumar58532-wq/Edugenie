const task = document.getElementById("task");
const inputText = document.getElementById("inputText");
const submitBtn = document.getElementById("submitBtn");
const clearBtn = document.getElementById("clearBtn");
const resultCard = document.getElementById("resultCard");
const result = document.getElementById("result");
const resultType = document.getElementById("resultType");

const endpointMap = {
  qa: "/qa",
  explain: "/explain",
  quiz: "/quiz",
  summarize: "/summarize",
  learn: "/learn/recommendations"
};

const labels = {
  qa: "Q&A",
  explain: "Concept Explanation",
  quiz: "3 MCQs",
  summarize: "Summary",
  learn: "Learning Path"
};

function renderQuiz(data) {
  result.innerHTML = "";
  data.questions.forEach((item, index) => {
    const wrapper = document.createElement("div");
    wrapper.className = "quiz-question";

    const title = document.createElement("h3");
    title.textContent = `${index + 1}. ${item.question}`;
    wrapper.appendChild(title);

    item.options.forEach((option) => {
      const button = document.createElement("button");
      button.className = "option";
      button.textContent = option;
      button.addEventListener("click", () => {
        wrapper.querySelectorAll(".option").forEach((b) => b.disabled = true);
        if (option === item.answer) {
          button.classList.add("correct");
          button.textContent += " ✓ Correct";
        } else {
          button.classList.add("wrong");
          button.textContent += " ✗ Try again";
          wrapper.querySelectorAll(".option").forEach((b) => {
            if (b.textContent === item.answer) {
              b.classList.add("correct");
              b.textContent += " ✓ Correct answer";
            }
          });
        }
        if (item.explanation) {
          const explanation = document.createElement("p");
          explanation.className = "explanation";
          explanation.textContent = item.explanation;
          wrapper.appendChild(explanation);
        }
      });
      wrapper.appendChild(button);
    });
    result.appendChild(wrapper);
  });
}

async function generate() {
  const text = inputText.value.trim();
  if (!text) {
    resultCard.classList.remove("hidden");
    result.innerHTML = '<div class="error">Please enter a question, topic, or text.</div>';
    return;
  }

  submitBtn.disabled = true;
  submitBtn.textContent = "Generating...";
  resultCard.classList.remove("hidden");
  resultType.textContent = labels[task.value];
  result.textContent = "EduGenie is thinking...";

  try {
    const response = await fetch(endpointMap[task.value], {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text })
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || "Request failed.");
    }

    if (task.value === "quiz") renderQuiz(data.result);
    else result.textContent = data.result;
  } catch (error) {
    result.innerHTML = `<div class="error">${escapeHtml(error.message)}</div>`;
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = "Generate";
  }
}

function escapeHtml(value) {
  return value.replace(/[&<>\"]/g, (char) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"
  }[char]));
}

submitBtn.addEventListener("click", generate);
clearBtn.addEventListener("click", () => {
  inputText.value = "";
  result.innerHTML = "";
  resultCard.classList.add("hidden");
});

inputText.addEventListener("keydown", (event) => {
  if ((event.ctrlKey || event.metaKey) && event.key === "Enter") generate();
});
