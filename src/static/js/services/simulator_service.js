/**
 * Simulator Service (UI Adapter)
 * 
 * Adapts pure Domain Logic and Application state to be usable by the UI.
 * Handles interaction with backend API if needed.
 */
import { SimulatorEngine } from '../application/simulator_engine.js';

export class SimulatorService {
    constructor(canvasId) {
        this.engine = new SimulatorEngine(canvasId);
    }

    start() {
        this.engine.start();
    }

    stop() {
        this.engine.stop();
    }

    setSpeed(speed) {
        this.engine.setSpeed(speed);
    }

    /**
     * Loads a sprite animation into the simulator
     * @param {Object} spriteData - The sprite DTO from the API
     */
    async loadSprite(spriteData) {
        console.log("Loading sprite into simulator:", spriteData);
        // clean current
        this.engine.clearEntities();

        // Get latest version
        const latestVersion = spriteData.versions && spriteData.versions.length > 0
            ? spriteData.versions[spriteData.versions.length - 1]
            : null;

        if (latestVersion && latestVersion.image_url) {
            // Load image asynchronously
            const img = new Image();
            img.src = latestVersion.image_url;

            await new Promise((resolve, reject) => {
                img.onload = resolve;
                img.onerror = reject;
            });

            // Extract animation if present
            let animation = null;
            if (latestVersion.animations && latestVersion.animations.length > 0) {
                // For now, just pick the first one (usually IDLE)
                animation = latestVersion.animations[0];
            } else {
                // Default: one frame showing the whole image
                animation = {
                    name: 'default',
                    fps: 1,
                    frames: [{ x: 0, y: 0, w: img.width, h: img.height }],
                    loop: true
                };
            }

            // Add entity with image property and animation
            this.engine.addEntity({
                x: 100, y: 100,
                width: 128, height: 128, // Scaled for better visibility
                image: img,
                animation: animation
            });
        } else {
            console.warn("No image found for sprite, using placeholder");
            this.engine.addEntity({
                x: 100, y: 100,
                width: 64, height: 64,
                color: 'lime'
            });
        }
    }
}
