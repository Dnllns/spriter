/**
 * Main Application Logic (Composition Root)
 * 
 * Orchestrates interaction between the Service (API), 
 * Presentation (UI), and Simulator layers.
 */

import { SpriteService } from './services/sprite_service.js';
import { DashboardUI } from './ui/dashboard.js';
import { SimulatorService } from './services/simulator_service.js';
import './components/spriter-player.js';

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
            stop: () => this.simulatorService.stop(),
            setSpeed: (speed) => this.simulatorService.setSpeed(speed)
        };

        this.currentSimulatedSpriteId = null;

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
            } else if (page === 'library') {
                document.getElementById('library-view').classList.remove('hidden');
                this.simulator.stop();
                this.loadLibraryContent();
            } else {
                // Fallback
                console.warn("View not found for:", page);
                document.getElementById('dashboard-view').classList.remove('hidden');
            }
        };
    }

    async loadLibraryContent() {
        const container = document.getElementById('frames-container');
        container.innerHTML = '<div style="grid-column: 1/-1; text-align: center;">Loading frames...</div>';

        try {
            const sprites = await this.spriteService.getSprites();
            container.innerHTML = '';

            sprites.forEach(sprite => {
                const latestVersion = sprite.versions && sprite.versions.length > 0
                    ? sprite.versions[sprite.versions.length - 1]
                    : null;

                if (latestVersion && latestVersion.animations) {
                    latestVersion.animations.forEach(anim => {
                        anim.frames.forEach(frame => {
                            if (frame.image_location) {
                                const card = document.createElement('div');
                                card.className = 'card sprite-card';
                                card.innerHTML = `
                                    <div class="sprite-preview">
                                        <img src="${frame.image_location}" style="max-width: 100%; max-height: 100%; object-fit: contain;">
                                    </div>
                                    <div class="sprite-meta">
                                        <h3 style="font-size: 0.9rem;">${sprite.name}</h3>
                                        <p style="font-size: 0.7rem; color: var(--color-text-muted);">Frame ${frame.index} - ${anim.name}</p>
                                    </div>
                                `;
                                container.appendChild(card);
                            }
                        });
                    });
                }
            });

            if (container.children.length === 0) {
                container.innerHTML = '<div style="grid-column: 1/-1; text-align: center;">No individual frames found. Try uploading a sprite with dimensions.</div>';
            }
        } catch (error) {
            console.error("Failed to load library content:", error);
            container.innerHTML = '<div style="grid-column: 1/-1; text-align: center; color: var(--color-danger);">Error loading frames.</div>';
        }
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
            this.currentSimulatedSpriteId = spriteId;
            this.simulatorService.loadSprite(sprite);
            this.simulatorService.start();

        } catch (error) {
            console.error("Failed to load sprite for simulation:", error);
            alert("Failed to load sprite: " + error.message);
        }
    }

    showUploadModal() {
        document.getElementById('upload-modal').classList.remove('hidden');
    }

    async handleUpload(form) {
        const formData = new FormData(form);
        const name = formData.get('name');
        const category = formData.get('category');
        const file = formData.get('file');
        const frameW = parseInt(formData.get('frame_w'));
        const frameH = parseInt(formData.get('frame_h'));

        try {
            // 1. Create Sprite
            const sprite = await this.spriteService.createSprite(name, [category]);
            console.log("Sprite created:", sprite);

            // 2. Prepare Animations if grid defined
            let animations = [];
            if (file && !isNaN(frameW) && !isNaN(frameH)) {
                try {
                    const img = await this._loadImage(file);
                    animations = this._generateGridAnimation(img, frameW, frameH);
                } catch (e) {
                    console.warn("Could not auto-generate animations from cloud file, skipping grid.");
                }
            }

            // 3. Upload Version
            if (file) {
                await this.spriteService.addSpriteVersion(sprite.id, file, animations);
                console.log("Version uploaded with animations:", animations);
            }

            // 4. UI Feedback and Close
            alert("Sprite uploaded successfully!");
            document.getElementById('upload-modal').classList.add('hidden');
            form.reset();

            // 5. Reload Dashboard
            this.init();

        } catch (error) {
            console.error("Upload failed:", error);
            alert("Upload failed: " + error.message);
        }
    }

    _loadImage(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = (e) => {
                const img = new Image();
                img.onload = () => resolve(img);
                img.onerror = reject;
                img.src = e.target.result;
            };
            reader.onerror = reject;
            reader.readAsDataURL(file);
        });
    }

    _generateGridAnimation(img, w, h) {
        const frames = [];
        let index = 0;
        for (let y = 0; y < img.height; y += h) {
            for (let x = 0; x < img.width; x += w) {
                if (x + w <= img.width && y + h <= img.height) {
                    frames.push({ index: index++, x, y, w, h });
                }
            }
        }
        return [{
            name: 'idle',
            fps: 10,
            frames: frames,
            loop: true
        }];
    }

    showEmbedModal() {
        if (!this.currentSimulatedSpriteId) {
            alert("No sprite loaded to share!");
            return;
        }

        const modal = document.getElementById('embed-modal');
        const code = document.getElementById('embed-code');

        const origin = window.location.origin;
        const scriptUrl = `${origin}/static/js/components/spriter-player.js`;

        const embedHtml = `
<!-- Spriter Player Embed -->
<script type="module" src="${scriptUrl}"></script>
<spriter-player 
  sprite-id="${this.currentSimulatedSpriteId}" 
  base-url="${origin}"
  width="400" 
  height="400" 
  speed="1.0">
</spriter-player>`.trim();

        code.textContent = embedHtml;
        modal.classList.remove('hidden');
    }

    copyEmbedCode() {
        const code = document.getElementById('embed-code').textContent;
        navigator.clipboard.writeText(code).then(() => {
            alert("Embed code copied to clipboard!");
        });
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
