/**
 * SpriteService (Service Layer)
 * 
 * Handles all communication with the backend API.
 * Follows the Adapter pattern, isolating external dependencies 
 * to provide a clean interface to the rest of the application.
 */

export class SpriteService {
    constructor(baseUrl = '/api/v1') {
        this.baseUrl = baseUrl;
    }

    async getSprites() {
        try {
            const response = await fetch(`${this.baseUrl}/sprites`);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            // The API returns a list of Sprites directly
            return await response.json();
        } catch (error) {
            console.error('Error fetching sprites:', error);
            throw error; // Propagate error for UI handling
        }
    }

    async getSprite(id) {
        const response = await fetch(`${this.baseUrl}/sprites/${id}`);
        if (!response.ok) throw new Error("Sprite not found");
        return await response.json();
    }

    async getSimulatorHealth() {
        // Example check for simulator status
        const response = await fetch(`${this.baseUrl}/simulate/health`);
        return response.ok;
    }
}
