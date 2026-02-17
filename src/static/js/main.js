/**
 * Main Application Logic (Composition Root)
 * 
 * Orchestrates interaction between the Service (API), 
 * Presentation (UI), and Simulator layers.
 */

import { SpriteService } from './services/sprite_service.js';
import { DashboardUI } from './ui/dashboard.js';
import { SimulatorService } from './services/simulator_service.js';

class App {
    constructor() {
        this.spriteService = new SpriteService('/api/v1');

        this.dashboardUI = new DashboardUI({
            container: '.sprites-grid',
            metrics: {
                total: '.metric:nth-child(1) div',
                storage: '.metric:nth-child(2) div',
                requests: '.metric:nth-child(3) div'
            }
        });

        // Simulator (initialized adapter)
        this.simulatorService = new SimulatorService('sim-canvas');

        // Expose method facade
        this.simulator = {
            start: () => this.simulatorService.start(),
            stop: () => this.simulatorService.stop()
        };

        // Make simulator accessible globally for the button callbacks in HTML
        window.simulator = this.simulator;
    }

    async init() {
        console.log("Spriter Frontend Application Initializing...");

        // Setup Navigation
        this.setupNavigation();

        // Load Dashboard Data
        try {
            const sprites = await this.spriteService.getSprites();
            this.dashboardUI.renderSprites(sprites);
        } catch (error) {
            console.error("Failed to fetch initial data:", error);
            this.dashboardUI.showError(error);
        }
    }

    setupNavigation() {
        // Expose navigation globally for simple onclick handlers
        window.navigate = (page) => {
            console.log(`Navigating to ${page}...`);

            // 1. Update Active Nav Item based on the clicked element
            // This is brittle with inline onclick, but for MVP Phase 3 it's fine.
            const clickedElement = event ? event.currentTarget : null;
            if (clickedElement && clickedElement.classList.contains('nav-item')) {
                document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
                clickedElement.classList.add('active');
            }

            // 2. Switch Views
            document.querySelectorAll('.view').forEach(view => view.classList.add('hidden'));

            if (page === 'simulator') {
                document.getElementById('simulator-view').classList.remove('hidden');
                this.simulator.start();
            } else if (page === 'dashboard') {
                document.getElementById('dashboard-view').classList.remove('hidden');
                this.simulator.stop();
            } else {
                // Fallback
                console.warn("View not found for:", page);
                document.getElementById('dashboard-view').classList.remove('hidden');
            }
        };
    }
    async loadSpriteInSimulator(spriteId) {
        console.log("Requesting simulation for sprite:", spriteId);

        // Find the sprite data (we could also fetch it fresh)
        // For MVP, we'll refetch or use cached list if we implemented a store
        try {
            const sprite = await this.spriteService.getSprite(spriteId);

            // Switch view
            window.navigate('simulator');

            // Load into simulator
            this.simulatorService.loadSprite(sprite);
            this.simulatorService.start();

        } catch (error) {
            console.error("Failed to load sprite for simulation:", error);
            alert("Failed to load sprite: " + error.message);
        }
    }
}

// Start the application
const app = new App();
// Expose for interactions
window.app = app;

// Wait for DOM to load fully before any DOM manipulation
document.addEventListener('DOMContentLoaded', () => {
    app.init();
});
