/**
 * Simulation State (Domain)
 * 
 * Pure data structures representing the state of the simulation.
 * No DOM, no API calls, no rendering logic.
 */

export class SimulationState {
    constructor() {
        this.entities = [];
        this.camera = { x: 0, y: 0, scale: 1.0 };
        this.currentTime = 0;
        this.speed = 1.0;
    }

    addEntity(entity) {
        this.entities.push(entity);
    }

    clearEntities() {
        this.entities = [];
    }
}

/**
 * Simulation Logic (Domain Service)
 * 
 * Pure function to update state based on delta time.
 */
export class SimulationLogic {
    static update(state, dt) {
        const effectiveDt = dt * state.speed;
        state.currentTime += effectiveDt;

        state.entities.forEach(entity => {
            // Animation logic
            if (entity.animation && entity.animation.frames && entity.animation.frames.length > 0) {
                if (entity.animElapsed === undefined) entity.animElapsed = 0;
                if (entity.currentFrame === undefined) entity.currentFrame = 0;

                entity.animElapsed += effectiveDt;

                // Get current frame duration or use animation fps
                const fps = entity.animation.fps || 10;
                const frameDuration = 1 / fps;

                if (entity.animElapsed >= frameDuration) {
                    entity.animElapsed -= frameDuration;
                    entity.currentFrame++;

                    if (entity.currentFrame >= entity.animation.frames.length) {
                        if (entity.animation.loop !== false) {
                            entity.currentFrame = 0;
                        } else {
                            entity.currentFrame = entity.animation.frames.length - 1;
                        }
                    }
                }
            }

            if (entity.update) {
                entity.update(effectiveDt);
            }
            // Basic physics (velocity) if present
            if (entity.vx) entity.x += entity.vx * effectiveDt;
            if (entity.vy) entity.y += entity.vy * effectiveDt;
        });

        return state;
    }
}
