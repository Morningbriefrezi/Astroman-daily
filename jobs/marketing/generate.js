import fetch from "node-fetch";
import dotenv from "dotenv";
import { buildPrompt } from "./prompt.js";

dotenv.config();

const TELEGRAM_TOKEN = process.env.TELEGRAM_TOKEN;
const CHAT_ID = process.env.CHAT_ID;
const OPENAI_KEY = process.env.OPENAI_KEY;

async function generateMarketingPlan() {
  const day = process.env.DAY || "Monday";
  const response = await fetch("https://api.openai.com/v1/chat/completions", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${OPENAI_KEY}`
    },
    body: JSON.stringify({
      model: "gpt-4o-mini",
      messages: [
        { role: "system", content: "You are a world-class marketing strategist." },
        { role: "user", content: buildPrompt(day) }
      ],
      temperature: 0.95
    })
  });

  const data = await response.json();

  if (!response.ok) {
    console.error("OpenAI API Error:", data);
    throw new Error("OpenAI request failed");
  }

  if (!data.choices || !data.choices[0]) {
    console.error("Unexpected OpenAI response:", data);
    throw new Error("Invalid OpenAI response structure");
  }

  return data.choices[0].message.content;
}

async function sendToTelegram(text) {
  const chunks = text.match(/[\s\S]{1,3900}/g);

  for (const chunk of chunks) {
    await fetch(`https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendMessage`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        chat_id: CHAT_ID,
        text: chunk
      })
    });
  }
}

(async () => {
  try {
    const content = await generateMarketingPlan();
    await sendToTelegram(content);
    console.log("Marketing plan sent successfully.");
  } catch (error) {
    console.error("Fatal Error:", error.message);
    process.exit(1);
  }
})();
