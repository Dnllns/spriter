/**
 * Simulator Engine (Application)
 * 
 * Orchestrates interaction between the Service (API), 
 * Presentation (UI), and Simulator layers.
 */

import { SimulationState, SimulationLogic } from "../domain/simulation.js";
import { CanvasRenderer } from "../infrastructure/canvas_renderer.js";

export class SimulatorEngine {
    constructor(canvasId) {
        this.renderer = new CanvasRenderer(canvasId);
        this.state = new SimulationState();

        this.isRunning = false;
        this.lastTime = 0;

        // Bind methods
        this.loop = this.loop.bind(this);
    }

    start() {
        if (this.isRunning) return;
        this.isRunning = true;
        this.lastTime = performance.now();
        requestAnimationFrame(this.loop);
        console.log("SimulatorEngine: Started.");
    }

    stop() {
        this.isRunning = false;
        console.log("SimulatorEngine: Stopped.");
    }

    loop(timestamp) {
        if (!this.isRunning) return;

        const deltaTime = (timestamp - this.lastTime) / 1000; // seconds
        this.lastTime = timestamp;

        this.update(deltaTime);
        this.render();

        requestAnimationFrame(this.loop);
    }

    update(dt) {
        // Pure domain logic update
        SimulationLogic.update(this.state, dt);
    }

    render() {
        // Render current state via adapter
        this.renderer.render(this.state);
    }

    // Application facade methods
    addEntity(entity) {
        this.state.addEntity(entity);
    }

    clearEntities() {
        this.state.clearEntities();
    }
}
