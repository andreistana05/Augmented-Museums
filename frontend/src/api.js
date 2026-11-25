export async function identify(blob) {
    const form = new FormData();
    form.append("file", blob, "snapshot.jpg");
    const res = await fetch("/api/identify", {method: "POST", body: form});
    if (!res.ok) throw new Error(`Server: ${res.status}`);
    return res.json();
}