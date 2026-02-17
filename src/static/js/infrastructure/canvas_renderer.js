/**
 * CanvasRenderer (Infrastructure/Adapter)
 * 
 * Responsible for rendering the Simulation State to an HTML5 Canvas.
 * Depends on Domain (State), but Domain does NOT depend on this.
 */

export class CanvasRenderer {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        if (!this.canvas) {
            console.warn(`CanvasRenderer: Canvas with id '${canvasId}' not found.`);
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
                // If sprite sheet logic existed, we'd use drawImage locally clipped.
                // For now, draw whole image scaled to fit
                this.ctx.drawImage(entity.image, entity.x, entity.y, entity.width || 64, entity.height || 64);
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
