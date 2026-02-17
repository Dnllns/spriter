/**
 * CanvasRenderer (Infrastructure/Adapter)
 * 
 * Responsible for rendering the Simulation State to an HTML5 Canvas.
 * Depends on Domain (State), but Domain does NOT depend on this.
 */

export class CanvasRenderer {
    constructor(canvasOrId) {
        if (typeof canvasOrId === 'string') {
            this.canvas = document.getElementById(canvasOrId);
        } else {
            this.canvas = canvasOrId;
        }

        if (!this.canvas) {
            console.warn(`CanvasRenderer: Canvas not found.`);
            return;
        }
        this.ctx = this.canvas.getContext('2d');
    }

    render(state) {
        if (!this.ctx) return;

        // Clear screen
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        // Draw Grid (Debug)
        this.drawGrid();

        // Render entities
        this.ctx.save();
        this.ctx.scale(state.camera.scale, state.camera.scale);
        this.ctx.translate(-state.camera.x, -state.camera.y);

        state.entities.forEach(entity => {
            if (entity.image) {
                if (entity.animation && entity.animation.frames && entity.animation.frames.length > 0) {
                    const frameIndex = entity.currentFrame || 0;
                    const frame = entity.animation.frames[frameIndex];

                    // Frame data from metadata or calculated
                    // x, y on spritesheet, w, h on spritesheet
                    const sx = frame.x !== undefined ? frame.x : 0;
                    const sy = frame.y !== undefined ? frame.y : 0;
                    const sw = frame.w || entity.image.width;
                    const sh = frame.h || entity.image.height;

                    this.ctx.drawImage(
                        entity.image,
                        sx, sy, sw, sh,
                        entity.x, entity.y, entity.width || 64, entity.height || 64
                    );
                } else {
                    this.ctx.drawImage(entity.image, entity.x, entity.y, entity.width || 64, entity.height || 64);
                }
            } else {
                // Fallback
                this.ctx.fillStyle = entity.color || 'red';
                this.ctx.fillRect(entity.x, entity.y, entity.width || 32, entity.height || 32);
            }
        });

        this.ctx.restore();
    }

    drawGrid() {
        if (!this.ctx) return;

        this.ctx.strokeStyle = 'rgba(255, 255, 255, 0.1)';
        this.ctx.lineWidth = 1;
        const gridSize = 32;

        for (let x = 0; x < this.canvas.width; x += gridSize) {
            this.ctx.beginPath();
            this.ctx.moveTo(x, 0);
            this.ctx.lineTo(x, this.canvas.height);
            this.ctx.stroke();
        }
        for (let y = 0; y < this.canvas.height; y += gridSize) {
            this.ctx.beginPath();
            this.ctx.moveTo(0, y);
            this.ctx.lineTo(this.canvas.width, y);
            this.ctx.stroke();
        }
    }
}
