const API_BASE_URL = "http://localhost:8000";

export const api = {
    // Collections
    async getCollections(): Promise<string[]> {
        const res = await fetch(`${API_BASE_URL}/collections/`);
        if (!res.ok) throw new Error("Failed to fetch collections");
        const data = await res.json();
        return data.collections;
    },

    async createCollection(name: string): Promise<void> {
        const res = await fetch(`${API_BASE_URL}/collections/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name }),
        });
        if (!res.ok) throw new Error("Failed to create collection");
    },

    async deleteCollection(name: string): Promise<void> {
        const res = await fetch(`${API_BASE_URL}/collections/${name}`, {
            method: "DELETE",
        });
        if (!res.ok) throw new Error("Failed to delete collection");
    },

    // Documents
    async uploadDocument(collectionName: string, file: File): Promise<any> {
        const formData = new FormData();
        formData.append("file", file);
        formData.append("collection_name", collectionName);

        const res = await fetch(`${API_BASE_URL}/documents/upload`, {
            method: "POST",
            body: formData,
        });
        if (!res.ok) throw new Error("Failed to upload document");
        return res.json();
    },

    // Chat
    async chat(collectionName: string, message: string): Promise<any> {
        const res = await fetch(`${API_BASE_URL}/chat/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ collection_name: collectionName, message }),
        });
        if (!res.ok) throw new Error("Failed to send message");
        return res.json();
    }
};
