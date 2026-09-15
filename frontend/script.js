async function analyzeMessage() {

    const message = document.getElementById("message").value.trim();

    if (!message) {
        alert("Please enter a message first.");
        return;
    }

    const button = document.querySelector("button");

    button.innerText = "Analyzing...";
    button.disabled = true;

    try {

        const response = await fetch("http://127.0.0.1:8000/analyze", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })

        });


        const data = await response.json();


        document.getElementById("result")
            .classList.remove("hidden");


        document.getElementById("riskLevel")
            .innerText = data.risk_level + " RISK";


        document.getElementById("riskScore")
            .innerText = data.risk_score;


        const reasonsList =
            document.getElementById("reasons");

        reasonsList.innerHTML = "";


        data.reasons.forEach(reason => {

            const li = document.createElement("li");

            li.innerText = reason;

            reasonsList.appendChild(li);

        });


        document.getElementById("recommendedAction")
            .innerText = data.recommended_action;


    } catch (error) {

        alert(
            "Could not connect to AI Digital Shield backend."
        );

        console.error(error);

    } finally {

        button.innerText = "🔍 Analyze Message";

        button.disabled = false;

    }
}