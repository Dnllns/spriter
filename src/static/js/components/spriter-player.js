import { SimulationState, SimulationLogic } from '../domain/simulation.js';
import { CanvasRenderer } from '../infrastructure/canvas_renderer.js';

export class SpriterPlayer extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
        this.state = new SimulationState();
        this.renderer = null;
        this.lastTime = 0;
        this.isPlaying = true;
        this._initialized = false;
    }

    static get observedAttributes() {
        return ['sprite-id', 'speed', 'scale', 'width', 'height', 'base-url'];
    }

    async connectedCallback() {
        if (this._initialized) return;
        this._renderBase();
        const canvas = this.shadowRoot.querySelector('canvas');
        this.renderer = new CanvasRenderer(canvas);

        const spriteId = this.getAttribute('sprite-id');
        if (spriteId) {
            await this.loadSprite(spriteId);
        }

        requestAnimationFrame((t) => this._loop(t));
        this._initialized = true;
    }

    attributeChangedCallback(name, oldValue, newValue) {
        if (name === 'sprite-id' && oldValue !== newValue && this._initialized) {
            this.loadSprite(newValue);
        }
        if (name === 'speed') this.state.speed = parseFloat(newValue) || 1.0;
        if (name === 'scale') this.state.camera.scale = parseFloat(newValue) || 1.0;
        if (name === 'width' || name === 'height') this._updateSize();
    }

    async loadSprite(spriteId) {
        const baseUrl = (this.getAttribute('base-url') || '').replace(/\/$/, '');
        try {
            const fetchUrl = spriteId.startsWith('http') ? spriteId : `${baseUrl}/api/v1/sprites/${spriteId}`;
            const response = await fetch(fetchUrl);
            if (!response.ok) throw new Error("Failed to fetch sprite");
            const spriteData = await response.json();

            this.state.clearEntities();

            // Get latest version
            const latestVersion = spriteData.versions && spriteData.versions.length > 0
                ? spriteData.versions[spriteData.versions.length - 1]
                : null;

            if (latestVersion && latestVersion.image_url) {
                const img = new Image();
                const imgUrl = latestVersion.image_url.startsWith('http')
                    ? latestVersion.image_url
                    : `${baseUrl}${latestVersion.image_url.startsWith('/') ? '' : '/'}${latestVersion.image_url}`;

                img.src = imgUrl;
                await new Promise((res, rej) => {
                    img.onload = res;
                    img.onerror = rej;
                });

                // Preload individual frames if they exist
                if (latestVersion.animations) {
                    for (const anim of latestVersion.animations) {
                        for (const frame of anim.frames) {
                            if (frame.image_location) {
                                const frameImg = new Image();
                                const frameUrl = frame.image_location.startsWith('http')
                                    ? frame.image_location
                                    : `${baseUrl}${frame.image_location.startsWith('/') ? '' : '/'}${frame.image_location}`;

                                frameImg.src = frameUrl;
                                // We don't necessarily block on every frame but it's safer
                                await new Promise((res) => {
                                    frameImg.onload = res;
                                    frameImg.onerror = () => {
                                        console.warn("Failed to load frame image", frameUrl);
                                        res(); // Continue anyway
                                    };
                                });
                                frame.image_obj = frameImg;
                            }
                        }
                    }
                }

                // Default entity wrapper
                const entity = {
                    x: 0, y: 0,
                    width: 64, height: 64,
                    image: img
                };

                // Use first animation if available
                if (latestVersion.animations && latestVersion.animations.length > 0) {
                    entity.animation = latestVersion.animations[0];
                }

                this.state.addEntity(entity);
                this._centerEntity(entity);

                // Track play event
                this._trackPlay(spriteId);
            }
        } catch (error) {
            console.error("SpriterPlayer: Error loading sprite", error);
        }
    }

    async _trackPlay(spriteId) {
        if (!spriteId || spriteId.startsWith('http')) return;
        const baseUrl = (this.getAttribute('base-url') || '').replace(/\/$/, '');
        const trackUrl = `${baseUrl}/api/v1/analytics/sprites/${spriteId}/play`;
        try {
            fetch(trackUrl, { method: 'POST' }).catch(() => { });
        } catch (e) { }
    }

    _centerEntity(entity) {
        const canvas = this.shadowRoot.querySelector('canvas');
        entity.x = (canvas.width / 2) - (entity.width / 2);
        entity.y = (canvas.height / 2) - (entity.height / 2);
    }

    _updateSize() {
        const canvas = this.shadowRoot.querySelector('canvas');
        const w = this.getAttribute('width') || 300;
        const h = this.getAttribute('height') || 300;
        canvas.width = parseInt(w);
        canvas.height = parseInt(h);
    }

    _renderBase() {
        const w = this.getAttribute('width') || 300;
        const h = this.getAttribute('height') || 300;

        this.shadowRoot.innerHTML = `
        <style>
            :host {
                display: inline-block;
                border: 1px solid rgba(255,255,255,0.1);
                border-radius: 12px;
                overflow: hidden;
                background: #0a0e17;
            }
            canvas {
                display: block;
            }
        </style>
        <canvas width="${w}" height="${h}"></canvas>
        `;
    }

    _loop(timestamp) {
        if (!this.isPlaying) return;

        if (!this.lastTime) this.lastTime = timestamp;
        const dt = (timestamp - this.lastTime) / 1000;
        this.lastTime = timestamp;

        SimulationLogic.update(this.state, dt);
        this.renderer.render(this.state);

        requestAnimationFrame((t) => this._loop(t));
    }
}

customElements.define('spriter-player', SpriterPlayer);
