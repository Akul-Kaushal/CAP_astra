const API_BASE = "http://localhost:8000"; 

// Ask a text-based question
export async function askText({
  uid,
  request,
}: {
  uid: string;
  request: string;
}){
  const res = await fetch(`${API_BASE}/ask/${uid}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ prompt: request }),
  });

  if (!res.ok) {
    const errorText = await res.text();
    throw new Error(`Failed to ask text: ${errorText}`);
  }
  return res.json();
}

// Ask a question with an image
export async function askImage({
  uid,
  prompt,
  image,
}: {
  uid: string;
  prompt: string;
  image: File;
}) {
  const formData = new FormData();
  formData.append("prompt", prompt);
  formData.append("file", image);

  const res = await fetch(`${API_BASE}/ask_image/${uid}`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) throw new Error("Failed to ask image");
  return res.json();
}

// Upload a file for context
export async function uploadFile(uid: string, file: File) {
  const formData = new FormData();
  formData.append("uid", uid);
  formData.append("file", file);

  const res = await fetch(`${API_BASE}/upload`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    const errorText = await res.text();
    throw new Error(`Failed to upload file: ${errorText}`);
  }
  return res.json();
}
