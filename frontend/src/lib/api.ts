const API_BASE = "http://localhost:8000"; 

export async function askText(uid: string, question: string) {
  const res = await fetch(`${API_BASE}/ask`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ uid, question }),
  });

  if (!res.ok) throw new Error("Failed to ask text");
  return res.json();
}


export async function askImage(uid: string, question: string, image: File) {
  const formData = new FormData();
  formData.append("uid", uid);
  formData.append("question", question);
  formData.append("file", image);

  const res = await fetch(`${API_BASE}/ask_image`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) throw new Error("Failed to ask image");
  return res.json();
}

export async function uploadFile(uid: string, file: File) {
  const formData = new FormData();
  formData.append("uid", uid);
  formData.append("file", file);

  const res = await fetch(`${API_BASE}/upload`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) throw new Error("Failed to upload file");
  return res.json();
}

